from django.shortcuts import render
from .models import Document
from .services.pdf_loader import extract_text as extract_pdf_text


def home(request):
    extracted_text = ""

    if request.method == "POST":
        pdf = request.FILES.get("pdf")

        if pdf:
            document = Document.objects.create(
                name=pdf.name,
                file=pdf
            )
            extracted_text = extract_pdf_text(document.file.path)

    return render(request, "rag/index.html", {"extracted_text": extracted_text})