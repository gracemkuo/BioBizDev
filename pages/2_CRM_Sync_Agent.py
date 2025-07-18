import streamlit as st
import pandas as pd
from datetime import date


from service.google_calender_service import create_google_event
from datetime import datetime, timedelta

st.set_page_config(page_title="CRM Dashboard", layout="wide")

# 定義 Pipeline 階段順序
pipeline_stages = [
    "Initial Conversation",
    "Client Survey & Intro",
    "NDA Signed",
    "Milestone Discussion",
    "Quote Proposed",
    "Price Negotiated & Signed",
    "Downpayment Invoiced",
    "Round 1 Delivered",
    "Experiment Result Returned",
    "Round 2 Delivered",
    "Final Invoice",
    "Project Closed"
]

# 初始化
if "crm_data" not in st.session_state:
    st.session_state.crm_data = pd.DataFrame(columns=[
        "Company Name", "Contact Person", "Email", "Phone",
        "Interaction History", "Next Meeting", "Quote History", "Pipeline Stage"
    ])

st.title("🤝 CRM Dashboard")
st.markdown("Manage client records, pipeline progress, and outreach interactions.")

# Sidebar
st.sidebar.header("Client Management")
action = st.sidebar.radio("Select Action", ["Add New Client", "Edit Existing Client", "Delete Client"])

# Add Client
if action == "Add New Client":
    with st.sidebar.form("add_form", clear_on_submit=True):
        company = st.text_input("Company Name")
        contact = st.text_input("Contact Person")
        email = st.text_input("Email")
        phone = st.text_input("Phone")
        interaction = st.text_area("Interaction History", placeholder="e.g., Met at BioCon 2025")
        meeting = st.date_input("Next Meeting", value=date.today())
        quote = st.text_area("Quote History", placeholder="e.g., Sent quote for POC stage: $15,000")
        stage = st.selectbox("Pipeline Stage", pipeline_stages)
        submitted = st.form_submit_button("Add Client")
        if submitted and company:
            new_row = {
                "Company Name": company,
                "Contact Person": contact,
                "Email": email,
                "Phone": phone,
                "Interaction History": interaction,
                "Next Meeting": str(meeting),
                "Quote History": quote,
                "Pipeline Stage": stage
            }
            st.session_state.crm_data = pd.concat([
                st.session_state.crm_data,
                pd.DataFrame([new_row])
            ], ignore_index=True)
            st.success(f"✅ {company} added successfully.")

# Edit Client
elif action == "Edit Existing Client":
    if st.session_state.crm_data.empty:
        st.sidebar.warning("No clients available.")
    else:
        selected = st.sidebar.selectbox("Select a Company", st.session_state.crm_data["Company Name"])
        target = st.session_state.crm_data[st.session_state.crm_data["Company Name"] == selected].iloc[0]
        with st.sidebar.form("edit_form"):
            contact = st.text_input("Contact Person", value=target["Contact Person"])
            email = st.text_input("Email", value=target["Email"])
            phone = st.text_input("Phone", value=target["Phone"])
            interaction = st.text_area("Interaction History", value=target["Interaction History"])
            meeting = st.date_input("Next Meeting", value=pd.to_datetime(target["Next Meeting"]))
            quote = st.text_area("Quote History", value=target["Quote History"])
            stage = st.selectbox("Pipeline Stage", pipeline_stages, index=pipeline_stages.index(target["Pipeline Stage"]))
            update = st.form_submit_button("Update Client")
            if update:
                idx = st.session_state.crm_data.index[st.session_state.crm_data["Company Name"] == selected][0]
                st.session_state.crm_data.loc[idx] = [
                    selected, contact, email, phone, interaction, str(meeting), quote, stage
                ]
                st.success("✅ Client updated successfully.")

# Delete Client
elif action == "Delete Client":
    if st.session_state.crm_data.empty:
        st.sidebar.warning("No clients to delete.")
    else:
        selected = st.sidebar.selectbox("Select a Company", st.session_state.crm_data["Company Name"])
        if st.sidebar.button("Delete Client"):
            st.session_state.crm_data = st.session_state.crm_data[st.session_state.crm_data["Company Name"] != selected]
            st.success(f"🗑️ {selected} deleted successfully.")
