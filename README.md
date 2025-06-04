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

```plaintext
POS_Simulator_Microservice/
│
├── main.py                 # FastAPI producer script to send transaction data to Kafka
├── consumer.py             # Kafka consumer script to read from topic and write to PostgreSQL
├── requirements.txt        # Python dependencies for the project
├── docker-compose.yml      # Docker config file for Kafka and Zookeeper
├── .env                    # (Optional) Environment variables (e.g., DB connection details)
├── README.md               # Project documentation
│
└── __pycache__/            # Python bytecode cache directory (auto-generated)
```

---

## 🔧 Prerequisites

- ✅ Python 3.9 or higher installed
- ✅ Docker Desktop installed and running
- ✅ PostgreSQL installed locally (PGAdmin optional)
- ✅ Git installed

---



## 📦 Project Overview

This project simulates a **real-time Point-of-Sale (POS) transaction system** using **Apache Kafka**, **FastAPI**, and **PostgreSQL**.

The goal is to mimic a real-world retail environment where transactions — specifically **gaming laptop sales** — are generated live and streamed through Kafka for downstream processing and storage.

- `main.py` uses **FastAPI** and **Faker** to generate realistic sales data, including product info, quantity, prices, and timestamps. This data is continuously sent to a Kafka topic.
- `consumer.py` acts as the Kafka **consumer**, reading each transaction from the topic and inserting it into a **PostgreSQL** database using `psycopg2`.
- The setup is modular, real-time, and container-friendly. Kafka and Zookeeper are managed through Docker, ensuring portability and ease of setup.

This system is ideal as a **proof-of-concept (POC)** for real-time data pipelines, ETL workflows, or streaming dashboards in a retail or transactional analytics context.

---


## 🐳 Kafka Setup (via Docker) and start

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
## 🚀 Running the Scripts

Once Kafka and Zookeeper are running via Docker, start the producer and consumer applications as follows:

### 🟢 1. Start the FastAPI Producer (`main.py`)

In this CMD window (`main-script`), run the FastAPI app which generates and sends transaction data to Kafka:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

This will continuously emit synthetic POS transaction events every 2 seconds (e.g., sales of gaming laptops), which are sent to the `pos-transactions` Kafka topic.


![main](https://github.com/user-attachments/assets/8317a5c2-76fa-4a64-a042-b93c1e99c807)

   ---


### 🔵 2. Start the Kafka Consumer (`consumer.py`)

In this CMD window (`consumer-script`), run the Kafka consumer which listens to the topic and inserts the data into your PostgreSQL database:

```bash
python consumer.py
```

![consumer](https://github.com/user-attachments/assets/43679fa5-85bd-4e5e-81c8-11066e895b12)


This will consume the real-time transactions from Kafka and write them into the `poc_transactions` database on `localhost:5432`, under the appropriate schema.


   ---

### 🟡 3. Verify Data in PostgreSQL

Now that the data is being inserted into PostgreSQL, you can verify it directly by querying your database.

Assuming you're using `pgAdmin` or any PostgreSQL client, connect to the following configuration:

- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `poc_transactions`
- **Password:** `******` (as per your local setup)

You can run a simple query like:

```sql
SELECT * FROM transactions;
```

![postgres_output](https://github.com/user-attachments/assets/1052d661-9829-4bbc-8b03-853187f65bba)


This should show the latest transaction records being inserted in real-time.

---

### 🖥️ Streamlit Dashboard (Live Monitoring)

This project includes a simple yet effective real-time dashboard built using **Streamlit**, which connects directly to the PostgreSQL database and displays the latest POS transactions.

#### Features:
- ⏱️ **Auto-refreshing view** every few seconds
- 🔍 **Filter** by `Product Name` or `Store ID`
- 📊 Live KPIs: Total Transactions, Revenue, Active Stores
- 🧾 Data table showing latest 100 transactions

#### To Run the Dashboard:
1. Make sure your PostgreSQL server is running and Kafka consumer is writing data.
2. Install Streamlit and dependencies (if not already):
   ```bash
   pip install streamlit psycopg2 pandas
   ```
3. Run the app:
   ```bash
   streamlit run app.py
   ```


The dashboard will open in your browser and update in real time as new transactions are inserted into the database.

![streamlit_dashboard](https://github.com/user-attachments/assets/407371e3-4923-4d69-b8a9-d48940587dbe)

---

