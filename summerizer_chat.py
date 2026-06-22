import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Groq API Key
API_KEY = os.getenv("groq_api_key")

# Initialize Groq Client
client = Groq(api_key=API_KEY)

st.set_page_config(
    page_title="AI Text Summarizer",
    page_icon="📝",
    layout="wide"
)

st.title("📝 Groq AI Summarizer")

text = st.text_area(
    "Enter text to summarize",
    height=300
)

summary_type = st.selectbox(
    "Summary Length",
    ["Short", "Medium", "Detailed"]
)

if st.button("Generate Summary"):

    if not text.strip():
        st.warning("Please enter some text.")
        st.stop()

    prompt = f"""
    Summarize the following text.

    Summary Type: {summary_type}

    Text:
    {text}

    Instructions:
    - Short: 3-5 lines
    - Medium: 1 paragraph
    - Detailed: Key points and explanation
    """

    with st.spinner("Generating summary..."):

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        st.subheader("Summary")
        st.write(response.choices[0].message.content)