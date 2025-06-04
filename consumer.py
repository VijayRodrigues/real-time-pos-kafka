import json
import psycopg2
from kafka import KafkaConsumer

# PostgreSQL connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="poc_transactions",
    user="postgres",
    password="********"
)
cursor = conn.cursor()

# Kafka Consumer
consumer = KafkaConsumer(
    "pos-transactions",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="earliest",
    enable_auto_commit=True,
    group_id="pos-consumer-group",
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("✅ Consumer started. Listening to Kafka topic and writing to PostgreSQL...")

for message in consumer:
    try:
        data = message.value
        print("📥 Received:", data)

        insert_query = """
            INSERT INTO transactions (
                transaction_id, product_id, product_name, brand, model_name,
                cpu, gpu, ram_gb, storage_gb, screen_size, os,
                quantity, unit_price, total_amount,
                warranty_years, store_id, timestamp,
                purchase_channel, buyer_name, email, location
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        cursor.execute(insert_query, (
            data['transaction_id'],
            data['product_id'],
            data['product_name'],
            data['brand'],
            data['model_name'],
            data['cpu'],
            data['gpu'],
            data['ram_gb'],
            data['storage_gb'],
            data['screen_size'],
            data['os'],
            data['quantity'],
            data['unit_price'],
            data['total_amount'],
            data['warranty_years'],
            data['store_id'],
            data['timestamp'],
            data['purchase_channel'],
            data['buyer_name'],
            data['email'],
            data['location']
        ))

        conn.commit()
        print("✅ Inserted into DB.\n")

    except (json.JSONDecodeError, KeyError) as e:
        print("❌ JSON Parse Error:", e)
    except psycopg2.Error as e:
        print("❌ DB Insert Error:", e)
        conn.rollback()
