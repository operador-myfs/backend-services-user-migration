from app.user_migration.services.QueueService import QueueService


class TransferCitizenConfirmPublisherProcessor:
    @staticmethod
    def process(message):
        QueueService.publish_message(message, "CONFIRM_TRANSFER")
        return "Confirmation received successfully"
