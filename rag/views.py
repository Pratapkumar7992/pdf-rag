from django.shortcuts import render
from .models import Document
from .services.pdf_loader import extract_text as extract_pdf_text
from .services.chunker import create_chunk
from .services.embeddings import create_embeddings

def home(request):
    extracted_text = ""
    chunks = []
    embeddings = []

    if request.method == "POST":
        pdf = request.FILES.get("pdf")

        if pdf:
            document = Document.objects.create(
                name=pdf.name,
                file=pdf
            )
            extracted_text = extract_pdf_text(document.file.path)
            
            chunks = create_chunk(extracted_text)
            
            embeddings = create_embeddings(chunks)

    return render(
        request, 
        "rag/index.html", 
        {"extracted_text": extracted_text,
         "chunks": chunks,
         "embeddings": len(embeddings)}
    )