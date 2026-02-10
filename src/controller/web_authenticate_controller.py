from flask import Blueprint
from flask_pydantic import validate
from src.dto.login_dto import LoginDTO
from src.dto.web_manager_user_dto import WebManagerUserDTO
from src.service.web_authenticate_service import WebAuthenticateService


web_authenticate_controller = Blueprint("web_authenticate", __name__)
service = WebAuthenticateService()


@web_authenticate_controller.route("/login", methods=["POST"])
@validate()
def login(body: LoginDTO):
    return service.login(body)


@web_authenticate_controller.route("/register", methods=["POST"])
@validate()
def register(body: WebManagerUserDTO):
    return service.register(body)

