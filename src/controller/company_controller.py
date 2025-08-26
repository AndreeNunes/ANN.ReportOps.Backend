from flask import Blueprint, request
from flask_pydantic import validate
from src.dto.company_dto import CompanyDTO
from src.service.company_service import CompanyService

company_controller = Blueprint("company", __name__)
service = CompanyService()


@company_controller.route("", methods=["GET"])
@validate()
def get_all():
    client_id = request.headers.get("Client-Id")
    return service.get_all(client_id)


@company_controller.route("", methods=["POST"])
@validate()
def create(body: CompanyDTO):
    client_id = request.headers.get("Client-Id")

    print(client_id)
    return service.create(body, client_id)


@company_controller.route("/<id>", methods=["DELETE"])
@validate()
def delete(id: str):
    client_id = request.headers.get("Client-Id")
    return service.delete(id, client_id)
