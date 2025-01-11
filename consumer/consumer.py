import pika
import json
from pymongo import MongoClient

# RabbitMQ und MongoDB Verbindungen
rabbitmq_host = "rabbitmq"
queue_name = "AAPL"
mongo_host = "mongodb://mongodb:27017/"
db_name = "stockmarket"
collection_name = "stocks"

def calculate_average(data):
    prices = [item['price'] for item in data]
    return sum(prices) / len(prices)

# Verbindung zu RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
channel = connection.channel()
channel.queue_declare(queue=queue_name)

# Verbindung zu MongoDB
client = MongoClient(mongo_host)
db = client[db_name]
collection = db[collection_name]

def callback(ch, method, properties, body):
    messages = json.loads(body)
    avg_price = calculate_average(messages)
    result = {
        "company": queue_name,
        "avgPrice": avg_price
    }
    collection.insert_one(result)
    print(f"Verarbeitet: {len(messages)} Nachrichten.")

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
print(f"Warte auf Nachrichten in {queue_name}")
channel.start_consuming()
