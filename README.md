# PDF RAG

A Django-based PDF Question Answering app that lets you upload a PDF, extract text, split it into chunks, generate embeddings, store them in a FAISS vector database, and answer questions from the uploaded document.

## Features

- Upload PDF files via browser
- Extract text from PDF documents using PyMuPDF
- Split document text into chunks
- Generate embeddings using Sentence Transformers
- Store vectors in FAISS
- Retrieve relevant chunks for a user question
- Use Groq models to answer questions using document context
- Simple Django UI for upload + Q&A

## Tech Stack

- Python 3.12
- Django 6.1
- PyMuPDF
- Sentence Transformers
- FAISS
- Groq
- SQLite database

## Project Structure

```text
pdf-rag/
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── media/
│   └── documents/
├── rag/
│   ├── migrations/
│   ├── services/
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── llm.py
│   │   ├── pdf_loader.py
│   │   ├── retriever.py
│   │   └── vector_store.py
│   ├── templates/
│   │   └── rag/
│   │       └── index.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── vector_db/
├── .env
├── .gitignore
├── db.sqlite3
├── manage.py
├── README.md
└── requirements.txt (if added later)
```

## Prerequisites

- Python 3.10+
- Virtual environment recommended
- Groq API key

## Setup

1. Clone the repository
2. Create and activate a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
pip install Django faiss-cpu sentence-transformers PyMuPDF python-dotenv groq langchain-text-splitters
```

4. Create a `.env` file in the project root with your Groq key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

5. Run database migrations:

```bash
python manage.py migrate
```

6. Start the development server:

```bash
python manage.py runserver
```

7. Open the app in your browser:

```text
http://127.0.0.1:8000/
```

## Usage

1. Upload a PDF file from the homepage.
2. The app extracts text from the document.
3. The text is split into chunks and indexed in FAISS.
4. Ask a question about the uploaded document.
5. The app retrieves the most relevant chunks and sends them to the LLM for an answer.

## Important Notes

- The app currently expects a valid Groq API key in `.env`.
- If the uploaded PDF has no extractable text, the app shows a warning instead of crashing.
- FAISS index files and chunk data are stored under the `vector_db/` folder.
- If you want to use a different Groq model, update the model name in `rag/services/llm.py`.

## Troubleshooting

### 1. Upload fails with 500 error

Check whether:
- the PDF is valid
- the text extraction returns readable content
- the FAISS vector store has valid embedding dimensions

### 2. LLM answer fails

Check:
- `.env` contains a valid `GROQ_API_KEY`
- the model name in `rag/services/llm.py` is supported by your Groq account

### 3. Module import errors

Reinstall dependencies in the active virtual environment:

```bash
pip install -r requirements.txt
```

If you do not yet have a requirements file, install the packages manually as shown in the setup section.

## License

This project is intended for learning and local development. Add a license file if you plan to share it publicly.
