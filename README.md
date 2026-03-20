Vectorless RAG System (FastAPI + Streamlit + PostgreSQL + OpenAI)
Overview

This project implements a Vectorless Retrieval-Augmented Generation (RAG) system using:

FastAPI (Backend APIs)

Streamlit (User Interface)

PostgreSQL (Document storage + indexing)

OpenAI (LLM reasoning)

Unlike traditional RAG systems that use vector databases and embeddings, this project uses PostgreSQL Full-Text Search indexing to retrieve relevant documents.

This approach is:

Simpler to deploy

Cost-effective

Suitable for structured document collections

Production friendly for enterprise environments


System Architecture

                User
                 │
                 ▼
            Streamlit UI
                 │
                 ▼
              FastAPI
        ┌────────┴────────┐
        ▼                 ▼
PostgreSQL DB        OpenAI LLM
 (Documents)          (Reasoning)
        │                 ▲
        └──── Retrieval ──┘



Complete Workflow
1. User Uploads Document

User uploads a document from the Streamlit UI.

User → Upload Document → Streamlit UI

Streamlit sends the document to the backend API.

POST /upload
2. FastAPI Receives the File

FastAPI performs the following:

Receive uploaded file

Read file content

Extract text from document

Store document in database

Create search index automatically

Flow:

Upload Request
      ↓
FastAPI API
      ↓
Text Extraction
      ↓
Store in PostgreSQL
      ↓
Create Full Text Index
3. Document Stored in Database

Table structure:

documents
---------
id
title
content

Example stored data:

id: 1
title: transformer-paper.pdf
content: Attention Is All You Need...
Indexing (Core of Vectorless RAG)

Instead of embeddings, this project uses PostgreSQL Full Text Search.

Index created using:

GIN Index
to_tsvector()

Example:

CREATE INDEX idx_documents_fts
ON documents
USING GIN (to_tsvector('english', content));

What happens internally:

Document Text
      ↓
Tokenization
      ↓
Keyword Extraction
      ↓
Search Index Creation

Example transformation:

Original:
Attention is all you need transformer architecture

Converted Index:
'attent', 'need', 'transform', 'architectur'

This allows fast document retrieval without vectors.

Query Workflow (When User Asks Question)

User enters a question in the UI.

Example:

What is transformer architecture?

Flow:

User Question
      ↓
Streamlit
      ↓
FastAPI
      ↓
PostgreSQL Search
      ↓
Retrieve Relevant Documents
      ↓
Send Context to LLM
      ↓
LLM Generates Answer
      ↓
Display Response
Retrieval Process

Query executed in PostgreSQL:

SELECT title, content
FROM documents
WHERE to_tsvector('english', content)
@@ plainto_tsquery('transformer architecture')
LIMIT 5;

This retrieves the most relevant documents.

LLM Reasoning Step

After retrieval:

The system sends this to the LLM:

Context:
<Document content>

Question:
User question

LLM then generates the final answer.

Important:

LLM does not access the database directly.

It only sees:

Selected document content
Complete End-to-End Flow Diagram
User Uploads Document
        │
        ▼
Streamlit Upload UI
        │
        ▼
FastAPI Upload API
        │
        ▼
Extract Document Text
        │
        ▼
Store in PostgreSQL
        │
        ▼
Create Full Text Search Index
        │
        ▼
Document Ready for Search
        │
        ▼
User Asks Question
        │
        ▼
PostgreSQL Full Text Search
        │
        ▼
Retrieve Relevant Documents
        │
        ▼
Send Context to OpenAI LLM
        │
        ▼
LLM Generates Answer
        │
        ▼
Answer Displayed in UI
Why This is Called Vectorless RAG

Traditional RAG uses:

Embeddings
Vector Database
Similarity Search

This project uses:

Keyword Indexing
Full Text Search
PostgreSQL Search Engine

So:

No Embeddings
No Vector DB
No Chunking Required
How Document Security is Maintained

This system keeps documents safe because:

1 Documents remain inside your database

Documents are stored only in:

PostgreSQL
2 LLM does not store your data

Only a temporary prompt is sent.

Context + Question

After response generation:

Prompt is discarded
3 No training on your documents

The model is used only for inference.