from flask import Blueprint, g, request
from flask_pydantic import validate

from src.decorators.web_jwt_required import web_jwt_required
from src.dto.company_dto import CompanyDTO
from src.service.company_service import CompanyService

company_controller = Blueprint("company", __name__)
service = CompanyService()


@company_controller.route("", methods=["GET"])
@validate()
def get_all():
    id_client = request.headers.get("Client-Id")
    return service.get_all(id_client)

@company_controller.route("/web", methods=["GET"])
@web_jwt_required
@validate()
def get_all_web():
    return service.get_all(g.web_client_id)

@company_controller.route("", methods=["POST"])
@validate()
def create(body: CompanyDTO):
    id_client = request.headers.get("Client-Id")

    return service.create(body, id_client)


@company_controller.route("/<id>", methods=["PUT"])
@validate()
def update(id: str, body: CompanyDTO):
    id_client = request.headers.get("Client-Id")
    return service.update(id, body, id_client)


@company_controller.route("/<id>", methods=["DELETE"])
@validate()
def delete(id: str):
    id_client = request.headers.get("Client-Id")
    return service.delete(id, id_client)
