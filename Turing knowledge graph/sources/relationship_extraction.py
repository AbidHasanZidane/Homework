# relationship_extraction.py

def extract_relationships(text, entities, nlp):
    doc = nlp(text)
    relationships = []

    # ---------------------------
    # Entity mapping
    # ---------------------------
    entity_map = {}
    for ent in entities:
        entity_map[ent["original_text"].lower()] = ent["resolved_to"]

        no_spaces = ent["original_text"].lower().replace(" ", "")
        if len(no_spaces) > 3:
            entity_map[no_spaces] = ent["resolved_to"]

    # ---------------------------
    # Canonical + resolve
    # ---------------------------
    def canonical_turing(name):
        name_lower = name.lower()
        if name_lower in ["turing", "a. turing"] or "alan turing" in name_lower:
            return "Alan Turing"
        return None

    def resolve_entity(text):
        t = text.strip().lower()

        if t in entity_map:
            return entity_map[t]

        ct = canonical_turing(t)
        if ct:
            return ct

        return text.strip()

    # ---------------------------
    # Clean object builder
    # ---------------------------
    def get_clean_object(token):
        parts = []

        for t in token.subtree:
            if t.dep_ in ("relcl", "acl", "advcl"):
                break
            if t.dep_ in ("det", "punct"):
                continue

            parts.append(t.text)

        phrase = " ".join(parts).strip()

        if len(phrase) < 3 or len(phrase.split()) > 6:
            return None

        return phrase

    def is_valid_object(token, phrase):
        BAD = {"which", "who", "that", "one", "it", "this"}

        if phrase.lower() in BAD:
            return False

        if token.ent_type_:
            return True

        if token.pos_ in ("NOUN", "PROPN") and len(phrase) > 3:
            return True

        return False

    # ---------------------------
    # Main extraction
    # ---------------------------
    last_person = None

    for sent in doc.sents:

        for ent in entities:
            if ent["original_text"] in sent.text and ent["label"] == "PERSON":
                last_person = resolve_entity(ent["original_text"])

        for token in sent:

            if token.pos_ != "VERB":
                continue

            subjects = []

            # SUBJECT
            for child in token.children:
                if child.dep_ in ("nsubj", "nsubjpass"):
                    subj = child.text

                    if subj.lower() in ["he", "him", "his", "she", "they"] and last_person:
                        subj = last_person

                    subjects.append(resolve_entity(subj))

            if not subjects and last_person:
                subjects.append(last_person)

            # DIRECT OBJECT
            for child in token.children:
                if child.dep_ in ("dobj", "attr"):
                    obj = get_clean_object(child)

                    if obj and is_valid_object(child, obj):
                        obj = resolve_entity(obj)

                        for s in subjects:
                            if s != obj:
                                relationships.append({
                                    "subject": s,
                                    "predicate": token.lemma_,
                                    "object": obj
                                })

            # PREPOSITIONAL OBJECT
            for child in token.children:
                if child.dep_ == "prep":
                    for pobj in child.children:
                        if pobj.dep_ == "pobj":

                            obj = get_clean_object(pobj)

                            if obj and is_valid_object(pobj, obj):
                                obj = resolve_entity(obj)

                                for s in subjects:
                                    relationships.append({
                                        "subject": s,
                                        "predicate": f"{token.lemma_}_{child.text}",
                                        "object": obj
                                    })

    # ---------------------------
    # FILTER + NORMALIZE
    # ---------------------------
    filtered = []

    for rel in relationships:
        s = rel["subject"]
        o = rel["object"]

        if is_turing_entity(s) or is_turing_entity(o):

            rel["subject"] = canonicalize_turing(s)
            rel["object"] = canonicalize_turing(o)

            filtered.append(rel)

    # ---------------------------
    # DEDUP
    # ---------------------------
    seen = set()
    unique = []

    for rel in filtered:
        key = (
            rel["subject"].lower(),
            rel["predicate"].lower(),
            rel["object"].lower()
        )

        if key not in seen:
            seen.add(key)
            unique.append(rel)

    return unique



def is_turing_entity(name):
    name_lower = name.lower()
    return (
        "alan turing" in name_lower or
        "turing machine" in name_lower or
        "turing test" in name_lower or
        "turing award" in name_lower or
        name_lower in ["turing", "machine", "test", "award"]
    )


def canonicalize_turing(name):
    name_lower = name.lower()

    if "alan turing" in name_lower or name_lower == "turing":
        return "Alan Turing"
    if "turing machine" in name_lower or name_lower == "machine":
        return "Turing Machine"
    if "turing test" in name_lower or name_lower == "test":
        return "Turing Test"
    if "turing award" in name_lower or name_lower == "award":
        return "Turing Award"

    return name
