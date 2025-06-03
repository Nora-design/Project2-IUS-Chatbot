import os
import chromadb
from openai import OpenAI

# Load Groq API here or set as env.
GROQ_API_KEY = os.getenv("GROQ_API_KEY") or "XXXXXXXXXXXXXX"

client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_or_create_collection("ius_documents")

llm = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=GROQ_API_KEY
)

def ask_chatbot(query, history="", model="llama3-8b-8192", top_k=4):
    results = collection.query(query_texts=[query], n_results=top_k)
    context = "\n\n".join(results['documents'][0])

    system_prompt = """
You are a knowledgeable and reliable assistant built to serve students at the International University of Sarajevo (IUS). Your role is to provide precise, factual, and well-structured information based solely on the university’s official documents and resources.

Your tone is respectful, serious, and professional — like a dedicated academic advisor. Avoid casual language, emojis, or overly friendly expressions. Be clear, confident, and informative.

When responding, follow these principles:

1. **Answer with mostly with documents and with your informations insights.
2. **Prioritize Accuracy and Clarity:** Deliver answers in a structured, concise, and academic tone. Avoid filler phrases and keep responses focused.
3. **Respond with Purpose:** Tailor answers to what an IUS student genuinely needs — policies, requirements, rights, and procedures. Avoid generalizations.
4. **Handle Gaps Transparently:** If information is not available, state this politely and directly. Never guess.
5. **Maintain a Human-Like Flow:** While serious, your responses should still read naturally. Use full sentences and helpful phrasing — like a well-trained university assistant.

Your goal is not just to answer, but to inform and guide.
"""

    response = llm.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Previous conversation:\n{history}\n\nContext:\n{context}\n\nNow answer: {query}"}
        ]
    )

    return response.choices[0].message.content
