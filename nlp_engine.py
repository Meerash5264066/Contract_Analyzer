import re
from textblob import TextBlob

# 🔹 Split text into sentences properly
def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


# 🔹 Highlight keywords inside sentence
def highlight_keywords(clause, found_keywords):
    # Sort by length descending to match longest phrases first
    found_keywords = sorted(list(set(found_keywords)), key=len, reverse=True)
    
    for keyword in found_keywords:
        # Avoid processing if empty
        if not keyword.strip(): continue
        
        pattern = re.compile(r'\b' + re.escape(keyword) + r'\b', re.IGNORECASE)
        clause = pattern.sub(
            f'<span class="keyword-highlight">{keyword}</span>',
            clause
        )
    return clause


# 🔹 Main SMART NLP function
def analyze_contract(text, database_keywords):
    clauses = split_sentences(text)
    results = []

    for clause in clauses:
        clause_lower = clause.lower()
        score = 0
        found_keywords = []

        # ❌ Skip useless short lines
        if len(clause.strip()) < 20:
            continue

        # ----------------------------------------------------
        # 🔥 STEP 1: DB KEYWORDS + WEIGHTED SCORING
        # ----------------------------------------------------
        for keyword, risk_type in database_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', clause_lower):
                found_keywords.append(keyword)
                if risk_type == "High":
                    score += 3
                elif risk_type == "Medium":
                    score += 2
                else:
                    score += 1

        # ----------------------------------------------------
        # 🔥 STEP 2: CONTEXT-BASED RULES (SMART DETECTION)
        # ----------------------------------------------------
        if "terminate" in clause_lower and "without notice" in clause_lower:
            score += 3
            found_keywords.append("without notice")
        
        if "penalty" in clause_lower and ("rs" in clause_lower or "rupees" in clause_lower or "inr" in clause_lower):
            score += 3
            if "rs" in clause_lower: found_keywords.append("rs")
            if "rupees" in clause_lower: found_keywords.append("rupees")

        if "not liable" in clause_lower or "no responsibility" in clause_lower:
            score += 3
            if "not liable" in clause_lower: found_keywords.append("not liable")
            if "no responsibility" in clause_lower: found_keywords.append("no responsibility")

        # ----------------------------------------------------
        # 🔥 STEP 3: SENTIMENT ANALYSIS (TEXTBLOB)
        # ----------------------------------------------------
        try:
            sentiment = TextBlob(clause).sentiment.polarity
            # Very Negative language = higher risk (strict constraints)
            if sentiment < -0.2:
                score += 2
            # Mild Negative
            elif sentiment < 0:
                score += 1
        except Exception:
            pass

        # ----------------------------------------------------
        # 🔥 STEP 4: FINAL RISK CLASSIFICATION
        # ----------------------------------------------------
        # The scale:
        # 3 or more = High
        # 2 = Medium
        # 1 = Low
        if score >= 3:
            risk = "High"
        elif score >= 2:
            risk = "Medium"
        else:
            risk = "Low"

        # ❌ Skip LOW clauses if they have a zero score (purely neutral)
        # We also skip Low clauses that only got 1 point purely from mild TextBlob sentiment 
        # but have ZERO keywords, to prevent the report from filling up with 20+ meaningless generic sentences.
        if score == 0:
            continue
            
        if risk == "Low" and len(found_keywords) == 0:
            continue

        # 🔹 Highlight keywords in clause
        highlighted_clause = highlight_keywords(clause, found_keywords)

        results.append({
            "clause": highlighted_clause,
            "risk": risk,
            "keywords": sorted(list(set(found_keywords))),
            "score": score
        })

    return results