# app.py
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
import requests
import streamlit as st
import pandas as pd
from module.search_agent import search_and_extract_links
import os
import csv
from io import StringIO

load_dotenv()
client = OpenAI()

if not os.getenv("OPENAI_API_KEY") and not st.secrets.get("OPENAI_API_KEY"):
    st.error("❌ OpenAI API Key not found in Streamlit secrets or .env!")
    st.stop()

def clean_text(text):
    if not isinstance(text, str):
        return ""
    return text.strip().replace('"', '').replace("'", '')

def extract_contacts_from_links(links, context):
    contacts = []

    for url in links:
        try:
            page = requests.get(url, timeout=10)
            print(f"✅ Fetched: {url}, Status: {page.status_code}")
            soup = BeautifulSoup(page.content, "html.parser")
            text = soup.get_text(separator=" ", strip=True)[:3000]

            prompt = f"""
You are a biotech recruiter. Strictly output CSV format. No explanations, no apologies.

For each person, provide:
- Name (required)
- Job Title (required)
- Company Name (required)
- Email (optional)
- Original Webpage URL (required)

Context: {context}

HTML TEXT:
{text}

Expected Output (CSV Format):
Name,Title,Company,Email,URL
"""

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional recruiter and contact extractor. Return only CSV output."},
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response.choices[0].message.content
            print(f"✅ LLM raw response from {url}:\n{answer}\n")

            reader = csv.reader(StringIO(answer))
            for row in reader:
                # 判斷 row 至少有 3 欄，且內容非垃圾
                if len(row) >= 3:
                    cleaned_row = [clean_text(c) for c in row[:5]]
                    if (
                        cleaned_row[0] and cleaned_row[1] and cleaned_row[2] and
                        not any(x.lower() in cleaned_row[0].lower() for x in ["sorry", "html", "example", "provided", "template"])
                    ):
                        while len(cleaned_row) < 5:
                            cleaned_row.append("N/A")
                        contacts.append(cleaned_row)

        except Exception as e:
            print(f"❌ Error parsing {url}: {e}")
    if contacts:
        df = pd.DataFrame(contacts, columns=["Name", "Title", "Company", "Email", "URL"])
        df = df.drop_duplicates(subset=["Name", "Title", "Company"])
        df = df[
            (df["Name"].str.strip() != "") &
            (df["Company"].str.strip() != "") &
            (~df["Name"].str.contains("sorry|template|html|provided", case=False, na=False))
        ]
        for col in df.columns:
            df[col] = df[col].apply(clean_text)
    else:
        df = pd.DataFrame(columns=["Name", "Title", "Company", "Email", "URL"])

    return df