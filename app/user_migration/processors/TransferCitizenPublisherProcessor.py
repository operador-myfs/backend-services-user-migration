from app.user_migration.services.QueueService import QueueService


class TransferCitizenPublisherProcessor:
    @staticmethod
    def process(message):
        QueueService.publish_message(message, "TRANSFER_CITIZEN")
        return "User transaction received successfully"
