# app.py
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import openai
import requests
import streamlit as st
import pandas as pd
from module.search_agent import search_and_extract_links
import os

try:
    openai.api_key = st.secrets.get("OPENAI_API_KEY")
except Exception:
    openai.api_key = None


if not openai.api_key:
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("❌ OpenAI API Key not found in secrets or .env!")
    st.stop()
    
def extract_contacts_from_links(links, context):
    contacts = []

    for url in links:
        try:
            page = requests.get(url, timeout=10)
            soup = BeautifulSoup(page.content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)[:3000]
            prompt = f"""Given the following HTML text, extract people names, titles, emails, company name if available.
            
            Task Context: {context}
            
            HTML TEXT:
            {text}
            
            Expected Output Format:
            Name,Title,Company,Email,LinkedIn/URL"""

            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional recruiter and contact extractor."},
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response['choices'][0]['message']['content']
            for line in answer.splitlines():
                parts = [p.strip() for p in line.split(',')]
                if len(parts) >= 4:
                    contacts.append(parts[:5])
        except Exception as e:
            print(f"Error parsing {url}: {e}")

        df = pd.DataFrame(contacts, columns=["Name", "Title", "Company", "Email", "URL"])
    return df
