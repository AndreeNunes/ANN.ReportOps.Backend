from flask import Blueprint, request
from flask_pydantic import validate
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