import streamlit as st
import psycopg2
import pandas as pd
import time

# PostgreSQL connection details
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "poc_transactions"
DB_USER = "postgres"
DB_PASSWORD = "********"

# Connect to PostgreSQL
@st.cache_resource
def get_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def fetch_data(conn, product=None, store=None):
    query = "SELECT * FROM transactions"
    conditions = []
    if product:
        conditions.append(f"product_name = '{product}'")
    if store:
        conditions.append(f"store_id = {store}")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY timestamp DESC LIMIT 100"
    return pd.read_sql(query, conn)

# Streamlit App UI
st.set_page_config(page_title="POS Transactions Dashboard", layout="wide")
st.title("🛒 Real-Time POS Transactions Dashboard")

conn = get_connection()

# Load filter values
df_all = fetch_data(conn)
product_options = sorted(df_all["product_name"].dropna().unique())
store_options = sorted(df_all["store_id"].dropna().unique())

# Sidebar filters
st.sidebar.header("Filter Transactions")
selected_product = st.sidebar.selectbox("Product Name", ["All"] + list(product_options))
selected_store = st.sidebar.selectbox("Store ID", ["All"] + list(map(str, store_options)))

# Auto-refresh interval
refresh_sec = st.sidebar.slider("Auto-refresh every (seconds)", 5, 60, 10)

# Apply filters
product_filter = selected_product if selected_product != "All" else None
store_filter = int(selected_store) if selected_store != "All" else None

# Auto-refresh every N seconds
placeholder = st.empty()

while True:
    with placeholder.container():
        st.subheader("📦 Latest Transactions")

        data = fetch_data(conn, product_filter, store_filter)

        st.dataframe(data, use_container_width=True)

        # Optional: Show KPIs
        col1, col2, col3 = st.columns(3)
        col1.metric("🔄 Total Transactions", len(data))
        col2.metric("💰 Total Revenue", f"${data['total_amount'].sum():,.2f}")
        col3.metric("🏬 Stores Active", data['store_id'].nunique())

    time.sleep(refresh_sec)
