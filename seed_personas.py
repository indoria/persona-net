from models import Base, Journalist
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///pr_platform.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Seed: three PR journalist personas
personas = [
    Journalist(
        name="Alice Smith",
        interests="tech, startups, AI",
        style="inquisitive, neutral",
        sample_articles="The Rise of AI Startups; How Technology is Shaping the Future"
    ),
    Journalist(
        name="Bob Johnson",
        interests="consumer electronics, gadgets, innovation",
        style="formal, analytical",
        sample_articles="The Next Big Thing in Consumer Electronics; In-Depth: Gadget Trends 2025"
    ),
    Journalist(
        name="Carol Lee",
        interests="marketing, branding, social media",
        style="conversational, engaging",
        sample_articles="Branding in the Digital Age; Social Media's Impact on PR"
    ),
]

session.query(Journalist).delete()  # Clear old data for clean seed
session.add_all(personas)
session.commit()
print("Database seeded with journalist personas.")