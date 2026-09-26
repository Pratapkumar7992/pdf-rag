from django.shortcuts import render
from .models import Document
from .services.pdf_loader import extract_text as extract_pdf_text
from .services.chunker import create_chunk
from .services.embeddings import create_embeddings
from .services.vector_store import create_vector_store
from .services.retriever import retrieve_chunks

def home(request):
    extracted_text = ""
    chunks = []
    embeddings = []
    retrieved_chunks = []
    embedding_count = 0
    embedding_dimension = 0

    if request.method == "POST":
        pdf = request.FILES.get("pdf")
        question = request.POST.get("question")

        if pdf:
            document = Document.objects.create(
                name=pdf.name,
                file=pdf
            )
            extracted_text = extract_pdf_text(document.file.path)
            
            chunks = create_chunk(extracted_text)
            
            embeddings = create_embeddings(chunks)
            
            create_vector_store(embeddings, chunks)
        
        elif question:
            retrieved_chunks = retrieve_chunks(question)

    return render(
        request, 
        "rag/index.html", 
        {"extracted_text": extracted_text,
         "chunks": chunks,
         "embedding_count": len(embeddings),
         "retrieved_chunks": retrieved_chunks 
        }
    )