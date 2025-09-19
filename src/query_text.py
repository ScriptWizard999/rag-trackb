import os
import cohere
from pinecone import Pinecone
import re
from dotenv import load_dotenv
import streamlit as st
import os

# If running on Streamlit Cloud
if "COHERE_API_KEY" in st.secrets:
    COHERE_API_KEY = st.secrets["COHERE_API_KEY"]
    PINECONE_API_KEY = st.secrets["PINECONE_API_KEY"]
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
# If running locally (fallback to .env)
else:
    from dotenv import load_dotenv
    load_dotenv()
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

co = cohere.Client(api_key=COHERE_API_KEY)
pc = Pinecone(api_key=PINECONE_API_KEY)

index_name = "rag-index"
index = pc.Index(index_name)

def rag_query(question):
    try:
        # Step 1: Embed
        query_embedding = co.embed(
            texts=[question],
            model="embed-english-v3.0",
            input_type="search_query"
        ).embeddings[0]

        # Step 2: Pinecone
        pinecone_results = index.query(
            vector=query_embedding,
            top_k=50,
            include_metadata=True
        )

        documents_to_rerank = [
            match['metadata']['text']
            for match in pinecone_results['matches']
            if 'metadata' in match and 'text' in match['metadata']
        ]
        if not documents_to_rerank:
            return "I don't know. No relevant documents were found for this query.", []

        # Step 3: Rerank
        reranked_results = co.rerank(
            model="rerank-v3.5",
            query=question,
            documents=documents_to_rerank,
            top_n=5
        )
        if not reranked_results.results:
            return "I don't know. The reranker could not find relevant documents.", []

        top_docs_for_chat = [
            documents_to_rerank[result.index]
            for result in reranked_results.results
        ]

        # Step 4: LLM
        context = "\n\n".join([f"[{i+1}] {doc}" for i, doc in enumerate(top_docs_for_chat)])
        prompt = (
                "You are a helpful AI assistant. "
                "Use the following context to answer the question. "
                "Do not use outside knowledge. "
                "If the answer is not present, say 'I don't know'. "
                "When answering, you MUST cite using only the numbers provided in the context." 
                "If the context provides [1], [2], [3], you may only cite from those." 
                "Never invent a new citation number." 
                "If no citation is relevant, say 'I don't know.'"
                "When citing, only use the numbers provided in the context "
                "(e.g., [1], [2], [3]). "
                "Never invent citation numbers outside the given range.\n\n"
                f"Context:\n{context}\n\nQuestion:\n{question}"
            )


        final_answer_response = co.chat(
            model="command-a-03-2025",
            message=prompt,
            temperature=0.3
        )
        final_answer_text = final_answer_response.text

        # --- FIXED Citation alignment ---
        # Extract citations
        cited_indices = [int(m) for m in re.findall(r'\[(\d+)\]', final_answer_text)]
        valid_sources = [(i, top_docs_for_chat[i-1]) for i in cited_indices if 0 < i <= len(top_docs_for_chat)]

        # Fallback: if LLM gave invalid citations, still show top docs
        if not valid_sources:
            valid_sources = [(i+1, doc) for i, doc in enumerate(top_docs_for_chat[:2])]

        return final_answer_text, valid_sources



    except cohere.core.api_error.ApiError as e:
        if "429" in str(e):
            return "Error: Cohere API rate limit exceeded. Please wait and try again.", []
        return f"An API error occurred: {e}", []
    except Exception as e:
        return f"An unexpected error occurred: {e}", []



# --- 3. MAIN EXECUTION ---
if __name__ == "__main__":
    while True:
        user_question = input("\nAsk a question about the article (or type 'exit' to quit): ")
        if user_question.lower() == 'exit':
            break
        
        answer, sources = rag_query(user_question)
        print("\n------------------ Answer ------------------")
        print(answer)
        print("--------------------------------------------")
        if sources:
            print("\n------------------ Sources -----------------")
            for i, source_text in enumerate(sources):
                print(f"[{i+1}] {source_text}")
            print("--------------------------------------------")
