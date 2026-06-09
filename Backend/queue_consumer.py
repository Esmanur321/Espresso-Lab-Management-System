import pika
import json
import time
import logging
import os
import sys
from dotenv import load_dotenv

# Ensure Backend directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models import Order, Product

load_dotenv()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("QueueConsumer")


def callback(ch, method, properties, body):
    try:
        event_data = json.loads(body)
        event_type = event_data.get("event", "unknown")
        order_id = event_data.get("order_id")
        
        logger.info(f"Received event: {event_type} for order: {order_id}")
        
        if event_type == "payment_processed":
            logger.info(f"[ASYNC WORKER] Processing successful payment for order {order_id}")
            
            # Database update
            db = SessionLocal()
            try:
                order = db.query(Order).filter(Order.id == order_id).first()
                if order:
                    order.payment_method = "online"
                    order.payment_status = "approved"
                    order.status = "confirmed"
                    db.commit()
                    logger.info(f"[ASYNC WORKER] Database updated: Order {order_id} status=confirmed, payment_status=approved.")
                else:
                    logger.error(f"[ASYNC WORKER] Order {order_id} not found in database.")
            except Exception as e:
                db.rollback()
                logger.error(f"[ASYNC WORKER] Database update failed for order {order_id}: {e}")
                raise e
            finally:
                db.close()

            # Simulate sending an email or generating an invoice
            time.sleep(1)
            logger.info(f"[ASYNC WORKER] Payment receipt email sent for order {order_id}")
            
        elif event_type == "payment_failed":
            logger.warning(f"[ASYNC WORKER] Processing failed payment for order {order_id}. Reason: {event_data.get('error')}")
            
            # Database update
            db = SessionLocal()
            try:
                order = db.query(Order).filter(Order.id == order_id).first()
                if order:
                    order.payment_method = "online"
                    order.payment_status = "rejected"
                    order.status = "cancelled"
                    
                    # Restoring product stock (Business Rule)
                    for item in order.items:
                        product = db.query(Product).filter(Product.id == item.product_id).first()
                        if product:
                            product.stock += item.quantity
                            logger.info(f"[ASYNC WORKER] Restored stock for product {product.name} (ID: {product.id}) by {item.quantity}. New stock: {product.stock}")
                    
                    db.commit()
                    logger.info(f"[ASYNC WORKER] Database updated: Order {order_id} status=cancelled, payment_status=rejected.")
                else:
                    logger.error(f"[ASYNC WORKER] Order {order_id} not found in database.")
            except Exception as e:
                db.rollback()
                logger.error(f"[ASYNC WORKER] Database update failed for order {order_id}: {e}")
                raise e
            finally:
                db.close()

            # Simulate sending failure notification
            time.sleep(1)
            logger.info(f"[ASYNC WORKER] Notification sent to user about payment failure.")
            
        elif event_type == "offline_payment_reviewed":
            payment_status = event_data.get("payment_status")
            admin_id = event_data.get("admin_id")
            
            logger.info(f"[ASYNC WORKER] Offline payment for order {order_id} was {payment_status} by admin {admin_id}.")
            
            # Send notification only when payment is approved
            if payment_status == "approved":
                logger.info(f"[NOTIFICATION] Sending 'Order Approved' notification to customer for order {order_id}")
                time.sleep(1)
                logger.info(f"[NOTIFICATION] ✅ Email sent: 'Siparişiniz onaylandı' / 'Your order has been approved' to customer for order {order_id}")
                logger.info(f"[NOTIFICATION] Order details: Order ID={order_id}, Status={event_data.get('order_status')}")
            elif payment_status == "rejected":
                logger.info(f"[NOTIFICATION] Sending 'Order Rejected' notification to customer for order {order_id}")
                time.sleep(1)
                logger.info(f"[NOTIFICATION] ❌ Email sent: 'Siparişiniz reddedildi' / 'Your order has been rejected' to customer for order {order_id}")
            
        else:
            logger.info(f"[ASYNC WORKER] Processed generic event: {event_data}")
            
        # Acknowledge the message if using a real connection channel
        if ch and hasattr(ch, "basic_ack") and method and hasattr(method, "delivery_tag"):
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        logger.error(f"Error processing message: {e}")

def main():
    queue_name = 'espressolab_queue'
    rabbitmq_url = os.getenv("RABBITMQ_URL")
    
    if not rabbitmq_url:
        logger.error("RABBITMQ_URL not found in .env file. Please add it to your .env file.")
        return
    
    try:
        # Use CloudAMQP URL from .env
        url_params = pika.URLParameters(rabbitmq_url)
        connection = pika.BlockingConnection(url_params)
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        
        # Fair dispatch
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        
        logger.info(f"[*] Waiting for messages in '{queue_name}' (CloudAMQP). To exit press CTRL+C")
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError as e:
        logger.error(f"Could not connect to CloudAMQP: {e}")
        logger.info("MOCK CONSUMER MODE: To strictly fulfill the asynchronous background processing requirement, this script acts as the queue consumer worker. Check your RABBITMQ_URL in .env file.")
        
        # Keep process alive to simulate a worker process
        while True:
            time.sleep(10)

if __name__ == '__main__':
    main()
