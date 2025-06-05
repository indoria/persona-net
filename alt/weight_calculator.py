import json
from collections import defaultdict

def calculate_attribute_weights(observation_data_path, output_json_path, persona_template_path):
    """
    Simulates calculating/refining attribute weights based on a set of observations.
    
    Args:
        observation_data_path (str): Path to a JSON file containing simulated observations.
                                     Each observation should manually score attributes.
                                     Example structure:
                                     [
                                         {
                                             "content": "Transcript of an interview where Barkha was very empathetic.",
                                             "attribute_scores": {
                                                 "core_attributes.core_principles_and_values.Fearless Pursuit of Truth.weight": 4,
                                                 "core_attributes.core_principles_and_values.Amplifying Marginalized Voices.weight": 5,
                                                 "communication_linguistic_style.overall_tone.primary_tone.Empathetic": 5,
                                                 "personality_behavioral_modeling.dominant_personality_traits.Openness to Experience.weight": 3
                                             },
                                             "max_score_per_attribute": 5 # Max score for this observation for each attribute
                                         },
                                         {
                                             "content": "Article analyzing government policy, very direct and analytical.",
                                             "attribute_scores": {
                                                 "core_attributes.core_principles_and_values.Holding Power Accountable.weight": 5,
                                                 "communication_linguistic_style.overall_tone.primary_tone.Direct": 5,
                                                 "communication_linguistic_style.overall_tone.primary_tone.Analytical": 5
                                             },
                                             "max_score_per_attribute": 5
                                         }
                                     ]
        output_json_path (str): Path where the updated persona JSON with new weights will be saved.
        persona_template_path (str): Path to the original persona JSON template to update.
    """
    try:
        with open(observation_data_path, 'r', encoding='utf-8') as f:
            observations = json.load(f)
        with open(persona_template_path, 'r', encoding='utf-8') as f:
            persona_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Required file not found. Check paths.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in input files.")
        return

    attribute_sums = defaultdict(float)
    attribute_counts = defaultdict(int)

    for obs in observations:
        scores = obs.get("attribute_scores", {})
        max_score = obs.get("max_score_per_attribute", 5) # Default max score for the observation

        for attr_path, score in scores.items():
            # Convert raw score to a normalized value (0 to 1) for averaging
            normalized_score = score / max_score
            attribute_sums[attr_path] += normalized_score
            attribute_counts[attr_path] += 1
    
    # Calculate average normalized score for each attribute
    average_weights = {
        path: attribute_sums[path] / attribute_counts[path]
        for path in attribute_sums
    }

    print("\nCalculated Average Weights:")
    for path, avg_weight in average_weights.items():
        print(f"  {path}: {avg_weight:.3f}")

    # Apply calculated weights back to the persona_data structure
    updated_attributes_count = 0
    for path, new_weight in average_weights.items():
        keys = path.split('.')
        current_level = persona_data
        
        try:
            for i, key in enumerate(keys):
                if i == len(keys) - 1: # Last key is the attribute name
                    if key.endswith(".weight"): # Directly update 'weight'
                        parent_key = keys[-2]
                        # Find the dictionary within the list that matches the parent key
                        # This handles lists of dictionaries, like core_principles_and_values
                        found = False
                        if isinstance(current_level, list):
                            for item in current_level:
                                if isinstance(item, dict) and item.get("name") == parent_key:
                                    item["weight"] = new_weight
                                    found = True
                                    updated_attributes_count += 1
                                    break
                            if not found: # If not found by 'name', try by raw key (e.g., if it's not a list of named dicts)
                                if parent_key in current_level: # Direct dict key
                                    current_level[parent_key] = new_weight
                                    updated_attributes_count += 1
                        elif isinstance(current_level, dict): # Direct dict key update
                            current_level[key] = new_weight
                            updated_attributes_count += 1
                        break
                    else: # If not updating 'weight', find the item in a list or dict
                        if isinstance(current_level, list):
                            # This path logic is more complex for nested lists of dicts
                            # For simplicity, this example assumes direct 'weight' property or direct key update
                            # Realistically, you'd need more sophisticated pathing logic for complex structures.
                            pass # Handle other cases if needed
                        else: # Direct dict key (e.g., if path is 'interaction_protocols.interaction_impact_weight')
                            current_level[key] = new_weight
                            updated_attributes_count += 1
                else:
                    if isinstance(current_level, list):
                        # This part requires a specific strategy for lists of dicts.
                        # For Barkha Dutt's JSON, a path like "core_attributes.core_principles_and_values.Fearless Pursuit of Truth.weight"
                        # means: access core_attributes, then core_principles_and_values (which is a list).
                        # Then find the dict in that list where "name" is "Fearless Pursuit of Truth".
                        found_next_level = False
                        for item in current_level:
                            if isinstance(item, dict) and item.get("name") == key:
                                current_level = item
                                found_next_level = True
                                break
                        if not found_next_level:
                            raise KeyError(f"Could not find item with name '{key}' in list.")
                    else:
                        current_level = current_level[key]

        except (KeyError, TypeError) as e:
            print(f"Warning: Could not update attribute path '{path}': {e}. Skipping.")
            continue
    
    print(f"\nSuccessfully updated {updated_attributes_count} attribute weights in the persona data.")

    # Save the updated persona data
    with open(output_json_path, 'w', encoding='utf-8') as f:
        json.dump(persona_data, f, indent=2, ensure_ascii=False)
    print(f"Updated persona saved to {output_json_path}")