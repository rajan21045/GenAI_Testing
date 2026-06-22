import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
from pypdf import PdfReader


# Load env
load_dotenv()

API_KEY = os.getenv("groq_api_key")

client = Groq(api_key=API_KEY)


st.set_page_config(
    page_title="PDF Question Answering",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI PDF Question Answering System")


# Store PDF text
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""


uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)


# Extract PDF text
if uploaded_file:

    if st.button("Process PDF"):

        with st.spinner("Reading PDF..."):

            reader = PdfReader(uploaded_file)

            text = ""

            for page in reader.pages:
                text += page.extract_text() or ""

            st.session_state.pdf_text = text

        st.success("PDF processed successfully!")


# Question section

if st.session_state.pdf_text:

    question = st.text_input(
        "Ask a question from your PDF"
    )

    if st.button("Ask"):

        if not question.strip():
            st.warning(
                "Please enter a question"
            )
            st.stop()

        prompt = f"""
You are a document question answering assistant.

Answer the user question ONLY from the provided PDF content.

If the answer is not present in the document,
say:
"I could not find this information in the PDF."


PDF CONTENT:
{st.session_state.pdf_text}

Instructions:
- Provide a clear and concise answer based on the PDF content.
- If the answer is not in the PDF, respond with "I could not find this information in the PDF."


QUESTION:
{question}


Answer:
"""

        with st.spinner("Thinking..."):

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
            )

            answer = response.choices[0].message.content

        st.subheader("Answer")

        st.write(answer)