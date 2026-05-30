import streamlit as st
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
from dotenv import load_dotenv
from io import BytesIO
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import boto3
import numpy as np
import os

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
aws_region = os.getenv("AWS_REGION")
bucket_name = os.getenv("S3_BUCKET_NAME")

st.set_page_config(
    page_title="Document Chat Assistant",
    page_icon="💬",
    layout="wide"
)

if not groq_api_key:
    st.error("GROQ_API_KEY not found in .env file.")
    st.stop()

if not aws_access_key or not aws_secret_key or not aws_region or not bucket_name:
    st.error("AWS credentials missing in .env file.")
    st.stop()

client = Groq(api_key=groq_api_key)

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region
)


def upload_to_s3(file_bytes, file_name):
    s3.upload_fileobj(
        BytesIO(file_bytes),
        bucket_name,
        file_name
    )


def get_ai_answer(question, context):
    completion = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a helpful document assistant. "
                    "Answer only using the provided context. "
                    "If the answer is not found, say: "
                    "'I could not find this information in the uploaded document.'"
                )
            },
            {
                "role": "user",
                "content": f"""
Context:
{context}

Question:
{question}
"""
            }
        ]
    )

    return completion.choices[0].message.content


def retrieve_relevant_chunks(chunks, question, top_k=2):
    documents = chunks + [question]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(documents)

    chunk_vectors = vectors[:-1]
    question_vector = vectors[-1]

    similarities = cosine_similarity(
        question_vector,
        chunk_vectors
    )[0]

    top_indices = np.argsort(similarities)[::-1][:top_k]

    return [chunks[i] for i in top_indices]


st.markdown("""
<style>
.hero {
    padding: 30px;
    border-radius: 20px;
    background: rgba(255,255,255,0.04);
    border: 1px solid #2d3748;
    margin-bottom: 20px;
}

.small-text {
    color: #b0b0b0;
    font-size: 15px;
}

.answer-box {
    padding: 20px;
    border-radius: 14px;
    background: rgba(255,255,255,0.08);
    border-left: 5px solid #2563eb;
    line-height: 1.8;
    margin-top: 10px;
    color: white;
}

.source-box {
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #2d3748;
    background: rgba(255,255,255,0.06);
    margin-bottom: 12px;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>💬 AI Document Intelligence Chatbot</h1>
    <p class="small-text">
        Upload a PDF, store it in AWS S3, and ask questions using a lightweight RAG workflow.
    </p>
</div>
""", unsafe_allow_html=True)

left_col, right_col = st.columns([1, 1.5])

with left_col:
    st.markdown("### Upload Document")

    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type="pdf"
    )

    st.markdown("### Ask a Question")

    user_question = st.text_input(
        "Enter your question",
        placeholder="Example: What are the key points in this document?"
    )

    ask_button = st.button("Ask Document")

with right_col:
    st.markdown("### AI Response")

    if uploaded_file:
        file_bytes = uploaded_file.getvalue()

        try:
            upload_to_s3(file_bytes, uploaded_file.name)
            st.success("Document uploaded to AWS S3 successfully")
        except Exception as e:
            st.error(f"S3 Upload Failed: {e}")

        pdf_reader = PdfReader(BytesIO(file_bytes))
        text = ""

        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=700,
            chunk_overlap=120
        )

        chunks = splitter.split_text(text)

        st.success(f"Document ready • {len(chunks)} sections indexed")

        if ask_button and user_question:
            relevant_chunks = retrieve_relevant_chunks(
                chunks,
                user_question,
                top_k=2
            )

            context = "\n\n".join(relevant_chunks)

            with st.spinner("Generating answer..."):
                answer = get_ai_answer(user_question, context)

            st.markdown("### Generated Answer")

            st.markdown(
                f"""
                <div class="answer-box">
                    {answer}
                </div>
                """,
                unsafe_allow_html=True
            )

            with st.expander("View Retrieved Context"):
                for i, chunk in enumerate(relevant_chunks, start=1):
                    st.markdown(f"**Source Chunk {i}**")
                    st.markdown(
                        f"""
                        <div class="source-box">
                            {chunk}
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
    else:
        st.info("Upload a PDF to begin.")