from flask import Blueprint, g
from flask_pydantic import validate

from src.decorators.web_jwt_required import web_jwt_required
from src.dto.equipament_dto import EquipamentDTO
from src.service.equipament_service import EquipamentService

equipament_controller = Blueprint("equipament", __name__)
service = EquipamentService()


@equipament_controller.route("/<company_id>", methods=["GET"])
@validate()
def get_all(company_id: str):
    return service.get_all(company_id)


@equipament_controller.route("/<company_id>", methods=["POST"])
@validate()
def create(body: EquipamentDTO, company_id: str):
    return service.create(body, company_id)


@equipament_controller.route("/<company_id>", methods=["PUT"])
@validate()
def update(body: EquipamentDTO, company_id: str):
    return service.update(body, company_id)


@equipament_controller.route("/<company_id>/<id>", methods=["DELETE"])
@validate()
def delete(company_id: str, id: str):
    return service.delete(id, company_id)


@equipament_controller.route("/web", methods=["GET"])
@web_jwt_required
def get_all_client_id():
    return service.get_all_by_client(g.web_client_id)


@equipament_controller.route("/web/<id>", methods=["GET"])
@web_jwt_required
def get_client_id_by_id(id: str):
    return service.get_by_id_with_out_company(id)

@equipament_controller.route("/web/<id>", methods=["POST"])
@web_jwt_required
@validate()
def create_web(body: EquipamentDTO, id: str):
    return service.create(body, id)

@equipament_controller.route("/web/<id>", methods=["PUT"])
@web_jwt_required
@validate()
def update_web(body: EquipamentDTO, id: str):
    return service.update(body, id)

@equipament_controller.route("/web/<company_id>/<id>", methods=["DELETE"])
@web_jwt_required
def delete_web(company_id: str, id: str):
    return service.delete(id, company_id)
