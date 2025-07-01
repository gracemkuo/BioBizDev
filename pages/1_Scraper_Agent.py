# 1_Scraper_Agent.py
import streamlit as st
import pandas as pd
from module.search_agent import search_and_extract_links, batch_search_and_collect_links
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
    with st.spinner("🔍 Searching and analyzing results. Please wait..."):
        if not selected_keywords:
            st.warning("Please provide at least one keyword.")
        else:
           
            links = batch_search_and_collect_links(selected_keywords, batch_size=5)

            if not links:
                st.warning("No search results found.")
                results_df = pd.DataFrame() 
            else:
                results_df = extract_contacts_from_links(links,  " OR ".join(selected_keywords))
                st.success(f"Found {len(results_df)} potential contacts.")
                for link in links:
                    st.write(link)
                st.dataframe(results_df)
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
            cleaned_leads = []
            seen = set()

            for lead in leads:
                name = lead.get("name", "").strip()
                title = lead.get("title", "").strip()
                company = lead.get("company", "").strip()

                # 跳過明顯錯誤/空白資料
                if not name or not title:
                    continue
                if "no contact details" in name.lower() or "html text" in name.lower() or "provided" in name.lower():
                    continue
                if "there is no mention" in name.lower() or "csv format" in name.lower():
                    continue

                # 用 company+name+title 做唯一 key 去重
                unique_key = f"{company}_{name}_{title}"
                if unique_key in seen:
                    continue
                seen.add(unique_key)
                cleaned_leads.append(lead)

            leads_json = json.dumps(cleaned_leads, indent=2)

            file_name = f"leads_{service_line.replace(' ', '_').replace('-', '').lower()}.json"
            st.download_button("Download Results as JSON", leads_json, file_name, key="download_json_button")

