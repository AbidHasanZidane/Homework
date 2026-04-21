import spacy
import en_core_web_sm
import json
from collections import defaultdict
from disambiguation import disambiguate_entities
from relationship_extraction import extract_relationships
from kg_visualization import save_json, save_triplets_txt, visualize_ascii, visualize_html, visualize_dot, print_summary

# Load the model
nlp = en_core_web_sm.load()

print("Enter text: ")
text = input()

def extract_entities(text):
    """Extract named entities using spaCy."""
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_,
            "start": ent.start_char,
            "end": ent.end_char
        })
    return entities

def build_knowledge_graph(text):
    entities = extract_entities(text)
    disambiguated_entities = disambiguate_entities(entities, text, nlp)
    triplets = extract_relationships(text, disambiguated_entities, nlp)
    
    # Deduplicate entities by resolved_to name
    unique_entities = {}
    for ent in disambiguated_entities:
        key = ent["resolved_to"]
        if key not in unique_entities:
            unique_entities[key] = ent
    
    kg = {
        "source_text": text.strip(),
        "entities": list(unique_entities.values()),
        "triplets": triplets,
        "statistics": {
            "total_entities": len(unique_entities),
            "total_triplets": len(triplets),
            "entity_types": defaultdict(int)
        }
    }
    
    # Count entity types
    for ent in unique_entities.values():
        ent_type = ent.get("type", ent["label"])
        kg["statistics"]["entity_types"][ent_type] += 1
    
    kg["statistics"]["entity_types"] = dict(kg["statistics"]["entity_types"])
    
    return kg

if __name__ == "__main__":
    # Build knowledge graph
    kg = build_knowledge_graph(text)
    
    # Save outputs
    save_json(kg)
    
    # Visualizations
    visualize_html(kg)
    visualize_dot(kg)
    
    print("DONE.")