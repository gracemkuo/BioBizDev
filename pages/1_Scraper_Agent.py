# 1_Scraper_Agent.py
import streamlit as st
import pandas as pd
from module.search_agent import search_and_extract_links
from module.llm_parser import extract_contacts_from_links
import json
from dotenv import load_dotenv
load_dotenv()
import os

# 1_Scraper_Agent.py

st.title("🔍 Biotech Contact Finder Agent")


with open("config/presets.json", "r", encoding="utf-8") as f:
    PRESET_KEYWORDS = json.load(f)

service_line = st.selectbox(
    "Select a service line:",
    list(PRESET_KEYWORDS.keys()),
    key="service_line_select"
)
default_keywords = PRESET_KEYWORDS.get(service_line, {}).get("keywords", [])
selected_keywords = st.multiselect(
    "Keywords (edit, remove, or add new):",
    options=default_keywords,      # 提供建議選項
    default=default_keywords,      # 自動填入預設關鍵字
    accept_new_options=True,
    key="keyword_multiselect"
)

service_line_tags = PRESET_KEYWORDS.get(service_line, {}).get("tags", [])
st.markdown(f"**Tags for this service line:** {', '.join(service_line_tags)}")


if st.button("Start Search", key="start_search_button"):
    st.info("Searching and analyzing results. Please wait...")
    if not selected_keywords:
        st.warning("Please provide at least one keyword.")
    else:
        search_query = " OR ".join(selected_keywords)
        links = search_and_extract_links(search_query)

        if not links:
            st.warning("No search results found.")
            results_df = pd.DataFrame() 
        else:
            results_df = extract_contacts_from_links(links, search_query)
            st.success(f"Found {len(results_df)} potential contacts.")
            for link in links:
                st.write(link)
            #st.stop() 
            st.dataframe(results_df)
            st.download_button("Download Results as CSV", results_df.to_csv(index=False), "contacts.csv", key="download_csv_button")
        leads = []
        for _, row in results_df.iterrows():
                company_text = row.get("Description", "") 
                matched_categories = []
                for category, keywords in PRESET_KEYWORDS.items():
                    if any(kw.lower() in company_text.lower() for kw in keywords):
                        matched_categories.append(category)
                leads.append({
                    "company": row.get("Company", ""),
                    "name": row.get("Name", ""),
                    "title": row.get("Title", ""),
                    "email": row.get("Email", ""),
                    "linkedin": row.get("URL", ""),
                    "matched_categories": matched_categories
                })

        leads_json = json.dumps(leads, indent=2)
        file_name = f"leads_{service_line.replace(' ', '_').replace('-', '').lower()}.json"
        st.download_button("Download Results as JSON", leads_json, file_name, key="download_json_button")


# Example output leads.json structure
# This is a mockup of what the output might look like based on the provided context.
        # [
        #     {
        #         "company_name": "Genomex Biotech",
        #         "industry_tags": ["Cell Therapy", "Precision Medicine"],
        #         "category": "CellulaAI - Cell Therapy & Biomanufacturing",
        #         "contacts": [
        #         {
        #             "name": "Dr. Alice Wang",
        #             "title": "VP of R&D",
        #             "role": "Scientific Decision Maker",
        #             "linkedin": "https://linkedin.com/in/alicewang"
        #         }
        #         ]
        #     }
        # ]
