import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_response(question, context):
    if not question:
        return ""

    if not context:
        return "I could not find the answer in the provided document."

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful question-answering assistant. "
                "Answer the user's question using only the provided context. "
                "If the answer is not present in the context, say: "
                "\"I could not find the answer in the provided document.\""
            ),
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion:\n{question}",
        },
    ]

    try:
        response = client.chat.completions.create(
            model="allam-2-7b",
            messages=messages,
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception:
        return "I could not generate an answer right now. Please try again later."