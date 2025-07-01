import re
import json
import os
from pypdf import PdfReader
from datetime import datetime, timedelta
from config import (
    KEYWORDS,
    CONTEXT_MODIFIERS,
    DATE_PATTERN,
    SCORING_THRESHOLDS,
    DATE_WINDOW_DAYS,
    DATE_MATCH_SCORE,
    TITLE_HEADING_BONUS,
)
from custom_types import ClassificationResult

# --- Helper Functions ---


def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()
    text = ""

    if ext == ".pdf":
        with open(file_path, "rb") as f:
            reader = PdfReader(f, strict=False)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    else:
        raise ValueError(f"Unsupported file format: {ext}")

    return text.lower()


def score_keywords(text, title_and_headings):
    score = 0
    key_phrases = []
    reasoning_parts = []

    for level, config in KEYWORDS.items():
        for keyword in config["keywords"]:
            count = text.count(keyword)
            if count > 0:
                score += count * config["score"]
                key_phrases.append(keyword)
                reasoning_parts.append(
                    f"Found '{keyword}' {count} times ({config['score']} pts each)"
                )

                if keyword in title_and_headings:
                    score += TITLE_HEADING_BONUS
                    reasoning_parts.append(
                        f"'{keyword}' appears in title/heading (+{TITLE_HEADING_BONUS} pts)"
                    )

    return score, key_phrases, reasoning_parts


def apply_context_modifiers(text):
    score = 0
    reasoning_parts = []

    for modifier in CONTEXT_MODIFIERS:
        matches = len(re.findall(modifier["pattern"], text))
        if matches > 0:
            score += matches * modifier["score"]
            reasoning_parts.append(
                f"Modifier match: '{modifier['pattern']}' x{matches} ({modifier['score']} pts each)"
            )

    return score, reasoning_parts


def check_recent_dates(text):
    score = 0
    reasoning_parts = []

    dates = re.findall(DATE_PATTERN, text, flags=re.IGNORECASE)

    for date_str in dates:
        parsed_date = None
        for fmt in ("%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%Y-%m-%d"):
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                break
            except ValueError:
                continue

        if parsed_date and datetime.now() <= parsed_date <= datetime.now() + timedelta(
            days=DATE_WINDOW_DAYS
        ):
            score += DATE_MATCH_SCORE
            reasoning_parts.append(
                f"Recent date within {DATE_WINDOW_DAYS} days found: '{date_str}' (+{DATE_MATCH_SCORE} pts)"
            )

    return score, reasoning_parts


def classify_score(score):
    if score >= SCORING_THRESHOLDS["HIGH_PRIORITY"]:
        return "HIGH_PRIORITY", "immediate_follow_up"
    elif score >= SCORING_THRESHOLDS["MEDIUM_PRIORITY"]:
        return "MEDIUM_PRIORITY", "include_in_weekly_digest"
    elif score >= SCORING_THRESHOLDS["LOW_PRIORITY"]:
        return "LOW_PRIORITY", "log_for_background_awareness"
    else:
        return "IRRELEVANT", "ignore"


# --- Main Classifier Function ---


def classify_document(file_path, save_output=False) -> ClassificationResult:
    try:
        text = extract_text(file_path)
    except Exception as e:
        raise RuntimeError(f"Failed to extract text from '{file_path}': {e}")

    lines = text.splitlines()
    title_and_headings = " ".join(lines[:5])

    score = 0
    key_phrases = []
    reasoning_parts = []

    kw_score, kw_phrases, kw_reasoning = score_keywords(text, title_and_headings)
    score += kw_score
    key_phrases.extend(kw_phrases)
    reasoning_parts.extend(kw_reasoning)

    ctx_score, ctx_reasoning = apply_context_modifiers(text)
    score += ctx_score
    reasoning_parts.extend(ctx_reasoning)

    date_score, date_reasoning = check_recent_dates(text)
    score += date_score
    reasoning_parts.extend(date_reasoning)

    classification, recommended_action = classify_score(score)

    output = {
        "classification": classification,
        "score": score,
        "reasoning": "; ".join(reasoning_parts),
        "key_phrases": list(set(key_phrases)),
        "recommended_action": recommended_action,
        "source_file": file_path,
    }

    if save_output:
        output_path = file_path + ".json"
        with open(output_path, "w", encoding="utf-8") as f_out:
            json.dump(output, f_out, indent=2)

    return output
