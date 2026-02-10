from flask import Blueprint, request
from flask_pydantic import validate
from src.dto.report_reference_dto import ReportReferenceDTO
from src.dto.report_dto import ReportDTO
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
    app_user_id = request.headers.get("App-User-Id")
    return service.get_by_id(id, app_user_id)

@report_controller.route("/ids", methods=["GET"])
@validate()
def get_all_ids():
    app_user_id = request.headers.get("App-User-Id")
    return service.get_all_ids(app_user_id)

@report_controller.route("", methods=["POST"])
@validate()
def create(body: ReportDTO):
    app_user_id = request.headers.get("App-User-Id")
    
    return service.create(body, app_user_id)


@report_controller.route("/reference", methods=["POST"])
@validate()
def create_reference(body: ReportReferenceDTO):
    app_user_id = request.headers.get("App-User-Id")

    print(app_user_id)
    return service.create_reference(body, app_user_id)

@report_controller.route("/reference", methods=["PUT"])
@validate()
def update_reference(body: ReportReferenceDTO):
    app_user_id = request.headers.get("App-User-Id")
    return service.update_reference(body, app_user_id)


@report_controller.route("/<id>", methods=["DELETE"])
@validate()
def delete(id: str):
    app_user_id = request.headers.get("App-User-Id")
    return service.delete(id, app_user_id)
