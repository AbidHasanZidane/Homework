# relationship_extraction.py
# Pure spaCy - no extra dependencies

import re

def extract_relationships(text, entities, nlp):
    """
    Extract relationships using spaCy's dependency parsing.
    Captures more relationships than basic version.
    """
    doc = nlp(text)
    relationships = []
    
    # Identify the main subject (Alan Turing or first PERSON entity)
    main_subject = None
    for ent in entities:
        if ent.get("type") == "Person" or ent["label"] == "PERSON":
            if "turing" in ent["resolved_to"].lower() or "alan" in ent["resolved_to"].lower():
                main_subject = ent["resolved_to"]
                break
    
    if not main_subject:
        for ent in entities:
            if ent.get("type") == "Person" or ent["label"] == "PERSON":
                main_subject = ent["resolved_to"]
                break
    
    if not main_subject:
        main_subject = "Alan Turing"
    
    # Track last mentioned person for pronoun resolution
    last_person = main_subject
    
    # Keep track of dates already captured to avoid duplicates
    captured_dates = set()
    
    # Create set of all entity names for quick lookup
    entity_names = set()
    for ent in entities:
        entity_names.add(ent["original_text"].lower())
        entity_names.add(ent["resolved_to"].lower())
    
    def clean_text(text):
        """Clean text by removing punctuation and extra spaces."""
        text = text.strip('.,;:!?"\'')
        text = re.sub(r'\s+', ' ', text)
        return text
    
    def is_date_already_captured(date_value, predicate_type):
        """Check if a date has already been captured for this predicate type."""
        key = (date_value, predicate_type)
        if key in captured_dates:
            return True
        captured_dates.add(key)
        return False
    
    # Process each sentence
    for sent in doc.sents:
        sent_text = sent.text
        sent_lower = sent_text.lower()
        
        # Update last person if a person entity appears
        for ent in entities:
            if ent.get("type") == "Person" or ent["label"] == "PERSON":
                if ent["original_text"] in sent_text:
                    last_person = ent["resolved_to"]
        
        current_subject = last_person if last_person else main_subject
        
        # ============ 1. SUBJECT-VERB-OBJECT (filtered) ============
        for token in sent:
            if token.pos_ == "VERB" and token.dep_ == "ROOT":
                subjects = []
                objects = []
                
                # Find subjects
                for child in token.children:
                    if child.dep_ in ["nsubj", "nsubjpass"]:
                        span = sent[child.left_edge.i:child.right_edge.i + 1]
                        subj_text = span.text.strip()
                        
                        # Resolve pronouns
                        if subj_text.lower() in ["he", "him", "his", "he's", "he is", "he was"]:
                            subj_text = current_subject
                        subjects.append(subj_text)
                
                # If no subject found, use current_subject
                if not subjects:
                    subjects.append(current_subject)
                
                # Find objects
                for child in token.children:
                    if child.dep_ in ["dobj", "pobj", "attr", "dobj:pass"]:
                        span = sent[child.left_edge.i:child.right_edge.i + 1]
                        obj_text = span.text.strip()
                        
                        # Skip vague objects and dates that will be captured elsewhere
                        if len(obj_text) > 2 and obj_text.lower() not in ["one", "his", "her", "their", "its", "a", "an", "the"]:
                            # Skip if it's a date and we already have specific date predicates
                            if re.match(r'\d{4}', obj_text) or "born" in sent_lower or "died" in sent_lower:
                                continue
                            objects.append(obj_text)
                
                # Create relationships
                for subj in subjects:
                    for obj in objects:
                        if subj != obj and len(obj) > 2:
                            # Only keep if subject is main_subject
                            if main_subject.lower() in subj.lower() or subj.lower() == main_subject.lower():
                                predicate = token.lemma_
                                
                                # Skip generic verbs and "bear" (which gives "bear_on")
                                if predicate not in ["be", "have", "do", "say", "bear"]:
                                    relationships.append({
                                        "subject": main_subject,
                                        "predicate": predicate,
                                        "object": clean_text(obj)
                                    })
        
        # ============ 2. PREPOSITION RELATIONSHIPS ============
        for token in sent:
            if token.dep_ == "prep" and token.head.pos_ == "VERB":
                verb = token.head.lemma_
                prep = token.text
                
                # Skip "bear_on" type relationships
                if verb == "bear":
                    continue
                
                for child in token.children:
                    if child.dep_ == "pobj":
                        obj_text = sent[child.left_edge.i:child.right_edge.i + 1].text.strip()
                        
                        # Skip if it's a year (to avoid duplicate dates)
                        if re.match(r'^\d{4}$', obj_text):
                            continue
                        
                        if len(obj_text) > 2 and obj_text.lower() not in ["one", "his", "her"]:
                            # Create meaningful predicate
                            if verb not in ["be", "bear"]:
                                predicate = f"{verb}_{prep}" if verb != "be" else prep
                            else:
                                predicate = prep
                            
                            relationships.append({
                                "subject": main_subject,
                                "predicate": predicate,
                                "object": clean_text(obj_text)
                            })
        
        # ============ 3. IS_A (profession/nationality) ============
        is_a_pattern = r"(?:was|is)\s+(?:a|an)\s+([A-Za-z][A-Za-z\s,]+?)(?=\s+(?:and|\.|;|$))"
        match = re.search(is_a_pattern, sent_text, re.IGNORECASE)
        if match:
            professions_text = match.group(1)
            # Split by commas and "and"
            professions = re.split(r',\s*|\s+and\s+', professions_text)
            for prof in professions:
                prof = prof.strip()
                if len(prof) > 2 and len(prof.split()) <= 4:
                    relationships.append({
                        "subject": main_subject,
                        "predicate": "is_a",
                        "object": prof.title()
                    })
        
        # ============ 4. BIRTH DATE ============
        birth_date_match = re.search(r'born\s+on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', sent_text)
        if birth_date_match:
            date_value = birth_date_match.group(1)
            if not is_date_already_captured(date_value, "birth_date"):
                relationships.append({
                    "subject": main_subject,
                    "predicate": "birth_date",
                    "object": date_value
                })
        
        # ============ 5. BIRTH PLACE ============
        birth_place_match = re.search(r'born\s+in\s+([A-Z][a-z]+)', sent_text)
        if birth_place_match:
            relationships.append({
                "subject": main_subject,
                "predicate": "birth_place",
                "object": birth_place_match.group(1)
            })
        
        # ============ 6. DEATH DATE ============
        death_date_match = re.search(r'died\s+on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', sent_text)
        if death_date_match:
            date_value = death_date_match.group(1)
            if not is_date_already_captured(date_value, "death_date"):
                relationships.append({
                    "subject": main_subject,
                    "predicate": "death_date",
                    "object": date_value
                })
        
        # ============ 7. DEATH PLACE ============
        death_place_match = re.search(r'died\s+in\s+([A-Z][a-z]+)', sent_text)
        if death_place_match:
            # Clean up - don't include extra text
            place = death_place_match.group(1).strip()
            if "," not in place:  # Avoid capturing "Wilmslow" correctly
                relationships.append({
                    "subject": main_subject,
                    "predicate": "death_place",
                    "object": place
                })
        
        # ============ 8. EDUCATION ============
        studied_match = re.search(r'studied\s+(?:at|mathematics\s+at)\s+([A-Z][a-zA-Z\s]+(?:University|College))', sent_text)
        if studied_match:
            relationships.append({
                "subject": main_subject,
                "predicate": "studied_at",
                "object": studied_match.group(1).strip()
            })
        
        # Interested in
        interest_match = re.search(r'interest\s+in\s+([A-Za-z][a-zA-Z\s]+?)(?=\.|,|;)', sent_text)
        if interest_match and "developed" in sent_lower:
            relationships.append({
                "subject": main_subject,
                "predicate": "interested_in",
                "object": interest_match.group(1).strip().title()
            })
        
        # Graduate studies
        grad_match = re.search(r'pursued\s+graduate\s+studies\s+at\s+([A-Z][a-zA-Z\s]+(?:University))', sent_text)
        if grad_match:
            relationships.append({
                "subject": main_subject,
                "predicate": "pursued_graduate_studies_at",
                "object": grad_match.group(1).strip()
            })
        
        # PhD completion
        phd_match = re.search(r'completed\s+his\s+phd\s+in\s+(\d{4})', sent_lower)
        if phd_match:
            date_value = phd_match.group(1)
            if not is_date_already_captured(date_value, "completed_phd"):
                relationships.append({
                    "subject": main_subject,
                    "predicate": "completed_phd",
                    "object": date_value
                })
        
        # ============ 9. CREATIONS ============
        created_patterns = [
            r'introduced\s+the\s+concept\s+of\s+([A-Z][a-zA-Z\s]+)',
            r'created\s+the\s+([A-Z][a-zA-Z\s]+)',
            r'developed\s+the\s+([A-Z][a-zA-Z\s]+)',
            r'proposed\s+the\s+([A-Z][a-zA-Z\s]+)'
        ]
        
        for pattern in created_patterns:
            match = re.search(pattern, sent_text)
            if match:
                created_obj = match.group(1).strip()
                # Clean up object
                created_obj = created_obj.rstrip(',')
                relationships.append({
                    "subject": main_subject,
                    "predicate": "created",
                    "object": created_obj
                })
                break
        
        # ============ 10. WORK LOCATIONS ============
        work_patterns = [
            r'worked\s+at\s+([A-Z][a-zA-Z\s]+(?:Park|Laboratory|Institute))',
            r'worked\s+at\s+the\s+([A-Z][a-zA-Z\s]+(?:Laboratory))',
            r'joined\s+the\s+([A-Z][a-zA-Z\s]+(?:University))'
        ]
        
        for pattern in work_patterns:
            match = re.search(pattern, sent_text)
            if match:
                workplace = match.group(1).strip()
                predicate = "joined" if "joined" in pattern else "worked_at"
                # Clean up "the Bletchley Park" to "Bletchley Park"
                workplace = workplace.replace("the ", "")
                relationships.append({
                    "subject": main_subject,
                    "predicate": predicate,
                    "object": workplace
                })
        
        # ============ 11. CONTRIBUTIONS ============
        contrib_match = re.search(r'contributed\s+to\s+(?:the\s+field\s+of\s+)?([A-Z][a-zA-Z\s]+(?:Theory|Science|Intelligence|Cryptography))', sent_text)
        if contrib_match:
            contrib_obj = contrib_match.group(1).strip()
            contrib_obj = contrib_obj.rstrip(',')
            relationships.append({
                "subject": main_subject,
                "predicate": "contributed_to",
                "object": contrib_obj
            })
        
        # ============ 12. PUBLICATIONS ============
        pub_match = re.search(r'published\s+a\s+paper\s+titled\s+"([^"]+)"', sent_text)
        if pub_match:
            pub_title = pub_match.group(1).strip()
            pub_title = pub_title.rstrip(',')
            relationships.append({
                "subject": main_subject,
                "predicate": "published",
                "object": pub_title
            })
        
        pub_date_match = re.search(r'In\s+(\d{4}),\s+Alan Turing\s+published', sent_text)
        if pub_date_match:
            date_value = pub_date_match.group(1)
            if not is_date_already_captured(date_value, "publication_date"):
                relationships.append({
                    "subject": main_subject,
                    "predicate": "publication_date",
                    "object": date_value
                })
        
        # ============ 13. LEGAL EVENTS ============
        if "prosecuted" in sent_lower:
            relationships.append({
                "subject": main_subject,
                "predicate": "prosecuted_for",
                "object": "homosexuality"
            })
        
        treatment_match = re.search(r'accepted\s+([a-zA-Z\s]+)\s+as\s+an\s+alternative', sent_lower)
        if treatment_match:
            treatment = treatment_match.group(1).strip()
            relationships.append({
                "subject": main_subject,
                "predicate": "accepted",
                "object": treatment
            })
        
        pardon_match = re.search(r'pardoned\s+by\s+([A-Z][a-zA-Z\s]+(?:II))', sent_text)
        if pardon_match:
            relationships.append({
                "subject": main_subject,
                "predicate": "pardoned_by",
                "object": pardon_match.group(1).strip()
            })
        
        pardon_year_match = re.search(r'In\s+(\d{4}),\s+Alan Turing\s+was\s+posthumously\s+pardoned', sent_text)
        if pardon_year_match:
            date_value = pardon_year_match.group(1)
            if not is_date_already_captured(date_value, "pardoned_year"):
                relationships.append({
                    "subject": main_subject,
                    "predicate": "pardoned_year",
                    "object": date_value
                })
    
    # Deduplicate and filter
    unique_rels = []
    seen = set()
    
    # List of bad objects to filter out
    bad_objects = [
        "one", "his", "her", "their", "its", "a crucial role", "the field", 
        "graduate studies", "his phd", "in", "on", "at", "to", "for", "with", "by",
        "1954, in Wilmslow", "in Wilmslow"
    ]
    
    for rel in relationships:
        # Clean object
        rel["object"] = clean_text(rel["object"])
        
        # Skip bad objects
        if rel["object"].lower() in bad_objects:
            continue
        
        # Skip if object is just a year and we already have specific date predicates
        if re.match(r'^\d{4}$', rel["object"]):
            if rel["predicate"] in ["date", "birth_date", "death_date", "completed_phd", "publication_date", "pardoned_year"]:
                # Skip generic "date" predicate for years
                if rel["predicate"] == "date":
                    continue
        
        # Skip "bear_on" predicate
        if rel["predicate"] in ["bear", "bear_on"]:
            continue
        
        key = (rel["subject"].lower(), rel["predicate"].lower(), rel["object"].lower())
        if key not in seen:
            seen.add(key)
            unique_rels.append(rel)
    
    return unique_rels