import json
import random
from textwrap import dedent

class Persona:
    def __init__(self, persona_json_path):
        """Initializes the persona from a JSON file."""
        try:
            with open(persona_json_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            self.persona_name = self.data['persona_identification']['persona_name']
            self.real_person_name = self.data['persona_identification']['real_person_reference']['real_person_full_name']
            print(f"Persona '{self.persona_name}' based on '{self.real_person_name}' loaded successfully.")
        except FileNotFoundError:
            print(f"Error: Persona JSON file not found at {persona_json_path}")
            self.data = {}
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {persona_json_path}")
            self.data = {}

    def _get_attribute(self, path, default=None):
        """Helper to safely get nested attributes from the persona data."""
        keys = path.split('.')
        current = self.data
        try:
            for key in keys:
                current = current[key]
            return current
        except (KeyError, TypeError):
            return default

    def _apply_dynamic_weights(self, attribute_value, context=None):
        """
        Applies dynamic weighting based on context.
        This is a placeholder for complex logic.
        For example, if context includes 'crisis', empathy weight might increase.
        """
        # Example dynamic weighting logic (highly simplified)
        adjusted_weight = attribute_value.get('weight', 1.0) # Default weight is 1.0 if not specified
        if context:
            if 'crisis' in context.lower() and 'empathy' in attribute_value.get('description', '').lower():
                adjusted_weight *= 1.5 # Increase empathy in crisis
            if 'accountability' in context.lower() and 'directness' in attribute_value.get('description', '').lower():
                adjusted_weight *= 1.2 # Increase directness for accountability
        return adjusted_weight

    def assess_pitch(self, pitch_details):
        """
        Simulates Barkha Dutt assessing a media pitch based on defined criteria and weights.
        
        Args:
            pitch_details (dict): A dictionary containing details of the pitch,
                                  e.g., {'title': '...', 'summary': '...', 'data_provided': True, ...}
                                  The keys in pitch_details should ideally map to sub_criteria or
                                  be interpretable by a scoring function for each criterion.
        
        Returns:
            dict: An assessment including a score, strengths, and weaknesses.
        """
        if not self.data:
            return {"error": "Persona not loaded."}

        criteria = self._get_attribute('interaction_protocols.pitch_assessment_criteria.criteria_breakdown', {})
        total_weighted_score = 0
        max_possible_score = 0
        strengths = []
        weaknesses = []

        # Simplified scoring logic for demonstration.
        # In a real system, you'd use NLP to evaluate pitch_details against criterion.
        def score_criterion(criterion_name, criterion_def, pitch_details):
            score = 0
            # Placeholder: Replace with actual logic based on pitch_details content
            if "relevance" in criterion_name.lower() and "relevance" in pitch_details.get("keywords", []):
                score += 5
            if "newsworthiness" in criterion_name.lower() and "breaking" in pitch_details.get("keywords", []):
                score += 5
            if "clarity" in criterion_name.lower() and len(pitch_details.get("summary", "")) < 200:
                score += 5 # Assume concise is good
            if "completeness" in criterion_name.lower() and pitch_details.get("data_provided", False):
                score += 5
            if "originality" in criterion_name.lower() and "unique_angle" in pitch_details.get("keywords", []):
                score += 5
            if "impact" in criterion_name.lower() and pitch_details.get("potential_impact", 0) > 0.7:
                score += 5
            if "credibility" in criterion_name.lower() and pitch_details.get("source_reputation", 0) > 0.8:
                score += 5
            if "ethical" in criterion_name.lower() and pitch_details.get("ethical_alignment", True):
                score += 5
            
            return min(score, 5) # Cap score at 5 for simplicity

        for crit_name, crit_def in criteria.items():
            weight = crit_def.get('weight', 0.0)
            score = score_criterion(crit_name, crit_def, pitch_details)
            weighted_score = score * weight
            total_weighted_score += weighted_score
            max_possible_score += 5 * weight # Assuming max score for a criterion is 5

            if score >= 4: # Assuming 4-5 is a strength
                strengths.append(f"{crit_name}: {crit_def['details']} (Score: {score}/5)")
            elif score <= 2: # Assuming 0-2 is a weakness
                weaknesses.append(f"{crit_name}: {crit_def['details']} (Score: {score}/5)")

        overall_percentage = (total_weighted_score / max_possible_score) * 100 if max_possible_score > 0 else 0

        # Constructing the response based on persona's response framing principles
        response_goal = self._get_attribute('interaction_protocols.response_framing_principles.goal_of_response', 'provide feedback.')
        response_tone_options = self._get_attribute('interaction_protocols.response_framing_principles.tone_for_response', 'professional')
        
        # Pick a tone from options (simplified)
        response_tone = response_tone_options[0] if isinstance(response_tone_options, list) else response_tone_options

        feedback_message = f"Subject: Assessment of Your Pitch on '{pitch_details.get('title', 'Untitled Pitch')}'\n\n"
        feedback_message += f"Dear colleague,\n\n"
        feedback_message += dedent(f"""
            Thank you for reaching out with your pitch on '{pitch_details.get('title', 'Untitled Pitch')}'.
            I've reviewed the material.
            
            My initial assessment yields an overall score of {overall_percentage:.2f}%.
            
            From a journalistic perspective, here are the key observations:
        """)

        if strengths:
            feedback_message += "\n**Strengths:**\n" + "\n".join([f"- {s}" for s in strengths])
        else:
            feedback_message += "\n**Strengths:** No significant strengths immediately stood out, though the effort is noted."

        if weaknesses:
            feedback_message += "\n\n**Areas for Further Consideration/Improvement:**\n" + "\n".join([f"- {w}" for w in weaknesses])
        else:
            feedback_message += "\n\n**Areas for Further Consideration/Improvement:** The pitch was relatively strong, with no major weaknesses identified at this stage."

        feedback_message += dedent(f"""

            Given this assessment, to {response_goal.lower()}.

            Please consider these points for future pitches or if you wish to refine this one.
            
            Regards,
            {self.real_person_name} (AI Persona)
        """)

        return {
            "score": overall_percentage,
            "strengths": strengths,
            "weaknesses": weaknesses,
            "feedback_message": feedback_message,
            "persona_tone_used": response_tone
        }

    def generate_response(self, prompt, context="general discussion"):
        """
        Simulates Barkha Dutt's response to a given prompt,
        adapting communication style based on context and persona attributes.
        This is a highly simplified text generation for demonstration.
        Real implementation would use sophisticated NLP models.
        """
        if not self.data:
            return {"error": "Persona not loaded."}

        # Dynamically select communication style elements based on context
        tone_options = self._get_attribute('communication_linguistic_style.overall_tone.primary_tone', ['Analytical'])
        selected_tone = random.choice(tone_options) if isinstance(tone_options, list) else tone_options

        # Vocabulary usage - pick some descriptors
        vocab_descriptors = [d['usage'] for d in self._get_attribute('communication_linguistic_style.vocabulary_usage.descriptors', []) if 'usage' in d]
        
        # Common phrases
        common_phrases = [p['phrase'] for p in self._get_attribute('core_attributes.common_phrases_keywords', [])]
        
        # Core principles for content framing
        principles = [p['name'] for p in self._get_attribute('core_attributes.core_principles_and_values', [])]
        
        # Key thematic focus for content relevance
        thematic_focus = [t['theme'] for t in self._get_attribute('cognitive_information_processing.key_thematic_focus_areas', [])]

        # Construct a response based on simplified rules
        response_parts = []
        response_parts.append(f"({selected_tone.capitalize()} Tone):\n")
        response_parts.append(f"Regarding '{prompt}', it's crucial to approach this with a {selected_tone.lower()} lens. ")

        if any(p in context.lower() for p in ['crisis', 'human rights', 'justice']):
            response_parts.append(f"As an independent journalist, my {random.choice(principles).lower()} principle immediately brings the human element into focus. ")
            response_parts.append(f"What does this truly mean on the ground? We need to delve 'beyond the headlines' to understand the real impact.")
        else:
            response_parts.append(f"My focus here, as always, aligns with {random.choice(principles).lower()}. ")
            response_parts.append(f"This falls squarely within the realm of {random.choice(thematic_focus).lower()}.")

        if "question" in prompt.lower() or "ask" in prompt.lower():
             response_parts.append(f"We must 'ask the tough questions' here, demanding specifics and unearthing inconsistencies. ")
        
        if common_phrases:
            response_parts.append(f"To {random.choice(common_phrases).lower()}...")
        
        response_parts.append(f"This demands rigorous analysis, leveraging precise vocabulary. We must ensure 'accountability'.")
        
        # Add a concluding thought based on traits
        if "accountability" in context.lower() or "power" in context.lower():
            response_parts.append("Ultimately, the focus must remain on holding power accountable and amplifying voices that might otherwise be silenced.")
        else:
            response_parts.append("Ultimately, it's about robust journalism that informs the public and fosters critical discourse.")

        return {
            "response_text": dedent("".join(response_parts)).strip(),
            "selected_tone": selected_tone,
            "context_applied": context
        }

    def ask_question(self, topic, context="general"):
        """
        Simulates Barkha Dutt asking a question based on her questioning technique.
        """
        if not self.data:
            return {"error": "Persona not loaded."}
        
        question_types = self._get_attribute('communication_linguistic_style.questioning_technique.typical_question_types', [])
        priority_questions_config = self._get_attribute('interaction_protocols.reaction_to_press_conference_protocol.priority_questions', [])

        # Filter questions based on context if possible, or pick a random one
        relevant_questions = []
        if context == "press conference":
            relevant_questions = [q['focus'] for q in priority_questions_config]
        else:
            relevant_questions = [q['purpose'] for q in question_types]

        if not relevant_questions:
            return {"question": f"Given the topic of '{topic}', what more can you tell me?", "type": "General Inquiry"}

        selected_question_focus = random.choice(relevant_questions)
        
        # Craft a question using common phrases and style elements
        question_starter = random.choice(self._get_attribute('core_attributes.common_phrases_keywords', []))['phrase']
        
        question_text = f"{question_starter} Regarding '{topic}', {selected_question_focus.replace('e.g., ', '')}"

        return {
            "question": question_text,
            "type": selected_question_focus
        }