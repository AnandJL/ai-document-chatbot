# 💬 AI Document Chatbot

An AI-powered document chatbot that allows users to upload PDF documents, store them in AWS S3, and ask questions using a lightweight RAG (Retrieval-Augmented Generation) workflow powered by Groq LLM.

## 🚀 Features

* Upload PDF documents
* Store uploaded files in AWS S3
* Ask questions about uploaded documents
* Lightweight RAG pipeline for document retrieval
* Groq LLM integration for answer generation
* Streamlit-based interactive UI
* AWS EC2 deployment support
* Git & GitHub version control

---

## 🛠️ Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### AI / LLM

* Groq API (`llama-3.1-8b-instant`)

### Cloud Services

* AWS EC2
* AWS S3
* AWS IAM

### Libraries Used

* pypdf
* boto3
* scikit-learn
* groq
* streamlit
* python-dotenv
* numpy

---

## 📌 Project Architecture

User → Streamlit UI → PDF Upload → AWS S3
↓
Document Processing → Text Chunking → Retrieval
↓
Groq LLM → Answer Generation → UI Response

---

## 📂 Project Structure

```bash
ai-document-chatbot/
│── app.py
│── requirements.txt
│── .gitignore
│── README.md
│── .env (not included)
│── documents/
```

---

## ⚙️ Local Setup

### 1. Clone Repository

```bash
git clone https://github.com/AnandJL/ai-document-chatbot.git
cd ai-document-chatbot
```

### 2. Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file in the root directory.

Example:

```env
GROQ_API_KEY=your_groq_api_key

AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=ap-south-1

S3_BUCKET_NAME=your_bucket_name
```

---

## ☁️ AWS Setup

### Step 1 — Create IAM User

1. Open AWS Console
2. Go to IAM
3. Create a new IAM user
4. Attach permissions:

```text
AmazonS3FullAccess
```

5. Generate access keys

Copy:

* Access Key ID
* Secret Access Key

Add them to `.env`.

---

### Step 2 — Create S3 Bucket

1. Open AWS S3
2. Create a bucket
3. Copy bucket name
4. Add bucket name to `.env`

Example:

```env
S3_BUCKET_NAME=my-document-chatbot-bucket
```

---

## ▶️ Run Application

```bash
streamlit run app.py
```

Application runs on:

```text
http://localhost:8501
```

---

## ☁️ AWS EC2 Deployment

### 1. Launch EC2 Instance

Recommended:

* Ubuntu Server 24.04 LTS
* t3.micro / t2.micro

### 2. Configure Security Group

Add inbound rules:

| Type       | Port |
| ---------- | ---- |
| SSH        | 22   |
| Custom TCP | 8501 |

Source:

```text
0.0.0.0/0
```

### 3. SSH Into EC2

```bash
ssh -i your-key.pem ubuntu@your-public-ip
```

### 4. Clone Repository

```bash
git clone https://github.com/AnandJL/ai-document-chatbot.git
cd ai-document-chatbot
```

### 5. Create Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 6. Install Dependencies

```bash
pip install -r requirements.txt
```

### 7. Create `.env`

```bash
nano .env
```

Paste your credentials.

### 8. Run App

```bash
python -m streamlit run app.py --server.address 0.0.0.0
```

Access:

```text
http://your-public-ip:8501
```

---

## 🧠 RAG Workflow

1. User uploads a PDF
2. Text is extracted from document
3. Text is split into chunks
4. Relevant chunks are retrieved using TF-IDF similarity
5. Context is sent to Groq LLM
6. AI generates answer based on document context

---

## 📸 Screenshots

Add screenshots here later.

---

## 🔮 Future Improvements

* Chat history support
* Authentication system
* Better semantic retrieval
* Multi-document querying
* Persistent cloud deployment

---

## 👨‍💻 Author

**Anand JL**

GitHub: https://github.com/AnandJL
GitHub Repository: https://github.com/AnandJL/ai-document-chatbot

```
```
