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

if __name__ == "__main__":
    app.run(debug=True)