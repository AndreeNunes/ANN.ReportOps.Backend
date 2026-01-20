from flask import Blueprint
from flask_pydantic import validate
from src.dto.login_dto import LoginDTO
from src.service.authenticate_service import AuthenticateService
from src.dto.app_user_dto import AppUserDTO
from src.dto.client_dto import ClientCodeValidationDTO

authenticate_controller = Blueprint("authenticate", __name__)
service = AuthenticateService()


@authenticate_controller.route("/login", methods=["POST"])
@validate()
def login(body: LoginDTO):
    return service.login(body)


@authenticate_controller.route("/register", methods=["POST"])
@validate()
def register(body: AppUserDTO):
    return service.register(body)


@authenticate_controller.route("/validate-code", methods=["POST"])
@validate()
def validate_code(body: ClientCodeValidationDTO):
    return service.validate_user_code(body)
