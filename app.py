import os
import shutil
import streamlit as st
from dotenv import load_dotenv
from qa_model import load_or_create_vector_store, build_qa_chain

load_dotenv()

st.set_page_config(page_title="PDF Q&A App")
st.title("📄 PDF Question Answering App")
st.write("Upload a PDF file and ask a question based on its content.")

# File Upload
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")
a
if uploaded_file:
    pdf_path = "uploaded.pdf"

    try:
        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.read())
    except Exception as e:
        st.error(f"❌ Failed to save uploaded file: {e}")

    faiss_path = "faiss_index"

    try:
        vector_store = load_or_create_vector_store(pdf_path, faiss_path)
        qa_chain = build_qa_chain(vector_store)
    except Exception as e:
        st.error(f"❌ Error during vector store setup: {e}")
        st.stop()

    question = st.text_input("Ask a question about the uploaded document:")

    if question:
        with st.spinner("Thinking..."):
            try:
                answer = qa_chain.invoke(question)
                st.success("Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ Failed to generate answer: {e}")

    if st.button("Reset"):
        try:
            shutil.rmtree(faiss_path, ignore_errors=True)
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
            st.experimental_rerun()
        except Exception as e:
            st.error(f"❌ Failed to reset: {e}")
