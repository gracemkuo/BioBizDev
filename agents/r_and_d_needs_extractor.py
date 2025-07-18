# # r_and_d_needs_extractor.py

# import os
# from dotenv import load_dotenv
# from langchain.agents import Tool, initialize_agent, AgentType
# from langchain_community.tools import DuckDuckGoSearchResults
# from langchain_openai import ChatOpenAI
# from langchain.globals import set_debug

# set_debug(True)
# load_dotenv()

# def extract_rnd_needs(company_name: str) -> str:
#     print(f"Extracting R&D needs for {company_name}")
#  # 🔍 Step 1: 自定義搜尋查詢
#     search_query = f"{company_name} funding pipeline site:prnewswire.com OR site:businesswire.com OR site:globenewswire.com OR site:{company_name.lower().replace(' ', '')}.com"

#     # 🔍 Step 2: 執行搜尋
#     search = DuckDuckGoSearchResults()
#     search_results = search.run(search_query)
#     tools = [
#         Tool(
#             name="web_search",
#             func=search.run,
#             description="Useful for finding recent biotech press releases"
#         )
#     ]

#     llm = ChatOpenAI(
#         model="gpt-4o",
#         temperature=0.3
#     )
#     agent = initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent=AgentType.OPENAI_FUNCTIONS,
#         verbose=True
#     )
#     # 🧠 Step 4: 構建背景資料 + 指令任務 prompt
#     context = f"""Below is a collection of real-world news and web information about {company_name}. Use it for context when generating the strategic briefing.
#                 Search results:
#                 {search_results}
#                 """

#     question = f"""
# You are an AI assistant that prepares strategic briefings about biotech companies.

# Your task is to summarize all key information available about **{company_name}**, including:

# 1. 🧬 **Executive Summary** (What the company does and why it matters)
# 2. 🧾 **Company Profile**
#     - Website
#     - Headquarters
#     - Founded year
#     - CEO or key executives
#     - Mission statement
# 3. 🧪 **Therapies and Technology**
#     - Lead therapies (e.g., troculeucel)
#     - Pipeline stage and mechanism
#     - Scientific innovation or differentiation
# 4. 💰 **Funding & Investors**
#     - Recent funding rounds
#     - Investor names and amounts
#     - Reason for investments
# 5. 📈 **Milestones & News**
#     - Recent regulatory approvals (e.g., FDA Fast Track)
#     - Clinical trial progress
#     - Any news headlines
# 6. 🔬 **R&D Challenges & Focus**
#     - Therapeutic focus areas
#     - Manufacturing bottlenecks
#     - Clinical/regulatory hurdles
#     - Partnerships or hiring priorities
# 7. 🔗 **Links & Resources**
#     - Official website
#     - Notable news links
#     - PDF or slides if found

# At the end, add a section: 
# **📌 Meeting Preparation Questions**
# Provide 2–3 strategic questions the reader should consider before meeting the company (e.g., competitive position, regulatory timelines, funding gaps).

# Return in clear markdown bullet-point format.
# """
#     # 🧾 Step 5: 呼叫 Agent 處理合併後 prompt
#     full_prompt = context + question
#     result = agent.run(full_prompt)

#     print("\n✅ R&D 結果：", result)
#     return result

# r_and_d_needs_extractor.py

# import os
# from dotenv import load_dotenv
# from langchain.agents import Tool, initialize_agent, AgentType
# from langchain_community.tools import DuckDuckGoSearchResults
# from langchain_openai import ChatOpenAI
# from langchain.globals import set_debug
# from textwrap import dedent
# import re
# from langchain_community.tools.tavily_search import TavilySearchResults

# set_debug(True)
# load_dotenv()
# def sanitize_filename(name: str) -> str:
#     return re.sub(r'[^a-zA-Z0-9_\-]', '_', name.strip().lower())

# def split_context_into_chunks(text: str, max_len: int = 3000) -> list:
#     lines = text.split('\n')
#     chunks = []
#     current_chunk = []
#     current_length = 0
#     for line in lines:
#         if current_length + len(line) < max_len:
#             current_chunk.append(line)
#             current_length += len(line)
#         else:
#             chunks.append('\n'.join(current_chunk))
#             current_chunk = [line]
#             current_length = len(line)
#     if current_chunk:
#         chunks.append('\n'.join(current_chunk))
#     return chunks


# def build_briefing_prompt(company_name: str, context: str):
#     return dedent(f"""
#         You are an AI assistant that prepares strategic briefings about biotech companies.

