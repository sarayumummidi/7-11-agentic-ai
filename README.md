# Agentic AI for Insights on PDF Documents (7 Eleven)

This project focuses on developing an agentic AI system capable of autonomously extracting, summarizing, and generating insights from a collection of long, highly technical PDF manuals for 7-Eleven’s Franke commercial coffee machines. The system combines retrieval-augmented generation (RAG) with a multi-agent reasoning pipeline to deliver precise, contextually relevant answers to complex single- and multi-document queries.

Our goal is to demonstrate how an AI system can streamline information discovery, reduce troubleshooting time, and improve real-world operational decision-making across 7-Eleven stores.

## 👥 Team Members
| Name                       | GitHub Handle   | Contribution                                                                         |
| -------------------------- | --------------- | ------------------------------------------------------------------------------------ |
| **Hikmah Mohammed**        | @hikmahmohammed | Multi-agent pipeline (Planner → Retriever → Synthesizer), multi-document PDF processing, retrieval backbone exploration, project documentation |
| **Aydin Khan**             | @AydinK7        | Implemented the retrieval backbone with regex based PDF cleaning, LLM implementation with prompt engineering, and evaluated retrieval quality using relevant metrics|
| **Emily Wang**             | @emily-wang22   | Developed frontend message bubble and implemented frontend-side API integration      |
| **Sarayu Mummidi**         | @sarayumummidi  | Implemented FastAPI backend integrating the agentic workflow to the frontend, Real-time token by token streaming of LLM response, Frontend UI backdrop, and UI design/styling |
| **Harshika Vijayabharath** |  @HarshikaV     | Developed core frontend interaction features, including an advanced chat input module with controlled state, keyboard shortcuts, and seamless integration with the agentic reasoning pipeline, emabling real-time user interaction with the system |
| **Isabelle Ye**            |        @iaye1334         | Developed frontend AI chatbox input module chatpage UI, and integrated the send message operations|
| **Priya Deshmukh**         |  @priyasd-04    | Vector database design, pipeline from user query → embedding model → vector database → returning relevant chunks|


## 🎯 Project Highlights

- Built an intelligent RAG-powered agentic assistant for interpreting dense Franke coffee machine manuals

- Designed a multi-agent architecture (Planner → Retriever → Synthesizer) for structured reasoning and grounded answers

- Implemented a high-quality PDF ingestion pipeline using PyMuPDF, OCR fallback, regex cleaning, and metadata tagging

- Developed a vector search system using FAISS for fast, accurate retrieval across thousands of chunks

- Created a polished React UI chat interface with real-time messaging and auto-scroll behavior

- Achieved strong performance: 76% Precision@5, 92% Recall@5, 7.1s end-to-end latency, 4% hallucination rate


## 👩🏽‍💻 Setup & Installation

1. Clone Repository
   
```
git clone https://github.com/sarayumummidi/7-11-agentic-ai
```
2. Go to the right directory
```
cd 7-11-agentic-ai
```

3. Backend Setup
   
```
pip install -r requirements.txt
```

4. Update ```config.py```:

```
MISTRAL_API_KEY = your_key
```

5. Run the backend server

```
uvicorn main:app --reload
```

6. Frontend Setup
   
```
cd frontend
npm install
```

7. Run the frontend server
```
npm run dev
```

**The project will be available at ``http://localhost:5173`` to test.**



## 🏗️ Project Overview
According to project documentation, Franke machine manuals are long, dense, and inconsistent—often 70–100+ pages with mixed diagrams, procedures, and troubleshooting steps. Searching manually is slow and error-prone.

#### Our System Solves This Through:

- Automated ingestion + preprocessing

- Intelligent chunking + metadata tagging

- Vector search with FAISS

- Multi-agent reasoning for grounded, citation-linked answers

- A user-friendly chat frontend that runs in real time

#### Real-world impact:

- Faster troubleshooting

- Reduced training burden for new store associates

- More consistent & accurate machine maintenance

- Scalable solution for 83,000+ stores


## 📊 Data Exploration
### Datasets

- 5 manuals (A300–A1000)

- 70–100+ pages each

- Mixed text/diagrams → required OCR fallback

### Preprocessing Pipeline

- Text extraction via PyMuPDF

- OCR fallback via pytesseract

- Regex cleaning (headers, footers, whitespace)

### Chunking

- ~400 tokens per chunk

- 50-token overlap

- Metadata: manual, source_file, source_page, chunk_id

### Key EDA Insights

- Manuals vary heavily in structure → chunk size tuning required

- Metadata essential for selecting the correct machine model

- OCR increased text coverage for diagram-heavy pages

Include visuals such as:

- Chunk length histogram

- FAISS embedding similarity heatmap


## 🧠 Model Development
### 🔹 Retrieval Backbone

- Robust extraction and cleaning pipeline

- Metadata-enriched chunking

- FAISS vector index (L2 / cosine search)

### 🔹 Multi-Agent Architecture

- Planner: identifies intent + relevant manuals

- Retriever: pulls FAISS-ranked chunks

- Synthesizer: generates grounded, citation-backed answer via Mistral

### 🔹 Why Multi-Agent?

- Reduces hallucinations

- Enables cross-document reasoning

- Modular and scalable


## 📈 Results & Key Findings
| Metric                 | Value            |
| ---------------------- | ---------------- |
| **Precision@5**        | 76%              |
| **Recall@5**           | 92%              |
| **Retrieval Latency**  | 5ms avg, p95 6ms |
| **End-to-End Latency** | 7.1 seconds      |
| **Hallucination Rate** | 4%               |


### Insights:

- Chunking + FAISS dramatically improves relevance

- Multi-agent output yields clearer, more structured answers

- Latency acceptable for real store usage

Recommended visuals:

- Retrieval accuracy chart

- Latency distribution

- Annotated sample answer


## ⚠️ Risks, Challenges, & Mitigations
| Challenge                    | Risk                   | Mitigation                                            |
| ---------------------------- | ---------------------- | ----------------------------------------------------- |
| Hallucinations               | Incorrect instructions | Citation-enforced synthesis; retrieval-first pipeline |
| Latency                      | Multi-agent delay      | FAISS tuning, chunk reduction, caching                |
| Frontend/Backend Integration | Render failures        | Standardized API schema, error-handling               |


## 🚀 Next Steps
### Performance

- Bring latency < 10s consistently

- Add retrieval reranking

### Features

- Add advanced search & manual-specific filters

- Authentication + stored chat history

### Scalability

- Expand ingestion to all manuals

- Cloud deployment pipeline

### Model

- Feedback loops for continual improvement

- Explore lightweight fine-tuning


## 📝 License

This project is for Break Through Tech AI Studio and not licensed for external use.

## 📄 References

- Final project presentation

- FAISS documentation

- Mistral / OpenAI APIs

- PyMuPDF, Tesseract OCR

## 🙏 Acknowledgements

We thank:

- Our Challenge Advisor

- Break Through Tech AI program team

- 7-Eleven for providing guidance and context

- Our AI Studio Coach for feedback and support
