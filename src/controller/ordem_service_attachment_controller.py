from flask import Blueprint, g
from flask_pydantic import validate

from src.decorators.web_jwt_required import web_jwt_required
from src.dto.attachment_dto import MediaFinalizeRequestDTO, MediaUploadRequestDTO
from src.service.ordem_service_attachment import OrdemServiceAttachmentService

ordem_service_attachment_controller = Blueprint("ordem-service-attachment", __name__)
ordem_service_attachment_service = OrdemServiceAttachmentService()


@ordem_service_attachment_controller.route("/upload-urls/<order_service_id>", methods=["POST"])
@web_jwt_required
@validate()
def get_upload_urls(order_service_id: str, body: MediaUploadRequestDTO):
    return ordem_service_attachment_service.generate_upload_urls(
        order_service_id, g.web_client_id, body.media
    )


@ordem_service_attachment_controller.route("/complete/<order_service_id>", methods=["PUT"])
@web_jwt_required
@validate()
def complete_upload(order_service_id: str, body: MediaFinalizeRequestDTO):
    return ordem_service_attachment_service.finalize(
        order_service_id, g.web_client_id, body.media, body.base_media
    )


@ordem_service_attachment_controller.route("/media/<order_service_id>", methods=["GET"])
@web_jwt_required
def get_media(order_service_id: str):
    return ordem_service_attachment_service.get_media(order_service_id, g.web_client_id)
