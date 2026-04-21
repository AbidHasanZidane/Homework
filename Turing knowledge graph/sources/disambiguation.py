# disambiguation.py
# Only disambiguates ambiguous "Turing" - leaves "Alan Turing" and others unchanged

def disambiguate_entities(entities, text, nlp):
    """
    Disambiguate only ambiguous 'Turing' references.
    'Alan Turing' and other entities pass through unchanged.
    """
    doc = nlp(text)
    disambiguated = []
    
    for ent in entities:
        ent_text = ent["text"]
        ent_lower = ent_text.lower()
        
        # Get context for this entity
        context = ""
        for sent in doc.sents:
            if ent_text in sent.text:
                context = sent.text
                break
        
        context_lower = context.lower()
        
        # ONLY disambiguate if it's exactly "Turing" (not "Alan Turing")
        if ent_lower == "turing" and "alan" not in ent_lower:
            # Check context to determine what "Turing" refers to
            if any(keyword in context_lower for keyword in ["machine", "computational", "automaton"]):
                resolved = "Turing Machine"
                ent_type = "Concept"
                description = "Abstract computational model"
            elif any(keyword in context_lower for keyword in ["award", "prize", "acm"]):
                resolved = "Turing Award"
                ent_type = "Award"
                description = "ACM A.M. Turing Award"
            elif any(keyword in context_lower for keyword in ["test", "intelligence", "ai", "artificial intelligence"]):
                resolved = "Turing Test"
                ent_type = "Concept"
                description = "Test of machine intelligence"
            else:
                # Default to Alan Turing (the person)
                resolved = "Alan Turing"
                ent_type = "Person"
                description = "British computer scientist and mathematician"
            
            disambiguated.append({
                "original_text": ent_text,
                "label": ent["label"],
                "resolved_to": resolved,
                "type": ent_type,
                "description": description,
                "disambiguation_method": "context_inference",
                "disambiguated": True
            })
        else:
            # Fix entity types for known concepts
            ent_type = ent["label"]
            description = None
            
            # Override type for known concepts
            if ent_text == "Computability Theory":
                ent_type = "Concept"
                description = "Branch of theoretical computer science"
            elif ent_text == "Turing Machine":
                ent_type = "Concept"
                description = "Abstract computational model"
            elif ent_text == "Turing Test":
                ent_type = "Concept"
                description = "Test of machine intelligence"
            
            # All other entities: no disambiguation needed
            disambiguated.append({
                "original_text": ent_text,
                "label": ent["label"],
                "resolved_to": ent_text,
                "type": ent_type,
                "description": description,
                "disambiguation_method": "none",
                "disambiguated": False
            })
    
    return disambiguated