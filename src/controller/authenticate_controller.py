from flask import Blueprint
from flask_pydantic import validate
from src.dto.login_dto import LoginDTO
from src.service.authenticate_service import AuthenticateService
from src.dto.app_user_dto import AppUserDTO

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
