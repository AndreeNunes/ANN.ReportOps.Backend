from flask import Blueprint, g, request
from flask_pydantic import validate

from src.decorators.web_jwt_required import web_jwt_required
from src.dto.company_dto import CompanyDTO
from src.service.company_service import CompanyService

company_controller = Blueprint("company", __name__)
service = CompanyService()


@company_controller.route("", methods=["GET"])
def get_all():
    id_client = request.headers.get("Client-Id") or ""
    return service.get_all(id_client)


@company_controller.route("/web", methods=["GET"])
@web_jwt_required
def get_all_web():
    return service.get_all(g.web_client_id)


@company_controller.route("", methods=["POST"])
@validate()
def create(body: CompanyDTO):
    id_client = request.headers.get("Client-Id") or ""

    return service.create(body, id_client)


@company_controller.route("/web", methods=["POST"])
@web_jwt_required
@validate()
def create_web(body: CompanyDTO):
    return service.create(body, g.web_client_id)


@company_controller.route("/<id>", methods=["PUT"])
@validate()
def update(id: str, body: CompanyDTO):
    id_client = request.headers.get("Client-Id") or ""
    return service.update(id, body, id_client)


@company_controller.route("/web/<id>", methods=["PUT"])
@web_jwt_required
@validate()
def update_web(id: str, body: CompanyDTO):
    return service.update(id, body, g.web_client_id)


@company_controller.route("/<id>", methods=["DELETE"])
def delete(id: str):
    id_client = request.headers.get("Client-Id") or ""
    return service.delete(id, id_client)


@company_controller.route("/web/<id>", methods=["DELETE"])
@web_jwt_required
def delete_web(id: str):
    return service.delete(id, g.web_client_id)

@company_controller.route("/web/to-equipament", methods=["GET"])
@web_jwt_required
def get_to_equipament():
    return service.get_to_equipament(g.web_client_id)