# === SEARCH BAR ===
st.subheader("🔍 Search & View Clients")

search_query = st.text_input("Search by company name, contact, or email").strip().lower()
filtered_df = st.session_state.crm_data[
    st.session_state.crm_data.apply(
        lambda row: search_query in row["Company Name"].lower() or
                    search_query in row["Contact Person"].lower() or
                    search_query in row["Email"].lower(),
        axis=1
    )
] if search_query else st.session_state.crm_data


# 計算 Pipeline 進度
def stage_to_progress(stage):
    return (pipeline_stages.index(stage) + 1) / len(pipeline_stages)


# === CLIENT LIST VIEW WITH EXPANDABLE CARDS ===
if filtered_df.empty:
    st.info("No matching clients found.")
else:
    for _, row in filtered_df.iterrows():
        with st.expander(f"📌 {row['Company Name']}"):
            st.write(f"**Contact Person:** {row['Contact Person']}")
            st.write(f"**Email:** {row['Email']}")
            st.write(f"**Phone:** {row['Phone']}")
            st.write(f"**Next Meeting:** {row['Next Meeting']}")
            st.write(f"**Quote:** {row['Quote History']}")
            st.write(f"**Interaction:** {row['Interaction History']}")
            st.write(f"**Pipeline Stage:** {row['Pipeline Stage']}")
            progress = stage_to_progress(row["Pipeline Stage"])
            st.progress(progress)
            # 加入 Google Calendar 按鈕
            if st.button(f"📅 Add {row['Company Name']} to Google Calendar", key=f"calendar_{row['Company Name']}"):
                try:
                    meeting = pd.to_datetime(row["Next Meeting"])
                    company = row["Company Name"]
                    email = row["Email"]

                    start_dt = datetime.combine(meeting, datetime.min.time()) + timedelta(hours=10)
                    end_dt = start_dt + timedelta(hours=1)

                    cal_link = create_google_event(
                        summary=f"Meeting with {company}",
                        start_time=start_dt,
                        end_time=end_dt,
                        email=email
                    )

                    st.success(f"✅ Event created: [View on Google Calendar]({cal_link})")
                except Exception as e:
                    st.error(f"Google Calendar Error: {str(e)}")
            


# 加入進度欄位
if not st.session_state.crm_data.empty:
    st.session_state.crm_data["Pipeline Progress"] = st.session_state.crm_data["Pipeline Stage"].apply(stage_to_progress)

# 顯示客戶資料與進度條
st.subheader("📋 All Clients")
for _, row in st.session_state.crm_data.iterrows():
    with st.expander(row["Company Name"]):
        st.write(f"**Contact Person:** {row['Contact Person']}")
        st.write(f"**Email:** {row['Email']}")
        st.write(f"**Phone:** {row['Phone']}")
        st.write(f"**Next Meeting:** {row['Next Meeting']}")
        st.write(f"**Quote:** {row['Quote History']}")
        st.write(f"**Interaction:** {row['Interaction History']}")
        st.write(f"**Pipeline Stage:** {row['Pipeline Stage']}")
        st.progress(row["Pipeline Progress"])
        if st.button(f"📅 Add {row['Company Name']} to Google Calendar", key=f"calendar_all_{row['Company Name']}"):
            try:
                meeting = pd.to_datetime(row["Next Meeting"])
                company = row["Company Name"]
                email = row["Email"]

                start_dt = datetime.combine(meeting, datetime.min.time()) + timedelta(hours=10)
                end_dt = start_dt + timedelta(hours=1)

                cal_link = create_google_event(
                    summary=f"Meeting with {company}",
                    start_time=start_dt,
                    end_time=end_dt,
                    email=email
                )

                st.success(f"✅ Event created: [View on Google Calendar]({cal_link})")
            except Exception as e:
                st.error(f"Google Calendar Error: {str(e)}")
# 匯出 CSV
st.download_button(
    label="📥 Export as CSV",
    data=st.session_state.crm_data.to_csv(index=False),
    file_name="crm_data.csv",
    mime="text/csv"
)
