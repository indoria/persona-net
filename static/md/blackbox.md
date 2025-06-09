


"""
Step-by-step guide to implement an AI Persona system with RAG using:
- Python & Flask for the web backend
- OpenAI API (GPT-4) for generation and embeddings
- LangChain for orchestration
- Pinecone as vector database (can be replaced by others like Weaviate, FAISS)

This single file provides a minimal Flask app exposing an API endpoint to chat with the AI persona.
It loads persona data, indexes it into Pinecone, and performs Retrieval Augmented Generation on user queries.

Replace placeholders with your OpenAI and Pinecone credentials before running.

To run:  
  pip install flask openai langchain pinecone-client  
  python ai_persona_flask_app.py  
Then open http://localhost:5000 in your browser or use API clients.

"""

```python
import os
import json
from flask import Flask, request, render_template_string, jsonify
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
import pinecone

# === CONFIGURATION ===
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
PINECONE_ENV = os.environ.get("PINECONE_ENV")  # e.g. "us-west1-gcp"

PERSONA_TEXT_FILE = "persona_data.txt"  # Text corpus of the real-life person (one large text file)

INDEX_NAME = "ai-persona-index"

app = Flask(__name__)

# === HTML Template for frontend UI following minimal elegant design guidelines ===
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>AI Persona Chat</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@600&display=swap');
  body { background: #ffffff; margin:0; font-family: 'Poppins', sans-serif; color: #6b7280; }
  header { position: sticky; top:0; background: white; border-bottom: 1px solid #e5e7eb; padding: 1rem 2rem; display:flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
  .logo { font-weight: 700; font-size: 1.5rem; color: #111827;}
  main { max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
  h1 { font-size: 3rem; font-weight: 700; color: #111827; margin-bottom: 0.5rem; }
  p { font-size: 1.125rem; margin-bottom: 2rem; }
  #chat { background: #f9fafb; border-radius: 12px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); padding: 1rem; min-height: 400px; overflow-y: auto; }
  .message { margin-bottom: 1.5rem; max-width: 80%; padding: 0.75rem 1rem; border-radius: 0.75rem; }
  .user { background: #111827; color: white; margin-left: auto; transform: translateX(5px);}
  .bot { background: white; box-shadow: 0 1px 3px rgba(0,0,0,0.1); color: #111827;}
  form { margin-top: 1rem; display: flex; gap: 0.75rem; }
  input[type=text] { flex-grow: 1; padding: 0.75rem 1rem; border: 1px solid #d1d5db; border-radius: 0.75rem; font-size: 1rem; color: #111827; }
  button { background: #111827; color: white; border: none; padding: 0 1.5rem; border-radius: 0.75rem; font-weight: 600; cursor: pointer; transition: background-color 0.3s ease;}
  button:hover { background: #374151; }
  @media (max-width: 600px) {
    h1 { font-size: 2.25rem; }
    main { margin: 1rem; }
  }
</style>
</head>
<body>
<header>
  <div class="logo">AI Persona</div>
</header>
<main>
  <h1>Chat with the AI Persona</h1>
  <p>Ask anything, and the AI will respond just like the real person!</p>
  <div id="chat"></div>
  <form id="chat-form">
    <input type="text" id="user-input" placeholder="Type your message..." autocomplete="off" />
    <button type="submit">Send</button>
  </form>
</main>
<script>
  const chat = document.getElementById('chat');
  const form = document.getElementById('chat-form');
  const input = document.getElementById('user-input');

  function appendMessage(text, className) {
    const div = document.createElement('div');
    div.textContent = text;
    div.className = 'message ' + className;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userText = input.value.trim();
    if (!userText) return;
    appendMessage(userText, 'user');
    input.value = '';
    appendMessage('...', 'bot');
    const lastBotMessage = chat.querySelector('.message.bot:last-child');

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ message: userText })
      });
      const data = await response.json();
      lastBotMessage.textContent = data.response;
    } catch (error) {
      lastBotMessage.textContent = "Oops! Something went wrong.";
    }
  });
</script>
</body>
</html>
"""

# === Initialize Pinecone and LangChain only once ===
pinecone_initialized = False
vectorstore = None
chain = None

def initialize_vectorstore_and_chain():
    global pinecone_initialized, vectorstore, chain
    if pinecone_initialized:
        return

    # Initialize Pinecone client
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)

    # Check if index exists, create if not
    if INDEX_NAME not in pinecone.list_indexes():
        pinecone.create_index(INDEX_NAME, dimension=1536, metric="cosine")

    # Connect to index
    index = pinecone.Index(INDEX_NAME)

    # Create LangChain vectorstore wrapper for Pinecone
    embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    vectorstore = Pinecone(index, embeddings.embed_query, "text")

    # Load persona data if index empty and index embeddings
    index_info = index.describe_index_stats()
    if index_info['total_vector_count'] == 0:
        print("Index empty. Loading and indexing persona data...")
        with open(PERSONA_TEXT_FILE, "r", encoding="utf-8") as f:
            text = f.read()
        # Split text into smaller chunks for embeddings (basic split by paragraphs here - can improve)
        docs = [doc.strip() for doc in text.split('\n\n') if doc.strip()]
        # Prepare metadata for chunking if needed (skipped here)
        # Add to vectorstore
        from langchain.docstore.document import Document
        documents = [Document(page_content=d) for d in docs]
        vectorstore.add_documents(documents)
        print(f"Indexed {len(documents)} documents.")

    # Create a RetrievalQA chain with OpenAI LLM and Pinecone retriever
    llm = OpenAI(model_name="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k":4})
    chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    pinecone_initialized = True
    print("Pinecone and LangChain initialization complete.")

# === Flask Routes ===

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    if not user_message:
        return jsonify({"response": "Please enter a message."})

    if not pinecone_initialized:
        initialize_vectorstore_and_chain()

    # Run RAG: Pass user message to LangChain RetrievalQA chain
    try:
        response = chain.run(user_message)
    except Exception as e:
        response = "Sorry, there was an error generating the response."
        print(f"Error during chain.run: {e}")

    return jsonify({"response": response})

# === Run Flask app ===
if __name__ == "__main__":
    # Validate env variables presence before starting
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY env variable not set")
    if not PINECONE_API_KEY or not PINECONE_ENV:
        raise RuntimeError("PINECONE_API_KEY and PINECONE_ENV env variables must be set")

    print("Starting AI Persona Flask app...")
    app.run(debug=True)

```

