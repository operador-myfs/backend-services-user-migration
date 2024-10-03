from http import HTTPStatus

from flask import Blueprint, request, jsonify

from app.user_migration.processors.TransferCitizenConfirmPublisherProcessor import TransferCitizenConfirmPublisherProcessor
from app.user_migration.processors.TransferCitizenPublisherProcessor import TransferCitizenPublisherProcessor

user_migration = Blueprint("user_migration", __name__)


@user_migration.route("/transferCitizen", methods=["POST"])
def transfer_citizen_publisher():
    try:
        return jsonify(TransferCitizenPublisherProcessor.process(request.json)), HTTPStatus.OK
    except Exception as e:
        return jsonify(
            error=f"An error occurred while publishing transfer notification. {e}"), HTTPStatus.INTERNAL_SERVER_ERROR


@user_migration.route("/transferCitizenConfirm", methods=["POST"])
def transfer_citizen_confirm_publisher():
    try:

        return jsonify(TransferCitizenConfirmPublisherProcessor.process(request.json)), HTTPStatus.OK
    except Exception as e:
        return jsonify(error=f"An error occurred while publishing transfer confirm notification. {e}"), HTTPStatus.INTERNAL_SERVER_ERROR
