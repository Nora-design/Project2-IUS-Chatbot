import chromadb

client = chromadb.HttpClient(host="localhost", port=8000)
collection = client.get_or_create_collection("ius_documents")

def retrieve_docs(query, n_results=3):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    docs = results['documents'][0]
    metadatas = results['metadatas'][0]

    # Filtering out None or empty documents
    filtered = [
        (doc, meta) for doc, meta in zip(docs, metadatas)
        if isinstance(doc, str) and doc.strip()
    ]

    return filtered

