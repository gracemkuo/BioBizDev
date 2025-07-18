import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os

st.set_page_config(page_title="Multi-Agent BizDev Assistant", page_icon="🧠", layout="wide")

st.title("🧠 Multi-Agent BizDev Assistant")

st.markdown("""
Welcome to the **Multi-Agent Business Development System**.  
Please use the sidebar to navigate through the available agents.

---

### 🧾 1. Briefing Agent - *Company Intelligence Generator*
- **Input**: Company name or website
- **Technology**: OpenAI GPT + Web scraping + Templates
- **Output**: Strategic briefing report (overview, pipeline, leadership, outreach draft)

---

### 🔗 2. CRM Organized Agent - *CRM Integration & Automation*
- **Input**: Leads and outreach progress
- **Technology**: Streamlit + Pandas + Google Calendar API
- **Function**:
    - Add, edit, delete client records
    - Track pipeline stages
    - Sync with Google Calendar for meetings

---

### 🤖 3. Client Q&A Chatbot Agent (RAG-based)
- **Technology**: LangChain + FAISS + Streamlit UI
- **Input**: User questions
- **Data Source**: Company FAQs, brochures, documents
- **Output**: Real-time, contextual answers with sources

---

### 🏢 4. Company List Viewer
- **Function**: Browse, filter, and search pre-scraped company list
- **Features**: Business type filter, keyword search, and table display
- **Data**: Static CSV or JSON file loaded from project directory

---
""")
