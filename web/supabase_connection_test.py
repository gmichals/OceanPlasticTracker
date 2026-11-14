import streamlit as st
import httpx

st.title("Supabase Connection Test")

url = st.secrets["SUPABASE_URL"].rstrip("/") + "/rest/v1/"

try:
    response = httpx.get(url, timeout=10)
    st.success(f"HTTP status: {response.status_code}")
    st.write("Supabase API responded.")
except Exception as exc:
    st.error(f"Connection failed: {type(exc).__name__}")