#         Your task is to summarize all key information available about **{company_name}**, including:

   
#         Please find both the LinkedIn profile and the email address of the CEO of {company_name}.
#         If either one is not available or cannot be found publicly, explicitly state that in the answer.
#         Always include:
#         1. CEO name
#         2. LinkedIn profile (or "Not found")
#         3. Email address (or "Not found / Not publicly available")

#         Return the result clearly with bullet points.


#         1. 🧬 **Executive Summary** (What the company does and why it matters)
#         2. 🧾 **Company Profile**
#             - Website
#             - Headquarters
#             - Founded year
#             - CEO or key executives
#             - Mission statement
#         3. 🧪 **Therapies and Technology**
#             - Lead therapies (e.g., troculeucel)
#             - Pipeline stage and mechanism
#             - Scientific innovation or differentiation
#         4. 💰 **Funding & Investors**
#             - Recent funding rounds
#             - Investor names and amounts
#             - Reason for investments
#         5. 📈 **Milestones & News**
#             - Recent regulatory approvals (e.g., FDA Fast Track)
#             - Clinical trial progress
#             - Any news headlines
#         6. 🔬 **R&D Challenges & Focus**
#             - Therapeutic focus areas
#             - Manufacturing bottlenecks
#             - Clinical/regulatory hurdles
#             - Partnerships or hiring priorities
#         7. 🔗 **Links & Resources**
#             - Official website
#             - Notable news links
#             - PDF or slides if found

#         At the end, add a section: 
#         **📌 Meeting Preparation Questions**
#         Provide 2–3 strategic questions the reader should consider before meeting the company (e.g., competitive position, regulatory timelines, funding gaps).

#         Return in clear markdown bullet-point format.

#         Context:
#         {context}
#     """)
# def build_outreach_prompt(company_name: str, briefing: str):
#     return dedent(f"""
#     Based on this strategic briefing about {company_name}:

#     {briefing}

#     Draft:
#     1. Email Outreach (subject + body)
#     2. LinkedIn Message
#     3. Contact Form Message

#     Be concise, professional, and reference their actual R&D needs. Tie your service offering to those needs.
#     """)




# def extract_rnd_needs(company_name: str) -> str:
#     print(f"Extracting R&D needs for {company_name}")
    
#  # 🔍 Step 1: 自定義搜尋查詢
#     search_query = f"{company_name} funding pipeline site:prnewswire.com OR site:businesswire.com OR site:globenewswire.com OR site:{company_name.lower().replace(' ', '')}.com"

#     # 🔍 Step 2: 執行搜尋
#     search = DuckDuckGoSearchResults()
#     search_results = search.run(search_query)
#     tools = [
#         Tool(
#             name="web_search",
#             func=search.run,
#             description="Useful for finding recent biotech press releases"
#         )
#     ]
#     llm = ChatOpenAI(
#         model="gpt-4o",
#         temperature=0.3
#     )
#     agent = initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent=AgentType.OPENAI_FUNCTIONS,
#         verbose=True
#     )
#     context_chunks = split_context_into_chunks(search_results)

#     # Step 2: 每段進行摘要 + 合併
#     all_briefings = []
#     for i, chunk in enumerate(context_chunks):
#         print(f"🧩 Processing chunk {i+1}/{len(context_chunks)}")
#         prompt = build_briefing_prompt(company_name, chunk)
#         summary = agent.run(prompt)
#         all_briefings.append(summary)

#     merged_briefing = "\n\n".join(all_briefings)

#     # Step 3: 產出 Outreach Message
#     outreach_prompt = build_outreach_prompt(company_name, merged_briefing)
#     outreach = agent.run(outreach_prompt)
#     # ✅ 儲存為 Markdown 檔
#     output = f"# {company_name} Strategic Briefing\n\n"
#     output += merged_briefing.strip() + "\n\n"
#     output += "# 📬 Outreach Messages\n\n"
#     output += outreach.strip()

#     filename = f"{sanitize_filename(company_name)}_briefing.md"
#     with open(filename, "w", encoding="utf-8") as f:
#         f.write(output)
#     print(f"✅ Markdown saved to: {filename}")

#     return output

# r_and_d_needs_extractor.py
import os
import re
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_community.tools import DuckDuckGoSearchResults
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from textwrap import dedent
from agents.find_leadership import find_leadership_contact


# 初始化
load_dotenv()

# 🔧 工具設定
search_ddg = DuckDuckGoSearchResults()
search_tavily = TavilySearchResults(k=8)  # Tavily 搜尋數量

