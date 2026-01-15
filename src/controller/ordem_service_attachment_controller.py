from flask import Blueprint
from src.service.ordem_service_attachment import OrdemServiceAttachmentService

ordem_service_attachment_controller = Blueprint("ordem-service-attachment", __name__)

ordem_service_attachment_service = OrdemServiceAttachmentService()


@ordem_service_attachment_controller.route("/upload-url/<report_id>", methods=["POST"])
def get_upload_url(report_id: str):
    return ordem_service_attachment_service.generate_upload_url(report_id)


@ordem_service_attachment_controller.route("/download-url/<object_key>", methods=["GET"])
def get_download_url(object_key: str):
    return {
        "download_url": ordem_service_attachment_service.generate_download_url(object_key)
    }
