import os
from dotenv import load_dotenv
import cohere
from pinecone import Pinecone, ServerlessSpec
from langchain.text_splitter import RecursiveCharacterTextSplitter

# --- 1. Load environment variables ---
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENV")

# --- 2. Initialize clients ---
co = cohere.Client(api_key=COHERE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

# --- 3. Setup Pinecone index ---
index_name = "rag-index"
if index_name not in pc.list_indexes():
    pc.create_index(
        name=index_name,
        dimension=1024,  # must match Cohere embedding dim
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1")
    )
    print(f"Index '{index_name}' created successfully.")
else:
    print(f"Index '{index_name}' already exists. Connecting to it.")

index = pc.Index(index_name)

# --- 4. Read data ---
with open("data/sample.txt", "r", encoding="utf-8") as f:
    text = f.read()

# --- 5. Chunking strategy (assignment requirement: 800–1200, overlap 10–15%) ---
chunk_size = 1000  # between 800 and 1200
chunk_overlap = int(chunk_size * 0.1)  # 10% overlap = 100

splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap,
    separators=["\n\n", "\n", " ", ""]
)

chunks = splitter.split_text(text)
print(f"Total chunks created: {len(chunks)}")

# --- 6. Generate embeddings and upsert into Pinecone ---
vectors = []
for i, chunk in enumerate(chunks):
    response = co.embed(
        texts=[chunk],
        model="embed-english-v3.0",
        input_type="search_document"
    )
    embedding = response.embeddings[0]

    vectors.append({
        "id": f"chunk-{i}",
        "values": embedding,
        "metadata": {"text": chunk}
    })

# Upsert in batches (safe for large docs)
index.upsert(vectors)
print(f"Upserted {len(vectors)} chunks into Pinecone index '{index_name}'.")
print("Indexing complete.")