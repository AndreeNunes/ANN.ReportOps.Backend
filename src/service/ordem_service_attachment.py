import uuid
from src.dto.api_result import ApiResult
from src.infra.tebi import get_tebi_client
import os

BUCKET_NAME = os.getenv("TEBI_BUCKET")


class OrdemServiceAttachmentService:
    def __init__(self):
        self.s3 = get_tebi_client()

    def generate_upload_url(
        self,
        report_id: str,
        content_type: str = "image/jpeg",
        expires_in: int = 3600,
    ):
        filename = f"photo-{uuid.uuid4()}.jpg"
        
        object_key = f"order-service-report/{report_id}/{filename}"

        upload_url = self.s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": object_key,
                "ContentType": content_type,
            },
            ExpiresIn=expires_in,
        )

        response = ApiResult.success_result(
            data={
                "upload_url": upload_url,
                "object_key": object_key,
            },
            message="Upload URL generated successfully",
            status_code=200
        )

        return response.to_dict(), response.status_code

    def generate_download_url(
        self,
        object_key: str,
        expires_in: int = 3600,
    ):
        return self.s3.generate_presigned_url(
            ClientMethod="get_object",
            Params={
                "Bucket": BUCKET_NAME,
                "Key": object_key,
            },
            ExpiresIn=expires_in,
        )
