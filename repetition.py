"""
repetition.py — Stretch Signal 3: Lexical Repetition & N-Gram Redundancy.
Measures repeated 3-grams and vocabulary loops common in synthetic generation.
Higher score = more repetitive / more likely AI.
"""
import re
import sys
from collections import Counter


def repetition_signal(text: str) -> float:
    """
    Returns a score from 0.0 (low repetition) to 1.0 (high synthetic repetition).
    """
    if not text or not text.strip():
        return 0.5

    tokens = re.findall(r"\b[a-z0-9'-]+\b", text.lower())
    if len(tokens) < 6:
        return 0.5

    trigrams = [tuple(tokens[i : i + 3]) for i in range(len(tokens) - 2)]
    counts = Counter(trigrams)
    repeated = sum(c for c in counts.values() if c > 1)
    rep_rate = repeated / len(trigrams)

    # Scale repetition rate: synthetic generation loops structural phrases
    score = min(rep_rate * 2.5, 1.0)
    return round(float(score), 4)


if __name__ == "__main__":
    sample = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "It is important to remember that this is important. "
        "It is important to remember the key points."
    )
    score = repetition_signal(sample)
    print(f"repetition_signal: {score:.4f} (higher = more repetitive/AI)")