# 🤖 AI PDF Chatbot (LangChain + Streamlit + OpenAI)

This project is a simple and powerful **PDF Question Answering Chatbot** built with [LangChain](https://www.langchain.com/), [OpenAI](https://platform.openai.com/), and [Streamlit](https://streamlit.io/). It lets you upload a PDF document and ask questions about its content — using embeddings and semantic search powered by FAISS and GPT.

---

## 📸 Demo Screenshot

![alt text](<Screenshot 2025-08-01 at 4.47.24 PM.png>)

---

## 🚀 Features

- 🗂 Upload any PDF document
- 🤔 Ask questions in plain English
- 🔍 Retrieves relevant document chunks via FAISS vector store
- 🧠 Uses OpenAI LLM to generate accurate answers
- 🧱 Built using LangChain's modular components
- 🌐 Streamlit interface for interactive use

---

## 📁 Project Structure

```bash
AI_PDF_Chatbot/
├── app.py           # Streamlit frontend
├── qa_model.py      # LangChain backend logic (vector store + chain)
├── requirements.txt # All dependencies
├── .env.example     # Template for environment variables
├── .gitignore       # Files to ignore in Git
└── README.md        # This file
