import streamlit as st
import httpx
from urllib.parse import urlparse

st.title("Supabase Connection Test")

url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
host = urlparse(url).hostname

st.write("Configured hostname:", host)
st.write("Expected hostname:", "aqwyzpkfxozyrmrvilzt.supabase.co")

try:
    response = httpx.get(
        url + "/rest/v1/",
        timeout=15,
        trust_env=False,
    )
    st.success(f"HTTP status: {response.status_code}")
except httpx.ConnectError as exc:
    st.error("Connection failed: ConnectError")
    st.write("Underlying error type:",
             type(exc.__cause__).__name__ if exc.__cause__ else "Unknown")
except Exception as exc:
    st.error(f"Connection failed: {type(exc).__name__}")
