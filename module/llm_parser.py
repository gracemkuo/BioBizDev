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
                        You are a biotech recruiter. Given the following HTML page text, extract up to 5 people profiles who may be decision makers.

                        For each person, provide:
                        - Name (if available)
                        - Job Title (if available)
                        - Company Name (guess if not explicitly mentioned)
                        - Email (if available)
                        - Original Webpage URL (this link)

                        Context: {context}

                        HTML TEXT:
                        {text}

                        Expected Output (CSV Format):
                        Name, Title, Company, Email, URL
                        """

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a professional recruiter and contact extractor."},
                    {"role": "user", "content": prompt}
                ]
            )

            answer = response.choices[0].message.content
            print(f"✅ LLM raw response from {url}:\n{answer}\n")
            
            reader = csv.reader(StringIO(answer))
            for row in reader:
                if len(row) >= 3:  # 至少有人名、title、company
                    while len(row) < 5:
                        row.append("N/A")
                    contacts.append(row[:5])
                    cleaned_row = [clean_text(c) for c in row[:5]]
                    if (
                        not any(x.lower() in cleaned_row[0].lower() for x in ["name", "sorry", "provided", "template", "html"]) and
                        cleaned_row[0] and cleaned_row[1]
                    ):
                        contacts.append(cleaned_row)\
            #                 except Exception as e:
            # print(f"❌ Error parsing {url}: {e}")
            # for line in answer.splitlines():
            #     parts = [p.strip() for p in line.split(',')]
            #     if len(parts) >= 5:
            #         contacts.append(parts[:5])

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