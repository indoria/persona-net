import random
import spacy
from transformers import pipeline

# Load spaCy for NER and basic NLP
nlp = spacy.load("en_core_web_sm")
# Transformers summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")

def extract_topics(pitch_text):
    doc = nlp(pitch_text)
    topics = [ent.text for ent in doc.ents if ent.label_ in ("ORG", "PRODUCT", "PERSON")]
    return topics if topics else ["your topic"]

def persona_response(journalist, pitch_text, conversation_history=None):
    topics = extract_topics(pitch_text)
    try:
        summary = summarizer(pitch_text, max_length=32, min_length=10, do_sample=False)[0]['summary_text']
    except Exception:
        summary = pitch_text[:50] + "..."
    interests = journalist.interests.split(',')

    starter = "From what I userstand : " + summary + "<br />"

    templates = [
        f"{starter} <br> I'm interested in your pitch about {' and '.join(topics)}. Could you elaborate on how this relates to {random.choice(interests).strip()}?",
        f"{starter} <br> As someone who writes in a {journalist.style} style, I find your product intriguing. What sets it apart from others?",
        f"{starter} <br> Thank you for reaching out. Can you provide more background on your target audience for this launch?",
        f"{starter} <br> This sounds interesting, especially since I cover {', '.join(interests)}. What makes this newsworthy right now?"
    ]
    # Use conversation history for future expansion
    return random.choice(templates)