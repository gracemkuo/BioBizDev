# 📁 agents/contact_finder.py
# # BioBizDev Agent: Search Agent
# from langchain.agents import initialize_agent, Tool, AgentType
# from langchain_openai import ChatOpenAI
# from langchain_community.tools import DuckDuckGoSearchResults
# import os
# from dotenv import load_dotenv
# from langsmith import traceable
# from langchain.globals import set_debug

# set_debug(True)

# def find_leadership_contact(company_name):
#     print(f"Finding leadership contact for {company_name}")
#     search = DuckDuckGoSearchResults()
#     tools = [
#         Tool(
#             name="web_search",
#             func=search.run,
#             description="Useful for finding recent information about a company or person"
#         )
#     ]
#     load_dotenv()
#     openai_api_key = os.getenv("OPENAI_API_KEY")
#     langchain_api_key = os.getenv("LANGCHAIN_API_KEY")
#     langchain_endpoint = os.getenv("LANGSMITH_ENDPOINT")

#     llm = ChatOpenAI(
#         model="gpt-4o",          
#         temperature=0            
#     )
#     # Agent: use OpenAI functions style to avoid format errors
#     agent = initialize_agent(
#         tools=tools,
#         llm=llm,
#         agent=AgentType.OPENAI_FUNCTIONS,  
#         verbose=True
#     )
#     # agent = initialize_agent(
#     #     tools, 
#     #     llm, 
#     #     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
#     #     verbose=True,
#     #     handle_parsing_errors=True)

#     # 問它去找一個公司資訊
#     question = f"""
#     Please find both the LinkedIn profile and the email address of the CEO of {company_name}.
#     If either one is not available or cannot be found publicly, explicitly state that in the answer.
#     Always include:
#     1. CEO name
#     2. LinkedIn profile (or "Not found")
#     3. Email address (or "Not found / Not publicly available")

#     Return the result clearly with bullet points.
#     """
#     result=agent.run(question)
#     print("\n✅ 結果：", result)



# find_leadership_contact.py

from langchain.agents import initialize_agent, Tool, AgentType
from langchain_openai import ChatOpenAI
from langchain_community.tools import DuckDuckGoSearchResults
import os
from dotenv import load_dotenv
from langsmith import traceable
from langchain.globals import set_debug
import re

set_debug(True)

def parse_result(text: str) -> dict:
    # 抓 CEO name
    name_match = re.search(r"\*\*CEO Name\*\*:\s*(.+)", text, re.IGNORECASE)

    # 抓 LinkedIn markdown 格式：[title](url)
    linkedin_match = re.search(r"\*\*LinkedIn Profile\*\*:\s*\[.*?\]\((.*?)\)", text, re.IGNORECASE)

    # 抓 Email
    email_match = re.search(r"\*\*Email Address\*\*:\s*(.+)", text, re.IGNORECASE)

    return {
        "ceo": name_match.group(1).strip() if name_match else "Not found",
        "linkedin": linkedin_match.group(1).strip() if linkedin_match else "Not found",
        "email": email_match.group(1).strip() if email_match else "Not found"
    }

def find_leadership_contact(company_name: str) -> dict:
    print(f"🔍 Finding leadership contact for {company_name}")
    search = DuckDuckGoSearchResults()
    web_tools = [
        Tool(
            name="web_search",
            func=search.run,
            description="Useful for finding recent information about a company or person"
        )
    ]

    load_dotenv()
    llm = ChatOpenAI(model="gpt-4o", temperature=0)

    agent = initialize_agent(
        tools=web_tools,
        llm=llm,
        agent=AgentType.OPENAI_FUNCTIONS,
        verbose=True
    )

    question = f"""
Please find both the LinkedIn profile and the email address of the CEO of {company_name}.
If either one is not available or cannot be found publicly, explicitly state that in the answer.
Always include:
1. CEO name
2. LinkedIn profile (or "Not found")
3. Email address (or "Not found / Not publicly available")

Return the result clearly with bullet points.
"""
    raw_output = agent.run(question)
    print("\n✅ LLM 回傳內容：\n", raw_output)
    parsed = parse_result(raw_output)
    print("📦 Parsed:", parsed)
    return parsed

if __name__ == "__main__":
    # 🧪 測試執行：輸入公司名稱與官網網址
    find_leadership_contact("NKGen Biotech")
