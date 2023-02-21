import streamlit as st
from google.oauth2 import service_account
from google.cloud import bigquery

# Create API client.
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
client = bigquery.Client(credentials=credentials)

# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 100 min.
@st.cache_data(ttl=600)
def run_query(query):
    query_job = client.query(query)
    rows_raw = query_job.result()
    # Convert to list of dicts. Required for st.cache_data to hash the return value.
    rows = [dict(row) for row in rows_raw]
    return rows

def new_ID(ID, height, weigth):
    query = f"INSERT INTO `foode-376420.foodE.ID_info` (UserID, Height, Weigth) VALUES ({ID}, {height}, {weigth})"
    rows = run_query(query)
    return rows

def exist_ID(ID):
    query = f"SELECT EXISTS( SELECT * FROM `foodE.ID_info` WHERE UserID={ID} )"
    rows = run_query(query)
    return rows

def ID_update_height(ID, height):
    query = f"UPDATE `foodE.ID_info` SET Height = {height} WHERE UserID={ID}"
    rows = run_query(query)
    return rows

def ID_update_weigth(ID, weigth):
    query = f"UPDATE `foodE.ID_info` SET Weight = {weigth} WHERE UserID={ID}"
    rows = run_query(query)
    return rows

def ID_update_weigth_height(ID, weigth, height ):
    query = f"UPDATE `foodE.ID_info` SET Weigth = {weigth}, Height = {height} WHERE UserID={ID}"
    rows = run_query(query)
    return rows
