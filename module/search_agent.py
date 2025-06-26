# search_agent.py
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()
print("🔐 SERPAPI_API_KEY loaded:", os.getenv("SERPAPI_API_KEY")[:4], "...")
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")  
def search_and_extract_links(query, num_results=100):
    print(f"Searching for: {query}")
    if not SERPAPI_API_KEY:
        raise ValueError("❌ SERPAPI_API_KEY is not set in environment variables.")
    print(f"Using SERPAPI_API_KEY: {SERPAPI_API_KEY[:4]}...")  # Print only the first 4 characters for security
    url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": query,
        "num": num_results,
        "api_key": SERPAPI_API_KEY
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        print(f"Search request failed: {e}")
        return []

    links = []
    for result in data.get("organic_results", []):
        link = result.get("link")
        if not link:
            continue
        parsed_url = urlparse(link)
        domain = parsed_url.netloc
        if any(key in link.lower() for key in ["linkedin.com/in", "about", "team", "company", "leadership", "executive"]):
            links.append(link)
            print(f"✅ Link added: {link}")
    return links
