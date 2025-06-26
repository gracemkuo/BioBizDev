import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import os

st.set_page_config(page_title="Multi-Agent BizDev Assistant", page_icon="🧠")

st.title("🧠 Multi-Agent BizDev Assistant")

st.markdown("""
Welcome to the **Multi-Agent Business Development System**.  
Please use the sidebar to navigate through the five functional agents.

---

### 🏭 1. Scraper Agent - *Company & Contact Info Scraper*
- **Input**: Keywords (e.g., Protein Design / RNA / UAE / USA)
- **Technology**: Scrapy / Playwright + GPT filtering for titles
- **Output**: `leads.json` with company name, contact, title, email, LinkedIn, etc.

---

### ✉️ 2. Marketing Message Generator Agent
- **Input**: `leads.json` from the Scraper Agent
- **Technology**: OpenAI GPT-4 + Jinja2 templates + Company site scraping (e.g., `newspaper3k`)
- **Output**: `messages.json` with email, LinkedIn message, and contact form text

---

### 🤖 3. Client Q&A Chatbot Agent (RAG-based)
- **Technology**: LangChain + FAISS + Streamlit/Next.js frontend
- **Input**: User questions
- **Data Source**: FAQs, whitepapers, pricing sheets, pitch decks
- **Output**: Generated answers with source context  
- **Bonus**: Option to log conversations back to CRM

---

### 🔗 4. CRM Sync Agent - *CRM Integration & Automation*
- **Input**: `leads.json`, `messages.json`
- **Technology**: Pipedrive API + Webhooks + Cron jobs
- **Function**:
    - Create leads/deals
    - Sync message content
    - Trigger next steps based on sales stage

---

### 📆 5. Project Tracker Agent - *Post-Sales Workflow*
- **Input**: Deals marked as "Won" in CRM
- **Technology**: Pipedrive API + Google Calendar + Notion/Airtable APIs
- **Output**: Timeline milestones, reminders, invoice templates
- **Task Management**: Automatically generated delivery plans

---
""")
