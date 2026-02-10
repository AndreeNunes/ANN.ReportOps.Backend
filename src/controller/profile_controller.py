from flask import Blueprint, request
from flask_pydantic import validate
from src.service.profile_service import ProfileService


profile_controller = Blueprint("profile", __name__)
service = ProfileService()


@profile_controller.route("", methods=["GET"])
@validate()
def get_profile():
    app_user_id = request.headers.get("App-User-Id")
    return service.get_profile(app_user_id)

