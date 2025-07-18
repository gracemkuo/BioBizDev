import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter
from langchain.chains import RetrievalQA
from pydantic import SecretStr

# 🔐 讀取 .env 中的 OPENAI_API_KEY
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please set it in your .env file.")

# 📄 載入 PDF
pdf_path = "Ainnocence_SentinusAI_Deck_2025.pdf"
loader = PyPDFLoader(pdf_path)
pages = loader.load()

# ✂️ 拆分成 chunks
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(pages)

# 🔍 建立向量資料庫
embedding = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(docs, embedding)

# 🤖 啟用 QA Chain
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(
    model="gpt-4o",          # ✅ 使用新版推薦 model 名稱
    temperature=0            # ✅ 控制生成隨機性
)
llm=ChatOpenAI()
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=True,
)

# ❓ 問問題
question = "What does SentinusAI do and how is it different from traditional approaches?"
response = qa_chain.invoke(question)

# 📤 顯示回答
print("🧠 Answer:\n", response["result"])
print("\n📚 Source Pages:")
for doc in response["source_documents"]:
    print("-", doc.metadata.get("source", "Unknown"))
