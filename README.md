# 🩺 MediRAG AI — Clinical Guideline Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-orange?style=for-the-badge)
![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM_API-6467F2?style=for-the-badge)
![RAG](https://img.shields.io/badge/RAG-Powered-blueviolet?style=for-the-badge)
![License](https://img.shields.io/badge/License-Not_Specified-lightgrey?style=for-the-badge)

##  Overview

**MediRAG AI** is an AI-powered clinical guideline intelligence platform designed to explore Retrieval-Augmented Generation (RAG) and improve the reliability of answers generated from uploaded medical documents.

The system allows users to upload clinical guideline PDFs, process their content, retrieve relevant information through semantic search, and generate context-aware responses using a Large Language Model (LLM).

It also provides a way to compare AI-generated responses with and without RAG to understand the role of document retrieval in reducing unsupported answers.

> **Disclaimer:** This is an educational and research-oriented project. It is not intended for medical diagnosis, treatment decisions, or clinical use.

##  Key Features

-  **PDF Upload:** Upload clinical guidelines and reference documents.
-  **Document Chunking:** Split extracted text into smaller, manageable sections.
-  **Text Embeddings:** Convert document chunks into numerical vector representations.
-  **Semantic Search:** Retrieve relevant document content using ChromaDB.
-  **RAG Chatbot:** Generate responses using retrieved context and an LLM.
-  **Source References:** Connect generated responses with supporting document sections.
-  **RAG vs Non-RAG Comparison:** Compare grounded and general LLM responses.
-  **Evaluation Dashboard:** Explore response quality and hallucination-related behavior.
-  **Modern Web Interface:** React-based frontend with a FastAPI backend.

##  Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React, JavaScript |
| Backend | Python, FastAPI |
| LLM Integration | OpenRouter API |
| Language Model | GPT-4o Mini via OpenRouter |
| Vector Database | ChromaDB |
| Embeddings | Sentence Transformers |
| Document Processing | PDF text extraction |
| API Server | Uvicorn |

##  System Architecture

```text
                 User
                  |
                  v
            React Frontend
                  |
                  v
             FastAPI Backend
                  |
       +----------+----------+
       |                     |
       v                     v
  PDF Ingestion          User Question
       |                     |
       v                     v
  Text Extraction       Query Embedding
       |                     |
       v                     v
  Text Chunking         ChromaDB Search
       |                     |
       v                     v
  Embedding Model       Relevant Chunks
       |                     |
       v                     v
     ChromaDB ----------> RAG Prompt
                             |
                             v
                       OpenRouter LLM
                             |
                             v
                    Grounded AI Response
```

##  How RAG Works

**1. Document Ingestion**

Users upload clinical guideline PDFs through the frontend.

**2. Text Extraction**

The backend extracts readable text from uploaded documents.

**3. Chunking**

The extracted content is divided into smaller chunks for efficient retrieval.

**4. Embedding Generation**

Sentence Transformers convert each chunk into a vector representation.

**5. Vector Storage**

The generated embeddings are stored in ChromaDB.

**6. Semantic Retrieval**

When a user asks a question, the system searches for the most relevant chunks.

**7. Response Generation**

The retrieved information is passed to the LLM as context, helping it generate a document-grounded response.

##  Installation and Setup

### Prerequisites

- Python 3.13 (standard 64-bit build)
- Node.js and npm
- OpenRouter API key
- Sufficient free disk space for ML dependencies

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/MediRAG-AI-Clinical-Guideline-Intelligence.git
cd MediRAG-AI-Clinical-Guideline-Intelligence
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Backend setup

```powershell
cd backend
py -V:3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### 3. Environment configuration

Create a `.env` file in the backend directory and configure the OpenRouter credentials using the environment variable names expected by the backend.

Example:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

Never commit real API keys or `.env` files to GitHub.

### 4. Start the backend

```powershell
python -m uvicorn app.main:app --reload --port 8000
```

Backend URL:

`http://localhost:8000`

### 5. Start the frontend

Open another terminal, navigate to the directory containing the frontend's `package.json`, and run:

```bash
npm install
npm run dev
```

Open the local URL displayed by the frontend development server.

## Example Test Questions

After uploading a sample clinical guideline PDF, users can ask:

- What is the recommended follow-up interval?
- What monitoring instructions are mentioned?
- Which symptoms require urgent medical attention?
- What information is missing from the uploaded document?

The chatbot should use retrieved document evidence and avoid inventing recommendations when the source does not contain the answer.

## RAG vs Non-RAG Evaluation

The platform is designed to compare two response-generation approaches.

| Aspect | Without RAG | With RAG |
|---|---|---|
| Knowledge source | General LLM knowledge | Retrieved PDF content |
| Document grounding | Not guaranteed | Context provided from documents |
| Source references | Usually unavailable | Supported by retrieved passages |
| Hallucination risk | Potentially higher | Can be reduced, not eliminated |
| Document-specific answers | Limited | Better suited to uploaded content |

The comparison is intended for educational evaluation rather than a guarantee of medical accuracy.

## Learning Objectives

This project demonstrates:

- Retrieval-Augmented Generation architecture
- Document ingestion and preprocessing
- Embedding models and vector databases
- Semantic similarity search
- Prompt engineering
- LLM API integration
- Hallucination analysis
- Full-stack AI application development

##  Future Improvements

- Hybrid search combining keyword and semantic retrieval
- Reranking retrieved document chunks
- More detailed source citations
- Automated evaluation with benchmark questions
- Support for multiple document formats
- User authentication and access control
- Improved observability and retrieval analytics
