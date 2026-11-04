"""
Signal two: the style signal. (Milestone 4)

Signal one reads the text for meaning. This one measures it as text — the
shape of it, without understanding a word.

Three measures:
    sentence_length_spread   do sentences vary in length, or march in step?
    type_token_ratio         how much of the vocabulary repeats?
    punctuation_density      how much punctuation, and how varied?

Higher style_signal score means more likely AI (0.0 = human, 1.0 = AI).
"""

import re
import statistics


def sentences(text: str) -> list[str]:
    """Split into sentences. Rough and good enough — given to you."""
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p for p in parts if p.strip()]


def words(text: str) -> list[str]:
    """Split into lowercase words, punctuation stripped. Given to you."""
    return re.findall(r"[a-z0-9']+", text.lower())


# ── The three measures — IMPLEMENTED ─────────────────────────────────────────

def sentence_length_spread(text: str) -> float:
    """
    How much sentence length varies.
    Returns standard deviation of sentence lengths in words.
    Safely handles single-sentence edge cases without raising an exception.
    Higher spread indicates more organic, bursty human pacing.
    """
    sents = sentences(text)
    if len(sents) < 2:
        return 0.0

    lengths = [len(words(s)) for s in sents]
    # Filter out empty sentences if any
    lengths = [l for l in lengths if l > 0]
    if len(lengths) < 2:
        return 0.0

    return round(float(statistics.stdev(lengths)), 3)


def type_token_ratio(text: str) -> float:
    """
    Unique words over total words (Type-Token Ratio).
    Returns a float between 0.0 and 1.0. Higher means more varied vocabulary.
    """
    all_words = words(text)
    if not all_words:
        return 0.0
    return round(len(set(all_words)) / len(all_words), 3)


def punctuation_density(text: str) -> float:
    """
    Measures expressive punctuation marks (commas, semicolons, dashes, etc.)
    per 100 words. Higher density typically indicates complex human sentence rhythms.
    """
    all_words = words(text)
    if not all_words:
        return 0.0

    # Count commas, semicolons, colons, dashes, hyphens, parentheses, and quotes
    punct_count = len(re.findall(r"[,;:\"'()\-—]", text))
    density = (punct_count / len(all_words)) * 100.0
    return round(density, 2)


# ── Combining them ───────────────────────────────────────────────────────────

def style_signal(text: str) -> float:
    """
    The style signal as a 0–1 score. **Higher means more likely AI.**

    Combines:
      1. Sentence spread: low variation is more AI-like.
      2. Type-token ratio: repetitive vocabulary is more AI-like.
      3. Punctuation density: low structural nuance is more AI-like.
    """
    sents = sentences(text)
    all_words = words(text)

    if not all_words or not sents:
        return 0.50

    # 1. Evaluate sentence length spread (burstiness)
    spread = sentence_length_spread(text)
    # Human writing typically has stdev >= 7.0; AI prose is uniform (stdev <= 3.0)
    spread_score = 1.0 - min(spread / 10.0, 1.0)

    # 2. Evaluate Type-Token Ratio
    ttr = type_token_ratio(text)
    # TTR typically ranges from 0.45 (monotonous) to 0.85 (rich)
    ttr_score = 1.0 - max(min((ttr - 0.40) / 0.45, 1.0), 0.0)

    # 3. Evaluate Punctuation Density
    punct = punctuation_density(text)
    # Density below 4.0 marks per 100 words suggests plain uniform phrasing
    punct_score = 1.0 - min(punct / 12.0, 1.0)

    # Weighted combination: sentence burstiness carries the strongest weight (50%),
    # followed by vocabulary diversity (30%) and punctuation (20%)
    combined = (0.50 * spread_score) + (0.30 * ttr_score) + (0.20 * punct_score)

    return round(float(max(min(combined, 1.0), 0.0)), 4)


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or (
        "The system works well. It handles most cases correctly and provides "
        "good results. Users generally find it easy to use and understand."
    )

    print(f"{len(sentences(text))} sentences, {len(words(text))} words\n")
    print(f"sentence_length_spread   {sentence_length_spread(text)}")
    print(f"type_token_ratio         {type_token_ratio(text)}")
    print(f"punctuation_density      {punctuation_density(text)}")
    print(f"style_signal             {style_signal(text)}   (higher = more likely AI)")