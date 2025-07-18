
import streamlit as st
from agents.r_and_d_needs_extractor import extract_rnd_needs
import time
st.set_page_config(page_title="🧠 Strategic Briefing Generator", layout="wide")

st.title("📊 Biotech Company Briefing Agent")
st.markdown("Enter the company name to automatically generate a strategic briefing and outreach recommendations.")

company_name = st.text_input("Company Name", placeholder="例如：AbbVie Inc.")


if st.button("🚀 Generate Briefing"):
    if not company_name.strip():
        st.warning("Please enter a valid company name.")
    else:
                # 💡 顯示模擬的 Agent 思考過程
        placeholder = st.empty()
        steps = [
            "🔍 Retrieving company news and background",
            "🧪 Analyzing R&D focus and investment activities",
            "✍️ Generating strategic briefing",
            "💬 Drafting outreach messages (Email, LinkedIn, Contact Form)"
        ]
        for step in steps:
            placeholder.markdown(f"{step} ⏳")
            time.sleep(1)
            placeholder.markdown(f"{step} ✅")
        with st.spinner("🧠 Processing analysis and content generation..."):
            try:
                result = extract_rnd_needs(company_name)
                cleaned_result = result.replace("🗣️", "").replace("\n\n", "\n").replace("\n", "\n\n")
                st.markdown("### 🧾 Strategic Briefing Output")
                st.markdown(cleaned_result, unsafe_allow_html=True)
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
