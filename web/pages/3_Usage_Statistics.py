import hmac
import pandas as pd
import streamlit as st
from supabase import create_client

st.title("Ocean Plastic Tracker — Usage Statistics")

def check_password():
    expected = st.secrets["ANALYTICS_ADMIN_PASSWORD"]

    if st.session_state.get("analytics_admin_authenticated", False):
        return True

    password = st.text_input(
        "Administrator password",
        type="password",
        key="analytics_admin_password_input",
    )

    if st.button("Sign in"):
        if hmac.compare_digest(password, expected):
            st.session_state["analytics_admin_authenticated"] = True
            st.rerun()
        else:
            st.error("Incorrect password.")

    return False

if not check_password():
    st.stop()

if st.button("Sign out"):
    st.session_state["analytics_admin_authenticated"] = False
    st.rerun()

@st.cache_data(ttl=300, show_spinner=False)
def load_events():
    client = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_SECRET_KEY"],
    )

    events = []
    offset = 0

    while True:
        result = (
            client.table("trajectory_events")
            .select("created_at,river,event_type,session_id")
            .order("created_at", desc=True)
            .range(offset, offset + 999)
            .execute()
        )

        batch = result.data or []
        events.extend(batch)

        if len(batch) < 1000:
            break

        offset += 1000

    return events

try:
    events = load_events()
except Exception:
    st.error("Unable to retrieve analytics from Supabase.")
    st.stop()

if not events:
    st.info("No trajectory events have been recorded yet.")
    st.stop()

df = pd.DataFrame(events)
df["created_at"] = pd.to_datetime(df["created_at"], utc=True)
df["date"] = df["created_at"].dt.date

a, b, c = st.columns(3)
a.metric("Trajectory events", len(df))
b.metric("Unique sessions", df["session_id"].nunique())
c.metric("Rivers explored", df["river"].nunique())

st.caption(
    "Trajectory events include river selections and new-particle requests. "
    "Unique sessions are not necessarily unique visitors."
)

st.subheader("Events by type")
st.bar_chart(df["event_type"].value_counts())

st.subheader("Most popular rivers")
st.bar_chart(df["river"].value_counts())

st.subheader("Daily activity (UTC)")
daily = df.groupby("date").size().rename("Events")
st.line_chart(daily)

st.subheader("Recent trajectory requests")
st.dataframe(
    df[["created_at", "river", "event_type"]].head(100),
    hide_index=True,
)

if st.button("Refresh statistics"):
    load_events.clear()
    st.rerun()
