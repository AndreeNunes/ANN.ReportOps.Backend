from flask import Blueprint, g, request
from flask_pydantic import validate

from src.decorators.web_jwt_required import web_jwt_required
from src.dto.company_dto import CompanyDTO
from src.dto.company_contact_dto import (
    CompanyContactDTO,
    CompanyContactSignatureCompleteDTO,
    CompanyContactSignatureDTO,
)
from src.service.company_service import CompanyService
from src.service.company_contact_service import CompanyContactService

company_controller = Blueprint("company", __name__)
service = CompanyService()
contact_service = CompanyContactService()


@company_controller.route("", methods=["GET"])
def get_all():
    id_client = request.headers.get("Client-Id") or ""
    return service.get_all(id_client)


@company_controller.route("/web", methods=["GET"])
@web_jwt_required
def get_all_web():
    return service.get_all(g.web_client_id)


@company_controller.route("", methods=["POST"])
@validate()
def create(body: CompanyDTO):
    id_client = request.headers.get("Client-Id") or ""

    return service.create(body, id_client)


@company_controller.route("/web", methods=["POST"])
@web_jwt_required
@validate()
def create_web(body: CompanyDTO):
    return service.create(body, g.web_client_id)


@company_controller.route("/<id>", methods=["PUT"])
@validate()
def update(id: str, body: CompanyDTO):
    id_client = request.headers.get("Client-Id") or ""
    return service.update(id, body, id_client)


@company_controller.route("/web/<id>", methods=["PUT"])
@web_jwt_required
@validate()
def update_web(id: str, body: CompanyDTO):
    return service.update(id, body, g.web_client_id)


@company_controller.route("/<id>", methods=["DELETE"])
def delete(id: str):
    id_client = request.headers.get("Client-Id") or ""
    return service.delete(id, id_client)


@company_controller.route("/web/<id>", methods=["DELETE"])
@web_jwt_required
def delete_web(id: str):
    return service.delete(id, g.web_client_id)

@company_controller.route("/web/to-equipament", methods=["GET"])
@web_jwt_required
def get_to_equipament():
    return service.get_to_equipament(g.web_client_id)


@company_controller.route("/<company_id>/contacts", methods=["GET"])
def get_contacts(company_id: str):
    return contact_service.get_all(company_id, request.headers.get("Client-Id") or "")


@company_controller.route("/<company_id>/contacts", methods=["POST"])
@validate()
def upsert_contact(company_id: str, body: CompanyContactDTO):
    return contact_service.upsert(company_id, body, request.headers.get("Client-Id") or "")


@company_controller.route("/<company_id>/contacts/<contact_id>", methods=["PUT"])
@validate()
def update_contact(company_id: str, contact_id: str, body: CompanyContactDTO):
    body.id = contact_id
    return contact_service.upsert(company_id, body, request.headers.get("Client-Id") or "")


@company_controller.route("/<company_id>/contacts/<contact_id>", methods=["DELETE"])
def delete_contact(company_id: str, contact_id: str):
    return contact_service.delete(company_id, contact_id, request.headers.get("Client-Id") or "")


@company_controller.route("/<company_id>/contacts/<contact_id>/signature/upload-url", methods=["POST"])
@validate()
def contact_signature_upload_url(company_id: str, contact_id: str, body: CompanyContactSignatureDTO):
    return contact_service.get_signature_upload_url(
        company_id, contact_id, body, request.headers.get("Client-Id") or ""
    )


@company_controller.route("/<company_id>/contacts/<contact_id>/signature/complete", methods=["PUT"])
@validate()
def complete_contact_signature(company_id: str, contact_id: str, body: CompanyContactSignatureCompleteDTO):
    return contact_service.complete_signature(
        company_id, contact_id, body, request.headers.get("Client-Id") or ""
    )
