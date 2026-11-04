from flask import Blueprint, request
from flask_pydantic import validate
from src.dto.technician_dto import TechnicianDTO, TechnicianSignatureDTO, TechnicianSignatureCompleteDTO
from src.service.technician_service import TechnicianService

technician_controller = Blueprint('technician', __name__)
service = TechnicianService()
def _client_id(): return request.headers.get('Client-Id') or ''
@technician_controller.route('', methods=['GET'])
def get_all(): return service.get_all(_client_id())
@technician_controller.route('', methods=['POST'])
@validate()
def upsert(body: TechnicianDTO): return service.upsert(body, _client_id())
@technician_controller.route('/<technician_id>', methods=['PUT'])
@validate()
def update(technician_id: str, body: TechnicianDTO): body.id = technician_id; return service.upsert(body, _client_id())
@technician_controller.route('/<technician_id>', methods=['DELETE'])
def delete(technician_id: str): return service.delete(technician_id, _client_id())
@technician_controller.route('/<technician_id>/signature/upload-url', methods=['POST'])
@validate()
def upload_url(technician_id: str, body: TechnicianSignatureDTO): return service.upload_url(technician_id, body, _client_id())
@technician_controller.route('/<technician_id>/signature/complete', methods=['PUT'])
@validate()
def complete_signature(technician_id: str, body: TechnicianSignatureCompleteDTO): return service.complete_signature(technician_id, body, _client_id())