`AI_Persona_Google_Colab_Step_by_Step_Guide.md`
```md
# Step-by-Step Guide to Implement an AI Persona System on Google Colaboratory

This guide details how to build an AI persona system with Retrieval-Augmented Generation (RAG) using:

- OpenAI API (GPT-4) for generation and embeddings
- LangChain for orchestration
- A compatible vector database backend (using Pinecone here)
- Google Colab environment

The guide also suggests how to create a minimal, elegant UI inside the notebook following developer-friendly modern styling principles.

---

## 1. Setup Google Colab Environment

Open a new Google Colab notebook and install necessary libraries by running:

```python
!pip install --quiet openai langchain pinecone-client flask-ngrok
```

We use:
- `openai` and `langchain` for LLM orchestration
- `pinecone-client` as a managed vector database
- `flask-ngrok` for exposing a Flask app within the Colab environment (optional for UI)

---

## 2. Configure API Keys

In a new code cell, enter your OpenAI and Pinecone API keys securely:

```python
import os

# Set your API keys here (replace with your keys)
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
os.environ["PINECONE_API_KEY"] = "your-pinecone-api-key-here"
os.environ["PINECONE_ENV"] = "your-pinecone-env-here"  # e.g. "us-west1-gcp"
```

Make sure you keep your keys confidential. Colab allows environment variables per session.

---

## 3. Prepare Persona Data

Prepare a text corpus representing the real-life person. This could be transcripts, letters, articles, or social media posts.

You can upload a text file (.txt) using Colab's file upload:

```python
from google.colab import files
uploaded = files.upload()
```

Upload a file named `persona_data.txt` which contains the text data. This file will be used to generate embeddings.

---

## 4. Initialize Pinecone Vector Store and Create Embeddings

In a new cell, initialize Pinecone, create the index (if needed), read and chunk the persona data, generate embeddings, and upsert them into the index:

```python
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.docstore.document import Document

