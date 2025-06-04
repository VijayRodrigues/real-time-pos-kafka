from fastapi import FastAPI
from kafka import KafkaProducer
from faker import Faker
from uuid import uuid4
import json
import random
import time
import threading

app = FastAPI()
fake = Faker()

# Kafka Configuration
producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

TOPIC_NAME = "pos-transactions"

brands_models = {
    "Asus": ["ROG Strix G15", "TUF Gaming F15"],
    "MSI": ["Katana GF66", "Pulse GL76"],
    "Dell": ["Alienware M15", "G16 Gaming"],
    "HP": ["OMEN 16", "Victus 15"],
    "Lenovo": ["Legion 5 Pro", "LOQ 15IRH"]
}

gpus = ["NVIDIA RTX 4060", "NVIDIA RTX 4070", "NVIDIA RTX 4080"]
cpus = ["Intel i7-12700H", "AMD Ryzen 7 6800H", "Intel i9-12900HK"]
oss = ["Windows 11", "Ubuntu Linux"]
screen_sizes = [15.6, 16.0, 17.3]

# Pre-generated list of 100 realistic gaming laptops
products = []
for _ in range(100):
    brand = random.choice(list(brands_models.keys()))
    model = random.choice(brands_models[brand])
    product = {
        "product_id": str(uuid4()),
        "product_name": f"{brand} {model}",
        "brand": brand,
        "model_name": model,
        "gpu": random.choice(gpus),
        "cpu": random.choice(cpus),
        "ram_gb": random.choice([16, 32, 64]),
        "storage_gb": random.choice([512, 1024, 2048]),
        "screen_size": random.choice(screen_sizes),
        "os": random.choice(oss),
        "price": round(random.uniform(900.0, 2500.0), 2),
        "warranty_years": random.choice([1, 2, 3]),
        "in_stock": random.randint(10, 300),
        "created_at": fake.iso8601()
    }
    products.append(product)

def generate_transaction():
    product = random.choice(products)
    quantity = random.randint(1, 3)
    unit_price = product["price"]
    transaction = {
        "transaction_id": str(uuid4()),
        "product_id": product["product_id"],
        "product_name": product["product_name"],
        "brand": product["brand"],
        "model_name": product["model_name"],
        "gpu": product["gpu"],
        "cpu": product["cpu"],
        "ram_gb": product["ram_gb"],
        "storage_gb": product["storage_gb"],
        "screen_size": product["screen_size"],
        "os": product["os"],
        "quantity": quantity,
        "unit_price": unit_price,
        "total_amount": round(unit_price * quantity, 2),
        "warranty_years": product["warranty_years"],
        "store_id": fake.random_int(min=1, max=10),
        "timestamp": fake.iso8601(),
        "purchase_channel": random.choice(["Online", "In-store"]),
        "buyer_name": fake.name(),
        "email": fake.email(),
        "location": fake.city()
    }
    return transaction

def start_producing():
    while True:
        data = generate_transaction()
        producer.send(TOPIC_NAME, value=data)
        print(f"Produced -> {data}")
        time.sleep(2)

@app.on_event("startup")
def startup_event():
    print("🚀 POS Gaming Laptop Simulator started...")
    thread = threading.Thread(target=start_producing, daemon=True)
    thread.start()

@app.get("/")
def root():
    return {"status": "Gaming Laptop POS Simulator is running and sending data to Kafka"}
