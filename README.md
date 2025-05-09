# RAG_2
Sure! Here's a complete `README.md` that includes both modules:

---

````markdown
# 🔍 Retrieval-Augmented Generation with LangChain, Azure OpenAI & Azure Cognitive Search

This repository contains two Python scripts:

- `PDF_RAG.py`: A complete pipeline for processing PDFs using LangChain and Azure OpenAI, storing chunks in a Chroma vector store, and answering questions using retrieval-augmented generation (RAG).
- `SearchAI_test.py`: A test script that integrates Azure Cognitive Search with Azure OpenAI to retrieve indexed documents and answer user queries.

---

## 📁 Files

| File | Description |
|------|-------------|
| `PDF_RAG.py` | Load a PDF, split it into chunks, store it in a Chroma DB, and run a RAG-style question answering with LangChain. |
| `SearchAI_test.py` | Uses Azure Cognitive Search to retrieve documents and queries Azure OpenAI (GPT-35-Turbo) to answer a question. |

---

## 📦 Installation

Before running either script, install the required packages:

```bash
pip install -qU \
    langchain[openai] \
    langchain-openai \
    langchain-chroma \
    langchain-text-splitters \
    langchain-community \
    langgraph \
    azure-search-documents \
    pypdf
````

---

## 🔐 Environment Setup

Both scripts require Azure credentials:

### For Azure OpenAI:

```bash
export AZURE_OPENAI_API_KEY="your-azure-openai-key"
export AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
export AZURE_OPENAI_ENDPOINT="https://your-resource-name.openai.azure.com/"
```

### For Azure Cognitive Search (used in `SearchAI_test.py`):

```bash
export AZURE_SEARCH_API_KEY="your-search-key"
```

---

## 📄 How to Use

### `PDF_RAG.py` (PDF → Embeddings → RAG)

1. Set your Azure OpenAI environment variables.
2. Set the path to your PDF file inside the script.
3. Run the script to load the PDF, split it, index it in Chroma, and answer a user-defined query.

### `SearchAI_test.py` (Semantic Search + QA)

1. Make sure your Azure Search index is live and contains documents with a `"content"` field.
2. Set your API keys as environment variables or enter them when prompted.
3. Run the script to perform a semantic search and query the LLM with top-k results.

---

## 💡 Example

### From `SearchAI_test.py`:

```python
query = "What is the difference between default and failure rate?"
```

The script retrieves relevant documents from Azure Search and uses GPT-35-Turbo to answer:

```
Answer: "The default rate refers to the proportion of borrowers who fail to meet their debt obligations..."
```