tavily_tools = [
    # Tool(
    #     name="duckduckgo_search",
    #     func=search_ddg.run,
    #     description="Use this to find people (e.g., LinkedIn profile or email of a CEO), or when searching for named individuals"
    # ),
    Tool(
        name="tavily_search",
        func=search_tavily.run,
        description="Best suited for retrieving recent, high-quality biotech press releases, funding and clinical pipeline updates. Not suitable for people search"
    )
]

# 🔑 LLM 模型
llm = ChatOpenAI(model="gpt-4o", temperature=0.3)

agent = initialize_agent(
    tools=tavily_tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True
)

# ✂️ 工具：字串處理
def sanitize_filename(name: str) -> str:
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name.strip().lower())


# 📄 Prompt：產出報告
def split_context_into_chunks(text: str, max_len: int = 3000) -> list:
    lines = text.split('\n')
    chunks, current_chunk, current_length = [], [], 0
    for line in lines:
        if current_length + len(line) < max_len:
            current_chunk.append(line)
            current_length += len(line)
        else:
            chunks.append('\n'.join(current_chunk))
            current_chunk = [line]
            current_length = len(line)
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    return chunks

# leadership prompt
# def extract_leadership_contact(company_name: str) -> str:
#     prompt = dedent(f"""
#     Please find both the LinkedIn profile and the email address of the CEO of {company_name}.
#     If either one is not available or cannot be found publicly, explicitly state that in the answer.
#     Always include:
#     1. CEO name
#     2. LinkedIn profile (or "Not found")
#     3. Email address (or "Not found / Not publicly available")

#     Return the result clearly with bullet points.
#     """)
#     return agent.run(prompt)


# 🧠 Prompt 建構
def build_briefing_prompt(company_name: str, context: str):
    return dedent(f"""
        You are an AI assistant that prepares strategic briefings about biotech companies.

        Your task is to summarize all key information available about **{company_name}**, including:

        1. 🧬 **Executive Summary**
        2. 🧾 **Company Profile**
            - Website, HQ, CEO, Mission
        3. 🧪 **Therapies and Technology**
        4. 💰 **Funding & Investors**
        5. 📈 **Milestones & News**
        6. 🔬 **R&D Challenges & Focus**
        7. 🔗 **Links & Resources**

        Add at the end:
        **📌 Meeting Preparation Questions**

        Context:
        {context}
    """)

def build_outreach_prompt(company_name: str, briefing: str):
    return dedent(f"""
    Based on this strategic briefing about {company_name}:

    {briefing}

    Draft:
    1. Email Outreach (subject + body)
    2. LinkedIn Message
    3. Contact Form Message

    Be concise, professional, and reference their actual R&D needs. Tie your service offering to those needs.
    """)

# 🔍 主邏輯
def extract_rnd_needs(company_name: str) -> str:
    print(f"\n🔍 Extracting R&D needs for: {company_name}")

    # 自動讓 agent 選擇用哪個搜尋工具
    search_query = f"{company_name} funding pipeline site:prnewswire.com OR site:businesswire.com OR site:globenewswire.com OR site:{company_name.lower().replace(' ', '')}.com"
    search_results = agent.run(f"Search online for: {search_query}. Return useful content for preparing a briefing about {company_name}'s recent biotech updates.")

    # 拆段摘要
    chunks = split_context_into_chunks(search_results)
    summaries = []
    for i, chunk in enumerate(chunks):
        print(f"🧩 Summarizing chunk {i+1}/{len(chunks)}...")
        prompt = build_briefing_prompt(company_name, chunk)
        summary = agent.run(prompt)
        summaries.append(summary)

    merged_briefing = "\n\n".join(summaries)

    # 產生 outreach 提案
    outreach_prompt = build_outreach_prompt(company_name, merged_briefing)
    outreach = agent.run(outreach_prompt)

    # 儲存為 markdown
    filename = f"{sanitize_filename(company_name)}_briefing.md"
    leadership_info = find_leadership_contact(company_name)

    if isinstance(leadership_info, str):
        # 若已經是 markdown 格式好的字串
        leadership_markdown = leadership_info.strip()
    elif isinstance(leadership_info, dict):
        # 若為解析後的 dict，格式化成 markdown
        leadership_markdown = "\n".join([
            f"- **CEO**: {leadership_info.get('ceo', 'N/A')}",
            f"- **LinkedIn**: {leadership_info.get('linkedin', 'N/A')}",
            f"- **Email**: {leadership_info.get('email', 'N/A')}",
        ])
    output = f"""\
# {company_name} Strategic Briefing

## Leadership Contact

{leadership_markdown}

---

{merged_briefing.strip()}

---

# Outreach Messages

{outreach.strip()}
"""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(output)

    print(f"\n✅ Markdown saved to: {filename}")
    return output

