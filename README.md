# PR AI Persona Platform – Proof of Concept

## Overview

This POC demonstrates an AI-powered PR platform that analyzes user pitches and generates realistic, personalized responses from PR journalist personas.

---

## Deployment Guide

### 1. Prerequisites

- Python 3.8+
- pip
- Git
- (Optional) Virtualenv

### 2. Clone & Setup

```bash
git clone <your-repo-url>
cd <your-repo-dir>
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm

pip show flask
python -m flask --version
```

### 3. Seed the Database

```bash
python seed_personas.py
```

### 4. Run the Application

```bash
python app.py
```
Visit: http://127.0.0.1:5000

---

## en_core_web_sm
en_core_web_sm is a small English language model in spaCy, a popular Python library for Natural Language Processing (NLP). It is a multi-task Convolutional Neural Network (CNN) trained on the OntoNotes dataset. 

## Data Acquisition & Annotation Guide

### Step 1: Acquire Persona Data

- Search for PR journalists on platforms like LinkedIn, Twitter, or media websites.
- Collect public info: Name, interests (topics they cover), writing style (formal, conversational, inquisitive), and links to sample articles.

### Step 2: Data Sanitization

- Remove any sensitive or private information.
- Ensure all collected data is publicly available and used in line with privacy policies.

### Step 3: Annotation

- Assign interests as comma-separated tags (e.g., "tech, startups, AI").
- Summarize writing style in 1–2 adjectives (e.g., "formal, analytical").
- Optionally, add sample article titles or headlines for context.

---

## Project Structure

```
.
├── app.py
├── ai_persona.py
├── models.py
├── seed_personas.py
├── requirements.txt
├── mmd/
│   └── mermaid diagrams
├── templates/
│   └── index.html
├── .gitignore
├── resources.md # A list of useful AI resources
├── POC_README.md
└── README.md
```

---

## Next Steps

- Expand persona database with more annotated journalists.
- Enhance persona model using ML fine-tuning.
- Improve UI for multi-turn conversation.
- Package for cloud deployment (e.g., Docker, AWS EB).
