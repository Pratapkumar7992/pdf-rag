from django.shortcuts import render
from .models import Document


def home(request):

    if request.method == "POST":
        pdf = request.FILES.get("pdf")

        if pdf:
            Document.objects.create(
                name=pdf.name,
                file=pdf
            )

    return render(request, "rag/index.html")