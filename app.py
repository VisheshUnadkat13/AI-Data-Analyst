import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# -----------------------------------------------------
# Page Configuration
# -----------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------
# Session State Initialization
# -----------------------------------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# -----------------------------------------------------
# Sidebar
# -----------------------------------------------------

with st.sidebar:
    st.title("📊 AI Data Analyst")

    st.markdown("---")

    st.subheader("Project Status")

    st.success("Phase 1")

    st.markdown(
        """
        **Upcoming Features**

        - CSV Upload
        - Natural Language Q&A
        - Charts
        - SQL Generation
        - Business Insights
        - Anomaly Detection
        """
    )

# -----------------------------------------------------
# Main Page
# -----------------------------------------------------

st.title("📊 AI Data Analyst")

st.write(
    """
Welcome!

This application allows you to upload one or more CSV files and analyze
them using natural language.

Phase 1 focuses on setting up the project foundation.
"""
)

st.info(
    "CSV upload and AI analysis will be added in Phase 2."
)

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Uploaded Files", "0")

with col2:
    st.metric("Questions Asked", "0")

with col3:
    st.metric("Status", "Ready")

st.markdown("---")

st.subheader("🚀 Development Roadmap")

roadmap = [
    "✅ Phase 1 — Project Setup",
    "⬜ Phase 2 — CSV Upload & Validation",
    "⬜ Phase 3 — DataFrame Manager",
    "⬜ Phase 4 — Data Analysis",
    "⬜ Phase 5 — Charts",
    "⬜ Phase 6 — LLM Integration",
    "⬜ Phase 7 — AI Agent",
    "⬜ Phase 8 — Conversation Memory",
    "⬜ Phase 9 — SQL Engine",
    "⬜ Phase 10 — Insights",
    "⬜ Phase 11 — Anomaly Detection",
]

for item in roadmap:
    st.write(item)

st.markdown("---")

st.caption("AI Data Analyst • Built with Streamlit + Python")