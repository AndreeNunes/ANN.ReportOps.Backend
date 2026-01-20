from flask import Blueprint
from flask_pydantic import validate
from src.dto.client_dto import ClientDTO, ClientCodeValidationDTO
from src.service.client_service import ClientService


client_controller = Blueprint("client", __name__)
service = ClientService()


@client_controller.route("", methods=["POST"])
@validate()
def create(body: ClientDTO):
    return service.create(body)


@client_controller.route("/validate", methods=["POST"])
@validate()
def validate_code(body: ClientCodeValidationDTO):
    return service.validate_code(body)

