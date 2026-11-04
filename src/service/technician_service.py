import re, uuid
from botocore.exceptions import ClientError
from src.dto.api_result import ApiResult
from src.infra.db import get_connection
from src.infra.tebi import get_bucket_name, get_s3_client
from src.repository.technician_repository import TechnicianRepository
_ID=re.compile(r'^[A-Za-z0-9_-]{1,36}$')
class TechnicianService:
    def __init__(self): self.repository=TechnicianRepository();self.s3=None;self.bucket=None
    def storage(self):
        if not self.s3:self.s3,self.bucket=get_s3_client(),get_bucket_name()
        return self.s3,self.bucket
    def key(self,client_id,technician_id):return f'clients/{client_id}/technicians/{technician_id}/signature.png'
    def serialize(self,row,s3=None,bucket=None):
        value=dict(row)
        for key in ('created_at','updated_at','signature_updated_at'):
            if hasattr(value.get(key),'isoformat'):value[key]=value[key].isoformat()
        if value.get('signature_object_key') and s3:value['signature_download_url']=s3.generate_presigned_url('get_object',Params={'Bucket':bucket,'Key':value['signature_object_key']},ExpiresIn=600)
        return value
    def get_all(self,client_id):
        conn=get_connection()
        try:
            rows=self.repository.get_all(client_id,conn);s3=bucket=None
            if any(x.get('signature_object_key') for x in rows):s3,bucket=self.storage()
            return ApiResult.success_result(data=[self.serialize(x,s3,bucket) for x in rows],message='Técnicos encontrados').to_dict(),200
        finally:conn.close()
    def upsert(self,dto,client_id):
        technician_id=dto.id or str(uuid.uuid4())
        if not _ID.fullmatch(technician_id):return ApiResult.validation_error_result('Identificador de técnico inválido').to_dict(),422
        conn=get_connection()
        try:
            self.repository.upsert({'id':technician_id,'name':dto.name.strip(),'email':dto.email.strip() if dto.email else None,'phone':dto.phone.strip() if dto.phone else None},client_id,conn);saved=self.repository.get_owned(technician_id,client_id,conn)
            if not saved:return ApiResult.validation_error_result('Identificador de técnico já pertence a outro tenant').to_dict(),422
            return ApiResult.success_result(data=self.serialize(saved),message='Técnico salvo com sucesso').to_dict(),200
        finally:conn.close()
    def delete(self,technician_id,client_id):
        conn=get_connection()
        try:
            if not self.repository.deactivate(technician_id,client_id,conn):return ApiResult.not_found_result('Técnico não encontrado').to_dict(),404
            return ApiResult.success_result(data=None,message='Técnico removido com sucesso').to_dict(),200
        finally:conn.close()
    def upload_url(self,technician_id,dto,client_id):
        conn=get_connection()
        try:
            if not self.repository.get_owned(technician_id,client_id,conn):return ApiResult.not_found_result('Técnico não encontrado').to_dict(),404
            s3,bucket=self.storage();key=self.key(client_id,technician_id)
            return ApiResult.success_result(data={'object_key':key,'upload_url':s3.generate_presigned_url('put_object',Params={'Bucket':bucket,'Key':key,'ContentType':dto.content_type},ExpiresIn=600)},message='URL de upload gerada').to_dict(),200
        finally:conn.close()
    def complete_signature(self,technician_id,dto,client_id):
        if dto.object_key!=self.key(client_id,technician_id):return ApiResult.validation_error_result('Chave de assinatura inválida').to_dict(),422
        conn=get_connection()
        try:
            if not self.repository.get_owned(technician_id,client_id,conn):return ApiResult.not_found_result('Técnico não encontrado').to_dict(),404
            s3,bucket=self.storage()
            try:s3.head_object(Bucket=bucket,Key=dto.object_key)
            except ClientError:return ApiResult.validation_error_result('Assinatura não encontrada no storage').to_dict(),422
            self.repository.update_signature(technician_id,client_id,dto.object_key,dto.content_type,dto.size_bytes,conn)
            return ApiResult.success_result(data=self.serialize(self.repository.get_owned(technician_id,client_id,conn),s3,bucket),message='Assinatura salva com sucesso').to_dict(),200
        finally:conn.close()
