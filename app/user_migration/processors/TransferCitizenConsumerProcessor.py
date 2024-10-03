from datetime import datetime

from app.user_migration.services.CentralizerService import CentralizerService
from app.user_migration.services.DocumentService import DocumentService
from app.user_migration.services.NotificationService import NotificationService
from app.user_migration.services.OperatorService import OperatorService


class TransferCitizenConsumerProcessor:
    @staticmethod
    def process(message):

        user_id = message['id']
        user_name = message['citizenName']
        user_email = message['citizenEmail']
        documents = message['Documents']
        operator_confirmation_url = message['confirmationURL']

        DocumentService.save_user_documents(user_id, documents)
        CentralizerService.register_user(user_id, user_name, user_email)
        NotificationService.send_notification(user_id, "CITIZEN_RECEIVED", datetime.now())
        OperatorService.confirm_user_transaction(user_id, operator_confirmation_url)

        return "User received successfully"
