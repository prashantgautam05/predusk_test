import streamlit as st
from backend.ingest import ingest
from backend.rag import answer_query

st.set_page_config(page_title="Mini RAG App", layout="centered")

st.title("📄 Mini RAG Application")
st.write("Retrieval Augmented Generation using Streamlit")

# Document input
doc_text = st.text_area(
    "Paste document text (optional)",
    height=200
)

# Question input
query = st.text_input("Ask a question")

if st.button("Ask"):
    if not query:
        st.warning("Please enter a question")
    else:
        with st.spinner("Processing..."):
            if doc_text.strip():
                ingest(doc_text)

            answer, sources = answer_query(query)

        st.subheader("Answer")
        st.write(answer)

        if sources:
            st.subheader("Sources")
            for i, src in enumerate(sources, 1):
                st.markdown(f"**[{i}]** {src}")

