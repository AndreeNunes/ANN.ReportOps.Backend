from flask import Blueprint, request, g
from flask_pydantic import validate
from src.dto.report_reference_dto import ReportReferenceDTO
from src.dto.report_dto import ReportDTO
from src.dto.report_ids_dto import ReportIdsDTO
from src.dto.report_sync_dto import ReportSyncDTO
from src.service.report_service import ReportService
from src.decorators.web_jwt_required import web_jwt_required

report_controller = Blueprint("report", __name__)
service = ReportService()


@report_controller.route("", methods=["GET"])
@web_jwt_required
@validate()
def get_all():
    return service.get_all(g.web_jwt_payload.get("app_user_id"))

@report_controller.route("/<id>", methods=["GET"])
@web_jwt_required
@validate()
def get_by_id(id: str):
    return service.get_by_id(id, g.web_client_id)

@report_controller.route("/ids", methods=["GET"])
@web_jwt_required
@validate()
def get_all_ids():
    return service.get_all_ids(g.web_client_id)

@report_controller.route("/references/ids", methods=["POST"])
@web_jwt_required
@validate()
def get_references_by_ids(body: ReportIdsDTO):
    return service.get_ordem_service_by_report_ids(g.web_client_id, body.ids)

@report_controller.route("/bulk", methods=["DELETE"])
@web_jwt_required
@validate()
def delete_bulk(body: ReportIdsDTO):
    return service.delete_bulk(
        body.ids,
        g.web_client_id,
        confirm_media_deletion=body.confirm_media_deletion,
    )

@report_controller.route("", methods=["POST"])
@web_jwt_required
@validate()
def create(body: ReportDTO):
    return service.create(body, g.web_jwt_payload.get("app_user_id"), g.web_client_id)


@report_controller.route("/reference", methods=["POST"])
@web_jwt_required
@validate()
def create_reference(body: ReportReferenceDTO):
    return service.create_reference(body, g.web_client_id)

@report_controller.route("/reference", methods=["PUT"])
@web_jwt_required
@validate()
def update_reference(body: ReportReferenceDTO):
    return service.update_reference(body, g.web_jwt_payload.get("app_user_id"), g.web_client_id)


@report_controller.route("/<id>", methods=["DELETE"])
@web_jwt_required
@validate()
def delete(id: str):
    return service.delete_bulk([id], g.web_client_id)


@report_controller.route("/get-sync", methods=["POST"])
@web_jwt_required
@validate()
def get_report_sync(body: ReportSyncDTO):
    return service.get_report_sync(body, g.web_client_id)


@report_controller.route("/needs/<reference_id>/sync", methods=["GET"])
@web_jwt_required
def get_needs_assessment_sync(reference_id: str):
    return service.get_needs_assessment_sync(reference_id, g.web_client_id)


@report_controller.route("/orders/<id>/web", methods=["GET"])
@web_jwt_required
def get_ordem_by_id_web(id: str):
    return service.get_ordem_service_by_id(id)

@report_controller.route("/web/<id>", methods=["DELETE"])
@web_jwt_required
def delete_report_web(id: str):
    return service.delete_web(id, g.web_client_id)

@report_controller.route("/orders/web", methods=["GET"])
@web_jwt_required
def get_orders():
    return service.get_orders(g.web_client_id)

@report_controller.route("/dashboard/web", methods=["GET"])
@web_jwt_required
def get_dashboard():
    return service.get_dashboard(g.web_client_id)

@report_controller.route("/web", methods=["POST"])
@web_jwt_required
@validate()
def create_report_web(body: ReportDTO):
    return service.create(body, "", g.web_client_id)

@report_controller.route("/reference/web", methods=["POST"])
@web_jwt_required
@validate()
def create_reference_web(body: ReportReferenceDTO):
    return service.create_reference(body, g.web_client_id)


@report_controller.route("/reference/web", methods=["PUT"])
@web_jwt_required
@validate()
def update_reference_web(body: ReportReferenceDTO):
    return service.update_reference(body, "", g.web_client_id)



