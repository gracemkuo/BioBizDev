# search_agent.py
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os
import streamlit as st
from dotenv import load_dotenv

try:
    import streamlit as st
    try:
        SERPAPI_API_KEY = st.secrets["SERPAPI_API_KEY"]
    except Exception:
        SERPAPI_API_KEY = None
except ImportError:
    pass   

if not SERPAPI_API_KEY:
    load_dotenv()
    SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")

print("🔐 SERPAPI_API_KEY loaded:", os.getenv("SERPAPI_API_KEY")[:4], "...")


def search_and_extract_links(query, num_results=20, max_pages=5):
    print(f"Searching for: {query}")
    if not SERPAPI_API_KEY:
        raise ValueError("❌ SERPAPI_API_KEY is not set in environment variables.")
    print(f"Using SERPAPI_API_KEY: {SERPAPI_API_KEY[:4]}...")  # Print only the first 4 characters for security
    url = "https://serpapi.com/search"
    links = []

    for page in range(0, max_pages):
        start_index = page * num_results
        params = {
            "engine": "google",
            "q": query,
            "num": num_results,
            "start": start_index,
            "api_key": SERPAPI_API_KEY
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            print(f"❌ API Error on page {page+1}: {e}")
            continue

        count_this_page = 0
        for result in data.get("organic_results", []):
            link = result.get("link")
            if link and any(key in link.lower() for key in ["linkedin.com/in", "about", "team", "company", "leadership", "executive"]):
                links.append(link)
                count_this_page += 1
        print(f"✅ Page {page+1}: Added {count_this_page} links")
    print(f"✅ Total links collected: {len(links)}")
    return links

def batch_search_and_collect_links(keywords, batch_size=10):
    all_links = []
    total_batches = (len(keywords) + batch_size - 1) // batch_size
    progress = st.progress(0)
    for idx, i in enumerate(range(0, len(keywords), batch_size)):
        batch = keywords[i:i+batch_size]
        batch_query = " OR ".join(batch)
        st.info(f"🔍 Running batch {idx+1}/{total_batches}: {batch_query[:100]}...")
        batch_links = search_and_extract_links(batch_query, num_results=100)
        all_links.extend(batch_links)
        progress.progress((idx + 1) / total_batches)
    return all_links