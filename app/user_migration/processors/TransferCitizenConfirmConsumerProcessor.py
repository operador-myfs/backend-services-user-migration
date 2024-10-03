from datetime import datetime

from app.user_migration.services.DocumentService import DocumentService
from app.user_migration.services.NotificationService import NotificationService
from app.user_migration.services.UserService import UserService


class TransferCitizenConfirmConsumerProcessor:
    @staticmethod
    def process(message):
        user_id = message['id']
        if not UserService.validate_transfer_solicitude(user_id):
            return
        UserService.delete_user_metadata(user_id)
        DocumentService.delete_user_documents(user_id)
        NotificationService.send_notification(user_id, "CITIZEN_TRANSFERRED", datetime.now())
        return "User transferred successfully"
