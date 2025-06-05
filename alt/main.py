import json
from persona_model import Persona
from weight_calculator import calculate_attribute_weights

# --- Step 1: Define your Barkha Dutt Persona JSON (assuming it's in 'barkha_dutt_persona.json')
# You'd copy the detailed JSON from the previous response into this file.

# --- Step 2: Use the Weight Calculator (Simulated Learning Phase) ---
# Create a dummy persona.json first with your initial weights.
# Then, create observations_data.json with simulated observations as shown above.
# The `calculate_attribute_weights` function will update a copy of your persona.json
# with new weights based on these observations.

initial_persona_path = 'barkha_dutt_persona.json' # Your initial persona definition
observations_data_path = 'observations_data.json' # Simulated observations
updated_persona_path = 'barkha_dutt_persona_weighted.json' # Output for updated persona

print("--- Running Weight Calculation Simulation ---")
# Before running this, ensure `barkha_dutt_persona.json` exists with initial weights
# and `observations_data.json` exists with your simulated observations.
calculate_attribute_weights(observations_data_path, updated_persona_path, initial_persona_path)
print("-------------------------------------------\n")


# --- Step 3: Load and Use the Persona ---
# Now load the persona with the (potentially) updated weights
bd_persona = Persona(updated_persona_path)

if bd_persona.data:
    print("\n--- Simulating Persona Interactions ---")

    # Example 1: Assess a pitch
    pitch_example_good = {
        "title": "Investigative Report: Hidden Costs of [Policy Name]",
        "summary": "Our detailed investigation uncovers significant financial irregularities and human displacement linked to the recent [Policy Name] implementation. We have corroborating documents and direct testimonies from affected families.",
        "keywords": ["investigation", "accountability", "human impact", "policy", "unique_angle", "breaking"],
        "data_provided": True,
        "potential_impact": 0.9,
        "source_reputation": 0.95,
        "ethical_alignment": True
    }
    print("\n--- Pitch Assessment (Good Pitch) ---")
    assessment_good = bd_persona.assess_pitch(pitch_example_good)
    print(assessment_good['feedback_message'])

    pitch_example_bad = {
        "title": "New Product Launch: Revolutionary AI-Powered [Product Name]",
        "summary": "Our company, [XYZ Tech], is launching an AI product. It's awesome and will change everything. We need coverage.",
        "keywords": ["product launch", "tech", "hype"],
        "data_provided": False,
        "potential_impact": 0.3,
        "source_reputation": 0.6,
        "ethical_alignment": False # Lacks transparency
    }
    print("\n--- Pitch Assessment (Bad Pitch) ---")
    assessment_bad = bd_persona.assess_pitch(pitch_example_bad)
    print(assessment_bad['feedback_message'])

    # Example 2: Generate a response to a prompt
    print("\n--- Generate Response (General) ---")
    response_general = bd_persona.generate_response("Tell me about the state of media freedom in India.", "general discussion")
    print(response_general['response_text'])

    print("\n--- Generate Response (Crisis Context) ---")
    response_crisis = bd_persona.generate_response("What are your thoughts on the recent migrant crisis?", "crisis, human rights, accountability")
    print(response_crisis['response_text'])

    # Example 3: Ask a question
    print("\n--- Ask a Question (Press Conference) ---")
    question_pc = bd_persona.ask_question("government's response to rising unemployment", "press conference")
    print(question_pc['question'])
    
    print("\n--- Ask a Question (General Topic) ---")
    question_general = bd_persona.ask_question("challenges facing independent journalism today")
    print(question_general['question'])