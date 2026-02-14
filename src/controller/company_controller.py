from flask import Blueprint, request
from flask_pydantic import validate
from src.dto.company_dto import CompanyDTO
from src.service.company_service import CompanyService

company_controller = Blueprint("company", __name__)
service = CompanyService()


@company_controller.route("", methods=["GET"])
@validate()
def get_all():
    id_client = request.headers.get("Client-Id")
    return service.get_all(id_client)


@company_controller.route("", methods=["POST"])
@validate()
def create(body: CompanyDTO):
    id_client = request.headers.get("Client-Id")

    return service.create(body, id_client)


@company_controller.route("/<id>", methods=["DELETE"])
@validate()
def delete(id: str):
    id_client = request.headers.get("Client-Id")
    return service.delete(id, id_client)
