import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough

load_dotenv()

# Initialize embedding model
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

# Format retrieved docs
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# Build or load FAISS vector store
def load_or_create_vector_store(pdf_path, faiss_path="faiss_index"):
    try:
        if os.path.exists(faiss_path):
            return FAISS.load_local(faiss_path, embeddings, allow_dangerous_deserialization=True)
    except Exception as e:
        print(f"[Error] Failed to load FAISS index: {e}")
        print("[Info] Rebuilding index from PDF...")

    try:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = splitter.split_documents(documents)

        vector_store = FAISS.from_documents(docs, embeddings)
        vector_store.save_local(faiss_path)
        return vector_store
    except Exception as e:
        print(f"[Error] Failed to process PDF or create FAISS index: {e}")
        raise  # Let the app crash if this fails — it's a critical error

# Create LangChain final QA chain
def build_qa_chain(vector_store):
    try:
        retriever = vector_store.as_retriever(search_type="mmr", search_kwargs={"k": 3})

        prompt_template = """
You are an intelligent assistant that answers questions using only the information provided in the context below.

---------------------
Context:
{context}
---------------------

Answer the following question strictly based on the above context. 
If the answer is not present in the context, say "The answer is not available in the document."

Question: {question}
Answer:
"""
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])
        llm = ChatOpenAI()
        parser = StrOutputParser()

        parallel_chain = RunnableParallel({
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        })

        return parallel_chain | prompt | llm | parser
    except Exception as e:
        print(f"[Error] Failed to build QA chain: {e}")
        raise
