
from backend.embeddings import search
from backend.llm import generate
from backend.config import TOP_K


def answer(question: str):
    context = "\n".join(search(question, TOP_K))
    prompt = f"""
    You are a helpful company AI assistant.
    
    Rules:
    - Use ONLY the information in the context.
    - If the answer is not in the context, say: "I don't have that information."
    - Be brief and factual.
    - Do NOT guess or add extra details.

    Context:
    {context}


    Question: {question}
    Answer:
    """
    return generate(prompt)