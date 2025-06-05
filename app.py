from flask import Flask, render_template, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Journalist, Interaction
from ai_persona import persona_response
import os

app = Flask(__name__)

engine = create_engine('sqlite:///pr_platform.db', future=True, echo=False)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(engine, future=True))

@app.route("/", methods=["GET"])
def index():
    with Session() as session:
        journalists = session.query(Journalist).all()
        return render_template("index.html", journalists=journalists)

@app.route("/query_persona", methods=["POST"])
def query_persona():
    data = request.get_json()
    pitch = data.get('pitch', '')
    journalist_ids = data.get('journalists', [])
    responses = []
    with Session() as session:
        for jid in journalist_ids:
            journalist = session.get(Journalist, int(jid))  # SQLAlchemy 2.0: use session.get()
            if journalist:
                resp = persona_response(journalist, pitch)
                interaction = Interaction(journalist_id=journalist.id, pitch=pitch, response=resp)
                session.add(interaction)
                responses.append({
                    'name': journalist.name,
                    'response': resp
                })
        session.commit()
    return jsonify({'responses': responses})

@app.route('/arch')
def arch():
    mmd_folder = os.path.join(app.root_path, 'mmd')
    diagrams = []

    for filename in os.listdir(mmd_folder):
        if filename.endswith('.mmd'):
            with open(os.path.join(mmd_folder, filename, ), 'r', encoding='utf-8') as f:
                diagrams.append(f.read())

    return render_template("arch.html", diagrams=diagrams)

@app.route('/plan')
def timeline():
    return render_template("timeline.html")

@app.route('/persona')
def persona():
    persona_folder = os.path.join(app.root_path, 'doc/persona')
    personas = []

    for filename in os.listdir(persona_folder):
        if filename.endswith('.json'):
            with open(os.path.join(persona_folder, filename), 'r', encoding='utf-8') as f:
                personas.append({
                    'name': filename[:-5],  # Remove .json extension
                    'content': f.read()
                })

    return render_template("persona.html", personas=personas)

if __name__ == "__main__":
    app.run(debug=True)