import json
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# We import pika, but if it fails (not installed or no server), we fallback to a mock so the app doesn't crash
try:
    import pika
    HAS_PIKA = True
except ImportError:
    HAS_PIKA = False

logger = logging.getLogger(__name__)

class QueueService:
    def __init__(self, queue_name="espressolab_queue"):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        
        if HAS_PIKA:
            try:
                # Read RabbitMQ URL from .env file
                rabbitmq_url = os.getenv("RABBITMQ_URL")
                if not rabbitmq_url:
                    logger.warning("RABBITMQ_URL not found in .env file. Falling back to Mock Queue.")
                    return
                
                # Use CloudAMQP URL from .env
                url_params = pika.URLParameters(rabbitmq_url)
                self.connection = pika.BlockingConnection(url_params)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queue_name, durable=True)
                logger.info(f"Connected to RabbitMQ (CloudAMQP) on queue: {self.queue_name}")
            except Exception as e:
                logger.warning(f"Could not connect to RabbitMQ: {e}. Falling back to Mock Queue.")
                self.connection = None

    def publish_message(self, message: dict):
        """Publish a message to the queue (e.g. payment success)"""
        if self.connection and self.channel:
            try:
                self.channel.basic_publish(
                    exchange='',
                    routing_key=self.queue_name,
                    body=json.dumps(message),
                    properties=pika.BasicProperties(
                        delivery_mode=2,  # make message persistent
                    )
                )
                logger.info(f"Message published to RabbitMQ: {message}")
                return True
            except Exception as e:
                logger.error(f"Failed to publish message: {e}")
        
        # MOCK BEHAVIOR
        logger.info(f"[MOCK QUEUE] Message placed in queue '{self.queue_name}': {message}")
        return True

# Singleton instance
queue_service = QueueService()
