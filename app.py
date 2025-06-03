from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Journalist, Interaction
from ai_persona import persona_response
import os

app = Flask(__name__)
engine = create_engine('sqlite:///pr_platform.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.before_request
def log_server_info():
    host = request.host.split(':')[0]
    port = request.host.split(':')[1] if ':' in request.host else '80'
    app.logger.info(f"🚀 Flask is running at http://{host}:{port}")

@app.route("/", methods=["GET", "POST"])
def index():
    session = Session()
    journalists = session.query(Journalist).all()
    response = ""
    selected_journalist = None
    pitch = ""
    if request.method == "POST":
        pitch = request.form['pitch']
        journalist_id = int(request.form['journalist'])
        selected_journalist = session.query(Journalist).get(journalist_id)
        response = persona_response(selected_journalist, pitch)
        interaction = Interaction(journalist_id=journalist_id, pitch=pitch, response=response)
        session.add(interaction)
        session.commit()
    return render_template("index.html", journalists=journalists, response=response, selected=selected_journalist, pitch=pitch)

@app.route('/arch')
def arch():
    mmd_folder = os.path.join(app.root_path, 'mmd')
    diagrams = []

    for filename in os.listdir(mmd_folder):
        if filename.endswith('.mmd'):
            with open(os.path.join(mmd_folder, filename), 'r', encoding='utf-8') as f:
                diagrams.append(f.read())

    return render_template("index.html", diagrams=diagrams)

if __name__ == "__main__":
    app.run(debug=True)