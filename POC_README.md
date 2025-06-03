# AI-Powered PR Platform POC

## Overview

This Proof of Concept (POC) demonstrates an AI/ML-driven PR platform that analyzes pitches and generates personalized responses from simulated PR journalist personas. The system combines a knowledge graph, NLP, and a simple UI to streamline and enhance PR campaigns.

---

## Architecture

**Components:**
1. **AI Persona Engine** – Generates personalized responses using PR journalist profiles.
2. **Knowledge Graph** – Stores PR journalist persona data (interests, style, history).
3. **NLP Module** – Analyzes the pitch and user responses using spaCy/transformers.
4. **User Interface** – Simple web form to input pitch and view persona responses.
5. **Database** – SQLite for demonstration; stores journalists, persona data, and interactions.

---

## Tech Stack

- **Backend:** Python, Flask
- **NLP/ML:** spaCy, transformers (HuggingFace), NLTK, scikit-learn
- **Database:** SQLite (ORM: SQLAlchemy)
- **Frontend:** HTML/CSS/JavaScript (Flask templates)
- **OS:** Linux/Windows

---

## 1. Project Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install flask sqlalchemy spacy transformers nltk
python -m spacy download en_core_web_sm
```

---

## 2. Database Schema and Knowledge Graph

```python name=models.py
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Journalist(Base):
    __tablename__ = 'journalists'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    interests = Column(Text)  # e.g., "tech, startups, AI"
    style = Column(Text)      # e.g., "formal, inquisitive"
    sample_articles = Column(Text)  # For future expansion

class Interaction(Base):
    __tablename__ = 'interactions'
    id = Column(Integer, primary_key=True)
    journalist_id = Column(Integer, ForeignKey('journalists.id'))
    pitch = Column(Text)
    response = Column(Text)
    journalist = relationship("Journalist")
```

---

## 3. AI Persona Engine

```python name=ai_persona.py
import random
import spacy
from transformers import pipeline

nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def extract_topics(pitch_text):
    doc = nlp(pitch_text)
    topics = [ent.text for ent in doc.ents if ent.label_ in ("ORG", "PRODUCT", "PERSON")]
    return topics

def persona_response(journalist, pitch_text, conversation_history=None):
    topics = extract_topics(pitch_text)
    summary = summarizer(pitch_text, max_length=32, min_length=10, do_sample=False)[0]['summary_text']
    # Simple rules-based + persona flavoring for demonstration
    templates = [
        f"I'm interested in your pitch about {' and '.join(topics)}. Could you elaborate on how this relates to {random.choice(journalist.interests.split(','))}?",
        f"As someone who writes in a {journalist.style} style, I find your product intriguing. What sets it apart from others?",
        f"Thank you for reaching out. Can you provide more background on your target audience for this launch?"
    ]
    return random.choice(templates)
```

---

## 4. Flask App with UI

```python name=app.py
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Journalist, Interaction
from ai_persona import persona_response

app = Flask(__name__)
engine = create_engine('sqlite:///pr_platform.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route("/", methods=["GET", "POST"])
def index():
    session = Session()
    journalists = session.query(Journalist).all()
    response = ""
    selected_journalist = None
    if request.method == "POST":
        pitch = request.form['pitch']
        journalist_id = int(request.form['journalist'])
        selected_journalist = session.query(Journalist).get(journalist_id)
        response = persona_response(selected_journalist, pitch)
        interaction = Interaction(journalist_id=journalist_id, pitch=pitch, response=response)
        session.add(interaction)
        session.commit()
    return render_template("index.html", journalists=journalists, response=response, selected=selected_journalist)

if __name__ == "__main__":
    app.run(debug=True)
```

---

```html name=templates/index.html
<!DOCTYPE html>
<html>
<head>
    <title>PR AI Persona POC</title>
</head>
<body>
    <h1>PR Journalist AI Persona Demo</h1>
    <form method="post">
        <label for="pitch">Enter your pitch:</label><br>
        <textarea name="pitch" rows="4" cols="60"></textarea><br>
        <label for="journalist">Choose a journalist:</label>
        <select name="journalist">
            {% for j in journalists %}
                <option value="{{j.id}}" {% if selected and selected.id == j.id %}selected{% endif %}>{{j.name}}</option>
            {% endfor %}
        </select><br>
        <button type="submit">Submit</button>
    </form>
    {% if response %}
        <h2>AI Persona Response:</h2>
        <p>{{response}}</p>
    {% endif %}
</body>
</html>
```

---

## 5. Populate Database

```python name=populate_db.py
from models import Base, Journalist
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///pr_platform.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

journalists = [
    Journalist(name="Alice Smith", interests="tech,ai,startups", style="inquisitive,neutral"),
    Journalist(name="Bob Johnson", interests="consumer electronics,gadgets,innovation", style="formal,analytical"),
    Journalist(name="Carol Lee", interests="marketing,branding,social media", style="conversational,engaging"),
]
session.add_all(journalists)
session.commit()
```

---

## 6. Testing and Debugging

- Unit test AI persona responses for different pitches
- Test UI and database integration
- Validate multi-turn conversation (extend Interaction model if needed)

---

## 7. Report and Presentation

**Report Outline:**
- Introduction & Business Value
- Technical Approach
- Architecture Diagrams
- Implementation Details
- Sample Screenshots & Interactions
- Evaluation & Next Steps

**Presentation:**
- Slides summarizing the above, with demo screenshots and key findings

---

## Next Steps for Full Platform

- Expand the knowledge graph (use Neo4j for production scale)
- Add authentication/user management
- Utilize more sophisticated ML for persona adaptation (fine-tuned LLMs)
- Enhance UI/UX (React front-end, chat-like interface)
- Deploy to cloud (AWS, Azure, GCP)

---

## Example Use Case (Demo Walkthrough)

1. User enters a pitch:  
   _"We are launching a smart home device that uses AI to personalize user experience."_

2. Selects "Alice Smith" persona.

3. **AI Response:**  
   _"I'm interested in your pitch about smart home device and AI. Could you elaborate on how this relates to startups?"_

4. User can continue the conversation, and the AI persona will adapt responses.

---

## Evaluation Criteria

- Technical correctness (API, persona logic, NLP)
- Efficiency (response time, DB integration)
- Quality of responses (coherence, persona consistency)
- Quality of documentation and presentation

---

## PR pitch components
Key elements of an effective PR pitch:
Compelling Subject Line:
A strong subject line is crucial to grab the journalist's attention and encourage them to open the pitch.
Newsworthy Angle:
The pitch should highlight why the story is relevant and timely for the media outlet's audience.
Conciseness:
The message should be brief and to the point, making it easy for journalists to quickly understand the key details.
Clear Call to Action:
Specify what you want the journalist to do, such as schedule an interview, review a product, or cover an event.
Multimedia:
Include relevant visuals like photos, videos, or infographics to make the pitch more engaging.
Expert Availability:
Offer access to company representatives or experts for interviews to add credibility to the story.
Data and Research:
Support your pitch with relevant data and research findings to strengthen your argument.
Targeted Approach:
Research the journalist's beat and tailor the pitch to their specific interests and audience.
Online Media Kit:
Include a link to an online media kit with additional information about the company, product, or event.
Follow-Up:
After sending the pitch, follow up with journalists to ensure they received it and answer any questions they may have.