# Read environment variables
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENV = os.environ["PINECONE_ENV"]

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
index_name = "ai-persona-index"

# Create index if it doesn't exist
if index_name not in pinecone.list_indexes():
    pinecone.create_index(index_name, dimension=1536, metric="cosine")
index = pinecone.Index(index_name)

# Load persona data
with open("persona_data.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Basic chunking by paragraphs (adjust as needed)
documents = [Document(page_content=chunk) for chunk in text.split('\n\n') if chunk.strip()]

# Set up embeddings model
embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

# Wrap Pinecone vector store
vectorstore = Pinecone(index, embeddings.embed_query, "text")

# Add documents to Pinecone if index is empty
stats = index.describe_index_stats()
if stats['total_vector_count'] == 0:
    vectorstore.add_documents(documents)
    print(f"Indexed {len(documents)} persona documents.")
else:
    print(f"Index already contains {stats['total_vector_count']} vectors.")
```

---

## 5. Setup Retrieval QA Chain with LangChain and OpenAI

Create a RetrievalQA chain combining the vector retriever and the OpenAI GPT-4 LLM:

```python
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

# Create retriever from vectorstore
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})

# Initialize OpenAI LLM
llm = OpenAI(model_name="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)

# Create RetrievalQA chain
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
```

---

## 6. Interactive Chat Interface in Colab

You can use a simple input/output loop directly in Colab or use a minimal Flask app exposed via `flask-ngrok` for a nicer UI.

### a) Minimal Colab input loop:

```python
print("Chat with your AI Persona (type 'exit' to quit):")
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    answer = qa_chain.run(query)
    print("AI Persona:", answer)
```

### b) (Optional) Flask app exposed with ngrok for a simple web UI:

```python
from flask import Flask, request, jsonify, render_template_string
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
run_with_ngrok(app)  # starts ngrok when app.run() is called

html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>AI Persona Chat</title>
<style>
  body {background: #fff; font-family: Poppins, sans-serif; color: #6b7280; max-width: 700px; margin: 40px auto; padding: 20px;}
  h1 {font-weight: 700; font-size: 48px; color: #111827;}
  #chat {background: #f9fafb; border-radius: 12px; padding: 20px; min-height: 300px; box-shadow: 0 2px 6px rgba(0,0,0,0.05); overflow-y: auto;}
  .message {margin-bottom: 1rem; padding: 15px 20px; border-radius: 0.75rem;}
  .user {background: #111827; color: white; text-align: right;}
  .bot {background: white; color: #111827; box-shadow: 0 1px 3px rgba(0,0,0,0.1);}
  input[type=text] {width: 70%; padding: 1rem; border-radius: 12px; border: 1px solid #d1d5db; font-size: 16px;}
  button {background: #111827; color: white; border: none; padding: 1rem 2rem; border-radius: 12px; margin-left: 10px; font-weight: 600; cursor: pointer;}
  button:hover {background: #374151;}
  form {margin-top: 20px; display: flex; justify-content: center;}
</style>
</head>
<body>
  <h1>AI Persona Chat</h1>
  <div id="chat"></div>
  <form id="chat-form">
    <input id="user-input" autocomplete="off" placeholder="Say something..." />
    <button type="submit">Send</button>
  </form>
<script>
  const chatDiv = document.getElementById('chat');
  const chatForm = document.getElementById('chat-form');
  const userInput = document.getElementById('user-input');

  function appendMessage(text, className) {
    const div = document.createElement('div');
    div.className = 'message ' + className;
    div.textContent = text;
    chatDiv.appendChild(div);
    chatDiv.scrollTop = chatDiv.scrollHeight;
  }

  chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const text = userInput.value.trim();
    if (text === '') return;
    appendMessage(text, 'user');
    userInput.value = '';
    appendMessage('...', 'bot');
    const lastBotMessage = chatDiv.querySelector('.message.bot:last-child');

    const response = await fetch('/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({query: text})
    });
    const data = await response.json();
    lastBotMessage.textContent = data.response;
  });
</script>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/chat", methods=["POST"])
def chat_api():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"response": "Please enter a query."})
    try:
        answer = qa_chain.run(query)
    except Exception as e:
        answer = "Sorry, I couldn't process that."
        print("Error:", e)
    return jsonify({"response": answer})

# To run within Colab:
# app.run()
```

Run the last line in a Colab cell to start:

```python
app.run()
```

You will get a public ngrok URL to interact with the AI Persona chat web interface.

---

## 7. Improvements and Customizations

- **Better chunking:** Use more advanced document splitting from LangChain for cleaner semantic chunks.  
- **Metadata:** Add timestamps, source info to embeddings for refined retrieval.  
- **Persona prompt tuning:** Improve prompt engineering to better mimic the real-life person's voice and behavior.  
- **Conversation memory:** Maintain session state/history for context-aware responses.  
- **UI polish:** Add animations, theme toggle, and loading skeletons following the minimal and elegant design principles outlined above.

---

## Summary

Using Google Colab you can rapidly prototype a full AI persona system:

- Setup environment and credentials  
- Upload persona data and embed it in Pinecone or other vector DB  
- Build a LangChain RetrievalQA chain with OpenAI LLM  
- Interact via direct input loop or Flask web app with simple, elegant UI  
- Iteratively improve for production use, adding memory, richer UI, and monitoring

---


```

## persona.ipynb
```python
# 1. Install Required Libraries
!pip install --quiet openai langchain pinecone-client

# 2. Configure API Keys
import os

# Replace these strings with your actual API keys before running
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
os.environ["PINECONE_API_KEY"] = "your-pinecone-api-key-here"
os.environ["PINECONE_ENV"] = "your-pinecone-environment-here"  # e.g. "us-west1-gcp"

# 3. Upload Persona Data
from google.colab import files
uploaded = files.upload()
# Upload persona_data.txt file representing the real-life person's text corpus

# 4. Initialize Pinecone and Index Persona Data
import pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone
from langchain.docstore.document import Document

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
PINECONE_API_KEY = os.environ["PINECONE_API_KEY"]
PINECONE_ENV = os.environ["PINECONE_ENV"]

pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENV)
INDEX_NAME = "ai-persona-index"
if INDEX_NAME not in pinecone.list_indexes():
    pinecone.create_index(INDEX_NAME, dimension=1536, metric="cosine")
index = pinecone.Index(INDEX_NAME)

with open("persona_data.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Split persona text into paragraphs as basic chunks
chunks = [chunk.strip() for chunk in text.split('\n\n') if chunk.strip()]
documents = [Document(page_content=chunk) for chunk in chunks]

embedding_model = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
vectorstore = Pinecone(index, embedding_model.embed_query, "text")

stats = index.describe_index_stats()
if stats['total_vector_count'] == 0:
    vectorstore.add_documents(documents)
    print(f"Indexed {len(documents)} persona documents.")
else:
    print(f"Index already contains {stats['total_vector_count']} vectors.")

# 5. Setup RetrievalQA Chain with LangChain and OpenAI
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 4})
llm = OpenAI(model_name="gpt-4", temperature=0, openai_api_key=OPENAI_API_KEY)
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

print("QA chain is ready. You can start querying.")

# 6. Query the AI Persona in the Notebook
print("Start a conversation with your AI Persona! Type 'exit' to quit.")
while True:
    query = input("You: ")
    if query.lower() == "exit":
        print("Goodbye!")
        break
    try:
        answer = qa_chain.run(query)
        print("AI Persona:", answer)
    except Exception as e:
        print("Error generating response:", e)

```