# 📦 Install required libraries
#pip install --quiet --upgrade langchain[openai] langchain-text-splitters langchain-community langgraph langchain-openai langchain-chroma pypdf PyPDF2

# 🔐 Set Azure OpenAI credentials
import os
import getpass

if not os.environ.get("AZURE_OPENAI_API_KEY"):
    os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter API key for Azure OpenAI: ")

# Set environment variables
os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"] = "gpt-35-turbo"
os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"] = "text-embedding-new-model"
os.environ["AZURE_OPENAI_API_VERSION_CHAT"] = "2025-01-01-preview"
os.environ["AZURE_OPENAI_API_VERSION_EMBEDDING"] = "2023-05-15"

# 🧠 Load Chat Model
from langchain.chat_models import AzureChatOpenAI

llm = AzureChatOpenAI(
    model_name="gpt-35-turbo",
    deployment_name=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION_CHAT"],
)

# 🔍 Load Embeddings Model
from langchain_openai import AzureOpenAIEmbeddings

embeddings = AzureOpenAIEmbeddings(
    model="text-embedding-ada-002",
    deployment=os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION_EMBEDDING"],
)

# 🧹 Reset Vector Store
import shutil
persist_directory = "./chroma_langchain_db"
shutil.rmtree(persist_directory, ignore_errors=True)

# 🧠 Initialize Vector Store
from langchain_chroma import Chroma

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory=persist_directory,
)

# 📄 Load and split PDF
from langchain_community.document_loaders import PyPDFLoader

pdf_path = "/Users/hannachiaragoldstein/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Hannac/ULB/MA1/Banking/BANKING NOTES DE COURS FINALE.pdf" # <-- Replace this with your local path
loader = PyPDFLoader(pdf_path)
docs = loader.load()

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    add_start_index=True,
)

all_splits = text_splitter.split_documents(docs)
document_ids = vector_store.add_documents(documents=all_splits)

# 🧪 Test RAG-style prompt
from langchain import hub

prompt = hub.pull("rlm/rag-prompt")

question = "How are different balance sheet positions valued?"
retrieved_docs = vector_store.similarity_search(question)

context = "\n\n".join(doc.page_content for doc in retrieved_docs)
rag_prompt = prompt.invoke({"question": question, "context": context})
answer = llm.invoke(rag_prompt)

print(answer)
