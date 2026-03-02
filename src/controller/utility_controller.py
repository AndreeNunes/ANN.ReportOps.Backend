from flask import Blueprint
from src.service.utility_service import UtilityService

utility_controller = Blueprint("utility", __name__)
service = UtilityService()


@utility_controller.route("/cep/<cep>", methods=["GET"])
def get_address_by_cep(cep: str):
    return service.get_address_by_cep(cep)
