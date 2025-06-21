import google.generativeai as genai
from langchain.text_splitter import CharacterTextSplitter
from PyPDF2 import PdfReader


genai.configure(api_key="AIzaSyD7AsWA8k_waSVS3DoF1XUNQaiBpjvsdso")  

# Load 
def load_pdf_chunks(pdf_path):
    reader = PdfReader(pdf_path)
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() or ""
    
    text_splitter = CharacterTextSplitter(separator="\n", chunk_size=1000, chunk_overlap=100)
    texts = text_splitter.split_text(raw_text)
    return texts


def find_relevant_chunks(chunks, query):
    query_lower = query.lower()
    relevant = [chunk for chunk in chunks if any(word in chunk.lower() for word in query_lower.split())]
    return relevant[:3]  # Return top 3 matches

#answering
def hybrid_rag_answer(chunks, query):
    model = genai.GenerativeModel("gemini-1.5-flash")
    relevant_chunks = find_relevant_chunks(chunks, query)

    try:
        if relevant_chunks:
            # Build RAG prompt
            context = "\n\n".join(relevant_chunks)
            prompt = f"Answer the question based on this context:\n\n{context}\n\nQuestion: {query}\nAnswer:"
            response = model.generate_content(prompt)
        else:
            response = model.generate_content(query)

        return response.text.strip()

    except Exception as e:
        print(f"Error generating content: {e}")
        return "Sorry, AI could not generate a response at this time."
