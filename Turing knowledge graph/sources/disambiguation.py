def disambiguate_entities(entities, text, nlp):
    doc = nlp(text)
    disambiguated = []

    WINDOW_SIZE = 6  # slightly larger context

    # -------------------------
    # Scenario-based vocab
    # -------------------------
    PERSON_VERBS = {"bear", "born", "work", "study", "die", "publish", "prosecute"}
    PERSON_NOUNS = {"university", "war", "code", "laboratory"}

    MACHINE_VERBS = {"compute", "simulate", "process", "decide"}
    MACHINE_NOUNS = {"machine", "algorithm", "input", "output", "computable"}

    TEST_VERBS = {"test", "measure", "evaluate", "distinguish", "demonstrate"}
    TEST_NOUNS = {"intelligence", "behavior", "human", "judge"}

    AWARD_VERBS = {"award", "win", "receive"}
    AWARD_NOUNS = {"prize", "acm", "award"}

    for ent in entities:
        ent_text = ent["text"]
        ent_lower = ent_text.lower()

        # only disambiguate standalone "Turing"
        if ent_lower != "turing":
            disambiguated.append({
                "original_text": ent_text,
                "label": ent["label"],
                "resolved_to": ent_text,
                "type": ent["label"],
                "description": None,
                "disambiguation_method": "none",
                "disambiguated": False
            })
            continue

        # -------------------------
        # Shortcut for explicit phrases
        # -------------------------
        text_lower = text.lower()
        if "turing machine" in text_lower:
            best_label = "Turing Machine"
        elif "turing test" in text_lower:
            best_label = "Turing Test"
        elif "turing award" in text_lower:
            best_label = "Turing Award"
        else:
            matched_tokens = [t for t in doc if t.text == ent_text]

            best_label = None
            best_score = -1

            for token in matched_tokens:

                start = max(0, token.i - WINDOW_SIZE)
                end = min(len(doc), token.i + WINDOW_SIZE + 1)

                window = doc[start:end]
                words = {t.lemma_.lower() for t in window}

                # -------------------------
                # SCORING (weighted)
                # -------------------------
                scores = {
                    "Alan Turing": 0,
                    "Turing Machine": 0,
                    "Turing Test": 0,
                    "Turing Award": 0
                }

                # PERSON
                scores["Alan Turing"] += len(words & PERSON_VERBS) * 2
                scores["Alan Turing"] += len(words & PERSON_NOUNS)

                # MACHINE
                scores["Turing Machine"] += len(words & MACHINE_VERBS) * 2
                scores["Turing Machine"] += len(words & MACHINE_NOUNS)

                # TEST
                scores["Turing Test"] += len(words & TEST_VERBS) * 2
                scores["Turing Test"] += len(words & TEST_NOUNS)

                # AWARD
                scores["Turing Award"] += len(words & AWARD_VERBS) * 2
                scores["Turing Award"] += len(words & AWARD_NOUNS)

                label = max(scores, key=scores.get)
                score = scores[label]

                if score > best_score:
                    best_score = score
                    best_label = label

            # fallback
            if best_score == 0:
                best_label = "Alan Turing"

        # -------------------------
        # Type mapping
        # -------------------------
        if best_label == "Alan Turing":
            ent_type = "Person"
            desc = "British computer scientist"
        elif best_label == "Turing Machine":
            ent_type = "Concept"
            desc = "Abstract computational model"
        elif best_label == "Turing Test":
            ent_type = "Concept"
            desc = "Test of machine intelligence"
        else:
            ent_type = "Award"
            desc = "ACM A.M. Turing Award"

        disambiguated.append({
            "original_text": ent_text,
            "label": ent["label"],
            "resolved_to": best_label,
            "type": ent_type,
            "description": desc,
            "disambiguation_method": "context_classification",
            "disambiguated": True
        })

    return disambiguated
