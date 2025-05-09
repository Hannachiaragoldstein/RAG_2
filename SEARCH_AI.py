# Required installations (run in shell or notebook separately)
# %pip install --quiet --upgrade langchain-text-splitters langchain-community langgraph
# pip install -qU "langchain[openai]"
# pip install -qU langchain-openai
# pip install azure-search-documents

import os
import getpass
from itertools import islice
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from langchain.chat_models import AzureChatOpenAI

# --- Setup Azure OpenAI Credentials ---
if not os.environ.get("AZURE_OPENAI_API_KEY"):
    os.environ["AZURE_OPENAI_API_KEY"] = getpass.getpass("Enter API key for Azure OpenAI: ")
os.environ["AZURE_OPENAI_ENDPOINT"] = "https://aoi-intership-temp.openai.azure.com/openai/deployments/gpt-35-turbo/chat/completions?api-version=2025-01-01-preview"
os.environ["AZURE_OPENAI_DEPLOYMENT"] = "gpt-35-turbo"

llm = AzureChatOpenAI(
    model_name="gpt-35-turbo",
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    api_version="2025-01-01-preview",
)

# --- Setup Azure Cognitive Search Credentials ---
if not os.environ.get("AZURE_SEARCH_API_KEY"):
    os.environ["AZURE_SEARCH_API_KEY"] = getpass.getpass("Enter API key for Azure Search: ")

search_endpoint = "https://aoi-internship-temp-search.search.windows.net"
search_key = os.environ["AZURE_SEARCH_API_KEY"]
index_name = "azureblob-index2"

search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(search_key)
)

# --- Search Query ---
query = "What is the difference between default and failure rate?"
results = search_client.search(query)

# --- Collect Top-k Retrieved Documents ---
top_k = 3
documents = [result.get('content', '') for result in islice(results, top_k)]
docs_content = "\n\n".join(documents)

# --- Prepare and Run Prompt ---
prompt_template = "Given the context, answer the question: {question}\n\nContext: {context}"
final_prompt = prompt_template.format(question=query, context=docs_content)
answer = llm.invoke(final_prompt)

print("Answer:", answer)
