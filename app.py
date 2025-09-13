import streamlit as st
import os
import sys
import re

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from src.query_text import rag_query

st.set_page_config(page_title="RAG Application", layout="wide")
st.title("RAG-powered Q&A System")

st.write("Ask a Question about the Indexed articles and get a grounded answer")
user_question = st.text_input("Enter your Question:", key="user_question")

if st.button("Get Answer"):
    if user_question:
        with st.spinner("Processing your Request..."):
            answer, cited_sources = rag_query(user_question)

            st.subheader("Answer")
            st.write(answer)

            if cited_sources:
                st.subheader("Sources")

                # Deduplicate while preserving order
                seen = set()
                unique_sources = []
                for idx, src in cited_sources:
                    if idx not in seen:
                        seen.add(idx)
                        # truncate long source text to avoid overflow
                        short_src = src[:400] + "..." if len(src) > 400 else src
                        unique_sources.append((idx, short_src))

                # Display clean sources
                for idx, src in unique_sources:
                    st.markdown(f"**[{idx}]** {src}")

            else:
                st.info("No sources were used to generate this answer.")
    else:
        st.warning("Please enter a Question.")
