import streamlit as st
import pandas as pd

st.set_page_config(page_title="Company List Viewer", layout="wide")
st.title("📊 Company List Filtering & Viewer Tool")

# 📁 直接載入現成 CSV 檔案（請確認檔案在同資料夾）
df = pd.read_csv("classified_companies_org.csv")

# 🔍 Business Type 篩選器
business_types = ["All"] + sorted(df["Business Type"].dropna().unique())
selected_type = st.selectbox("Filter by Business Type", business_types)

if selected_type != "All":
    df = df[df["Business Type"] == selected_type]

# 🔎 關鍵字搜尋（公司名稱、描述）
keyword = st.text_input("Enter keyword to search (Company Name or Description)").strip().lower()
if keyword:
    df = df[
        df["Company Name"].str.lower().str.contains(keyword) |
        df["Description"].str.lower().str.contains(keyword)
    ]

# 📋 顯示資料表格（可編輯）
edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "URL": st.column_config.LinkColumn("公司網址")
    }
)

# 💾 匯出功能
st.download_button(
    "📥 Download Filtered CSV",
    data=edited_df.to_csv(index=False),
    file_name="filtered_company_list.csv",
    mime="text/csv"
)
