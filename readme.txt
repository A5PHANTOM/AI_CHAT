# 💬 AI Chat Application (Intern Task)

This is a Flask-based chat application that integrates:
- 🧠 **Hybrid RAG (Retrieval-Augmented Generation)** using a PDF document + Google Gemini AI
- 💾 **MongoDB Atlas** for message storage
- ⚡ **Redis Cloud** for caching recent messages
- 🌐 **Tailwind CSS frontend** for a simple, premium UI

The app answers questions using the provided PDF context when relevant and provides general knowledge answers using Gemini when no relevant context is found.

---

## 🚀 Features
✅ Send and store chat messages  
✅ Retrieve recent messages (with Redis cache)  
✅ Ask AI questions (hybrid RAG + fallback to general knowledge)  
✅ Simple and responsive frontend with Tailwind CSS  

---

## 🛠 Tech stack
- **Flask**
- **MongoDB Atlas**
- **Redis Cloud**
- **Google Gemini API (via google-generativeai)**
- **LangChain (for text splitting)**
- **PyPDF2 (for PDF parsing)**
- **Tailwind CSS**

---

## ⚡ Setup instructions

### 1️⃣ Clone this repository
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

