import uuid
import streamlit as st
from supabase import create_client


@st.cache_resource(show_spinner=False)
def _database(url, key):
    return create_client(url, key)


def record_trajectory(river, event_type):
    """Record a trajectory request without interrupting the tracker."""
    if event_type not in ("river_selected", "new_particle"):
        return False

    try:
        if "analytics_session_id" not in st.session_state:
            st.session_state.analytics_session_id = str(uuid.uuid4())

        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_SECRET_KEY"]

        _database(url, key).table("trajectory_events").insert({
            "river": river,
            "event_type": event_type,
            "session_id": st.session_state.analytics_session_id,
        }).execute()

        return True

    except Exception as exc:
        # Log only the exception class, never credentials or request details.
        import logging
        logging.warning(
            "Analytics event failed: %s",
            type(exc).__name__
        )
        return False
