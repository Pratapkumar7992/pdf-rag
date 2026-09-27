import logging

from django.shortcuts import render

from .models import Document
from .services.pdf_loader import extract_text as extract_pdf_text
from .services.chunker import create_chunk
from .services.embeddings import create_embeddings
from .services.vector_store import create_vector_store
from .services.retriever import retrieve_chunks
from .services.llm import generate_response

logger = logging.getLogger(__name__)


def home(request):
    extracted_text = ""
    chunks = []
    embeddings = []
    retrieved_chunks = []
    answer = ""
    embedding_count = 0
    embedding_dimension = 0
    upload_message = ""
    request_status = 200
    response_message = "Request completed successfully."

    logger.info("Incoming request: method=%s path=%s", request.method, request.path)

    if request.method == "POST":
        pdf = request.FILES.get("pdf")
        question = request.POST.get("question")

        logger.info("POST payload: pdf=%s question=%s", bool(pdf), bool(question))

        if pdf:
            logger.info("Processing PDF upload: %s", pdf.name)
            document = Document.objects.create(
                name=pdf.name,
                file=pdf
            )
            extracted_text = extract_pdf_text(document.file.path)

            if not extracted_text.strip():
                upload_message = "No text could be extracted from this PDF. Please upload a valid PDF with readable text."
                response_message = "PDF upload completed with warning: no extractable text found."
                request_status = 200
                logger.warning("Upload processed with warning: no text extracted from %s", pdf.name)
            else:
                chunks = create_chunk(extracted_text)
                if not chunks:
                    upload_message = "This PDF did not produce any readable chunks. Please try another file."
                    response_message = "PDF upload completed with warning: no chunks generated."
                    request_status = 200
                    logger.warning("Upload processed with warning: no chunks created for %s", pdf.name)
                else:
                    embeddings = create_embeddings(chunks)
                    create_vector_store(embeddings, chunks)
                    response_message = "PDF uploaded and indexed successfully."
                    logger.info("PDF uploaded and indexed successfully: %s", pdf.name)

        elif question:
            logger.info("Processing question: %s", question)
            retrieved_chunks = retrieve_chunks(question)
            context = "\n\n".join(retrieved_chunks)
            answer = generate_response(question, context)
            response_message = "Question answered successfully."
            logger.info("Question answered successfully for: %s", question)

    else:
        logger.info("GET request handled successfully.")

    logger.info("Returning response: status=%s message=%s", request_status, response_message)

    return render(
        request,
        "rag/index.html",
        {
            "extracted_text": extracted_text,
            "chunks": chunks,
            "embedding_count": len(embeddings),
            "retrieved_chunks": retrieved_chunks,
            "answer": answer,
            "upload_message": upload_message,
            "request_status": request_status,
            "response_message": response_message,
        },
        status=request_status,
    )