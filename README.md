# 💸 Real-Time POS Transactions Monitoring System

This project simulates real-time Point-of-Sale (POS) transactions using **FastAPI**, **Apache Kafka**, and **PostgreSQL**. It demonstrates a real-time data ingestion pipeline for retail transactions, ideal for portfolios and learning.

---

## 🚀 Tech Stack

- **Python 3.9+**
- **FastAPI**
- **Apache Kafka** (via Docker)
- **PostgreSQL + pgAdmin**
- **Kafka-Python**
- **Faker (Synthetic Data)**
- **Uvicorn**

---

## 📁 Project Structure




---

## 🔧 Prerequisites

- ✅ Python 3.9 or higher installed
- ✅ Docker Desktop installed and running
- ✅ PostgreSQL installed locally (PGAdmin optional)
- ✅ Git installed

---




## 🐳 Kafka Setup (via Docker)

To set up Kafka and Zookeeper using Docker:

1. **Prepare the Docker Compose File**  
   Ensure you have the YAML configuration saved.  
   Example path used: `F:\kafka-docker`

2. **Start Kafka and Zookeeper**  
   Navigate to the directory and run:  
   &nbsp;&nbsp;&nbsp;&nbsp;`docker-compose up -d`

3. **Verify Running Containers**  
   Check that the containers are running:  
   &nbsp;&nbsp;&nbsp;&nbsp;`docker ps`

4. **Confirm Kafka is Running on Port 9092**  
   Run the following to confirm:  
   &nbsp;&nbsp;&nbsp;&nbsp;`netstat -aon | findstr :9092`

5. **List Kafka Topics**  
   Use the container name (in this case, `kafka-docker-kafka-1`) to list topics:  
   &nbsp;&nbsp;&nbsp;&nbsp;`docker exec -it kafka-docker-kafka-1 kafka-topics --bootstrap-server localhost:9092 --list`

6. **(Optional) Create a Kafka Topic**  
   If your topic isn’t created yet:  
   &nbsp;&nbsp;&nbsp;&nbsp;`docker exec -it kafka-docker-kafka-1 kafka-topics --create --topic pos-transactions --bootstrap-server localhost:9092 --partitions 1 --replication-factor 1`


![docker_start](https://github.com/user-attachments/assets/e1b4ef85-8d2f-4ec7-9231-d4ed107658d1)


   ---
