from flask import Blueprint, request
from flask_pydantic import validate
from src.dto.report_reference_dto import ReportReferenceDTO
from src.dto.report_dto import ReportDTO
from src.dto.report_ids_dto import ReportIdsDTO
from src.service.report_service import ReportService

report_controller = Blueprint("report", __name__)
service = ReportService()


@report_controller.route("", methods=["GET"])
@validate()
def get_all():
    app_user_id = request.headers.get("App-User-Id")
    return service.get_all(app_user_id)

@report_controller.route("/<id>", methods=["GET"])
@validate()
def get_by_id(id: str):
    id_client = request.headers.get("Client-Id")
    return service.get_by_id(id, id_client)

@report_controller.route("/ids", methods=["GET"])
@validate()
def get_all_ids():
    id_client = request.headers.get("Client-Id")
    return service.get_all_ids(id_client)

@report_controller.route("/references/ids", methods=["POST"])
@validate()
def get_references_by_ids(body: ReportIdsDTO):
    id_client = request.headers.get("Client-Id")
    return service.get_ordem_service_by_report_ids(id_client, body.ids)

@report_controller.route("/bulk", methods=["DELETE"])
@validate()
def delete_bulk(body: ReportIdsDTO):
    return service.delete_bulk(body.ids)

@report_controller.route("", methods=["POST"])
@validate()
def create(body: ReportDTO):
    app_user_id = request.headers.get("App-User-Id")
    id_client = request.headers.get("Client-Id")
    
    return service.create(body, app_user_id, id_client)


@report_controller.route("/reference", methods=["POST"])
@validate()
def create_reference(body: ReportReferenceDTO):
    id_client = request.headers.get("Client-Id")

    return service.create_reference(body, id_client)

@report_controller.route("/reference", methods=["PUT"])
@validate()
def update_reference(body: ReportReferenceDTO):
    app_user_id = request.headers.get("App-User-Id")
    id_client = request.headers.get("Client-Id")

    return service.update_reference(body, app_user_id, id_client)


@report_controller.route("/<id>", methods=["DELETE"])
@validate()
def delete(id: str):
    app_user_id = request.headers.get("App-User-Id")

    return service.delete(id, app_user_id)
