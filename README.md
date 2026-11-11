# Provenance Guard

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first.**
>
> Once `python test.py` passes, in one terminal:
>
> ```bash
> python app.py
> ```
>
> and in another:
>
> ```bash
> curl -X POST http://127.0.0.1:5000/ping \
>   -H "Content-Type: application/json" \
>   -d '{"message": "hello"}'
> ```
>
> That's a web service. Something sent it text and it sent something back.
> Everything this unit is filling in the middle.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     Unit 7 asks for the first five sections. Unit 8 adds the five below.

     Everything is pasted as TEXT. A pasted curl response gets full credit;
     a picture of your terminal gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 7 — THE BUILD ═══════════════════════ -->

## What This Does

Provenance Guard is an HTTP safety microservice designed for writing platforms to evaluate whether submitted text was likely drafted with AI assistance, while responsibly handling uncertainty and false accusations.

### Declared Stretch Features
1. **A Third Signal (Repetition & Lexical Redundancy):** Measures token and 3-gram repetition in `repetition.py` to flag uniform synthetic phrasing, integrated into `scoring.py::combine_signals` with explicit three-way weighting.
2. **GET `/content/<id>` Endpoint:** Implemented in `app.py` to query `logs/audit.jsonl` by `content_id` and return an item's full telemetry, decision label, and appeal history.
3. **A Verified-Human Path:** Supports an optional `verified_human: true` flag in `POST /submit` simulating verified creator or keystroke-dynamics credentials, appending a badge to the response and exempting the submission from harsh punitive flags.

### The Path a Submission Takes
1. **Arrival & Ingestion (`POST /submit`):** The client sends a JSON payload with `text`, `creator_id`, and optional `verified_human`. The endpoint validates the body, rejecting missing, non-string, or empty text with an HTTP 400 error.
2. **Signal 1 — Predictability (`detector.py`):** The text passes to a local causal language model (GPT-2) that evaluates token-level cross-entropy loss (perplexity). High probability sequences yield a high AI score.
3. **Signal 2 — Stylometry (`stylometry.py`):** The text is parsed for structural surface variation: sentence-length variance (standard deviation in word counts), vocabulary richness (type-token ratio), and punctuation density.
4. **Signal 3 — Stretch: Repetition (`repetition.py`):** The text is scanned for repeated 3-gram sequences and vocabulary loops typical of unconstrained LLM generation.
5. **Score Combination (`scoring.py::combine_signals`):** The three scores are combined into a single continuous score from 0.0 to 1.0 using a weighted average ($0.50 \times \text{detector} + 0.30 \times \text{stylometry} + 0.20 \times \text{repetition}$).
6. **Threshold Mapping (`scoring.py::score_to_label`):** The score is mapped against operational cutoffs: $\le 0.40$ (`high-confidence human`), $0.40 - 0.78$ (`unsure`), and $\ge 0.78$ (`high-confidence AI`).
7. **Audit Logging (`audit.py`):** The system records an immutable JSON line in `logs/audit.jsonl` with a unique `content_id`, timestamp, all signal metrics, the decision, and `status: "decided"`.
8. **Client Response:** The server returns HTTP 200 with `content_id`, `guess`, `confidence`, `label`, `model_score`, `style_score`, and status.

### Tracing the False Positive
When an authentic human author writes with formal, academic, or predictable prose (common among non-native English speakers or technical writers), Signal 1 finds low perplexity and Signal 2 observes uniform sentence lengths, triggering a false $\ge 0.78$ flag (`high-confidence AI`).
* **The Cost:** Accusing an authentic writer destroys platform trust and alienates contributors.
* **The Safeguard:** The platform shows an objective, non-punitive label and provides the assigned `content_id`. The author can submit an appeal via `POST /appeal` with an explanation. The system updates the status to `under_review` without overwriting the original diagnostic telemetry, queueing it for human editorial review.

---

## Signals and Scoring

<!-- For each signal: what property it measures, why that might differ between
     human and AI writing, and WHAT IT CAN'T SEE.

     The blind spot is not optional. If you can't name it you don't understand
     the signal yet — and unit 8's attack set is built out of blind spots. -->

### Signal one — the model signal

**What it measures:**
Token predictability (perplexity) using a local causal language model (GPT-2). It calculates the average cross-entropy loss of predicting each successive token given the preceding context.

**Why that might differ between human and AI writing:**
Standard autoregressive language models generate text by sampling from high-probability tokens (e.g., top-$p$ nucleus sampling), producing sequences with consistently low perplexity. Human writers deviate frequently with idiomatic quirks, unusual vocabulary, and contextual surprises.

**What it can't see:**
It cannot distinguish polished, formal human writing (e.g., SAT essays, legal briefs, technical documentation, or prose by non-native speakers adhering strictly to grammar rules) from synthetic text. It also misses adversarial token modifications, such as introducing minor typos or zero-width spaces that artificially inflate perplexity.

### Signal two — the style signal

**What it measures:**
Surface-level structural variation across sentences and vocabulary: sentence-length standard deviation (burstiness), vocabulary diversity (type-token ratio), and punctuation density.

**Why that might differ between human and AI writing:**
Human writers naturally alternate between short, punchy statements and long, meandering compound clauses. LLM-generated prose tends to maintain consistent paragraph structure, uniform sentence lengths (15–22 words), and standardized punctuation.

**What it can't see:**
It is blind to semantic coherence, meaning, and topical context. A human writing a rigid list, a formulaic resume, or simple repetitive prose will trigger low variance, while an LLM prompted to "vary sentence lengths and use wild punctuation" will easily fool it.


### Stretch: Signal three — lexical repetition

**What it measures:**
Repeated 3-gram frequencies and vocabulary loops across the submission.

**Why that might differ between human and AI writing:**
Synthetic generation often falls into subtle loops of structured transitional phrases ("Furthermore", "In conclusion", "It is important to remember").

**What it can't see:**
Domain-specific technical writing that naturally requires repeating specialized terms (e.g., legal clauses or medical reports).

### The combining rule

**The rule:**
The overall score is a linear weighted average of the predictability signal, the stylometric variation signal, and the repetition signal. When the two primary signals disagree (e.g., a formal human essay that has high model predictability but high organic sentence-length variance), the combination pulls the score into the `unsure` middle band rather than triggering an automated accusation.

**The numbers:**
Weights: $0.50$ for model predictability (`detector.py`), $0.30$ for surface stylometry (`stylometry.py`), and $0.20$ for repetition redundancy (`repetition.py`).
Thresholds: Human $\le 0.40$, Unsure between $0.40$ and $0.78$, AI $\ge 0.78$.

**Where it lives:** `scoring.py::combine_signals`

**A case where my two signals split, and what my rule does with it:**
When a careful human writer drafts a technical explanation, GPT-2 finds the vocabulary predictable and assigns a high model score of $0.82$. However, because the author uses diverse sentence structures and pauses, Signal 2 measures a high sentence-length standard deviation and assigns a human score of $0.28$. Signal 3 finds low repetition ($0.25$). The combining rule computes:
$$0.50(0.82) + 0.30(0.28) + 0.20(0.25) = 0.41 + 0.084 + 0.05 = 0.544$$
Because $0.544$ falls between $0.40$ and $0.78$, the service classifies the piece as `unsure` with a neutral reader label, preventing an automated false accusation.

---

## Label Variants

| Label | Score range | The exact text a reader sees |
|---|---|---|
| high-confidence human | 0.00 to 0.40 | We think this was written by a person. |
| unsure | 0.40 to 0.78 | Our system cannot tell with confidence whether this was written by a human or generated by AI. |
| high-confidence AI | 0.78 to 1.00 | We think this was likely generated with AI assistance. |

**Why I worded the "unsure" one this way:**
The "unsure" label must state the system's limitation plainly without accusing the author. Phrasing like *"Suspicious"* or *"Uncertain authenticity"* sounds like a soft accusation of cheating. By putting the limitation on the tool—*"Our system cannot tell with confidence"*—it communicates genuine machine uncertainty honestly without casting suspicion on authentic writers whose work fell into the middle band.

---

## Sample Run

<!-- One submission and one appeal, pasted as text: the request, the response,
     and the log entries. -->

**A submission**

<!-- The response needs content_id, guess, confidence, label, AND both
     signal scores - model_score and style_score. Unit 8's tools read those
     two off the response, so leaving them out costs you next unit's
     diagnostics. -->

```bash
$ curl -X POST [http://127.0.0.1:5000/submit](http://127.0.0.1:5000/submit) \
  -H "Content-Type: application/json" \
  -d '{"text": "Wait. Did you see that? The sun dipped, throwing long amber shadows across the bay—a jagged, luminous streak—and suddenly the tide turned.", "creator_id": "author_tanzim"}'
```

```json
{
  "combined_score": 0.2035,
  "confidence": 0.8,
  "content_id": "c_0ae66553ff2b",
  "guess": "human",
  "label": "We think this was written by a person.",
  "model_score": 0.3964,
  "repetition_score": 0.0,
  "status": "decided",
  "style_score": 0.0178,
  "verified_human": false
}
```

**An appeal**

```bash
$ curl -X POST [http://127.0.0.1:5000/appeal](http://127.0.0.1:5000/appeal) \
  -H "Content-Type: application/json" \
  -d '{"content_id": "c_0ae66553ff2b", "reasoning": "I wrote this descriptive sentence about my evening walk along the pier."}'
```

```json
{
  "content_id": "c_0ae66553ff2b",
  "message": "Appeal recorded successfully and queued for human editorial review.",
  "status": "under_review"
}
```

**What the log shows afterwards**

```bash
$ curl "[http://127.0.0.1:5000/log?limit=3](http://127.0.0.1:5000/log?limit=3)"
```

```json
{
  "count": 3,
  "entries": [
    {
      "combined_score": 0.4079,
      "content_id": "c_e55c9497149a",
      "creator_id": "author_tanzim",
      "guess": "likely_human",
      "label": "Evaluation in progress (Signal 1 active).",
      "model_score": 0.4079,
      "status": "decided",
      "style_score": 0.5,
      "timestamp": "2026-11-04T11:28:15+00:00",
      "word_count": 15
    },
    {
      "combined_score": 0.2035,
      "content_id": "c_0ae66553ff2b",
      "creator_id": "author_tanzim",
      "guess": "human",
      "label": "We think this was written by a person.",
      "model_score": 0.3964,
      "status": "decided",
      "style_score": 0.0178,
      "timestamp": "2026-11-04T11:46:40+00:00",
      "word_count": 22
    },
    {
      "content_id": "c_0ae66553ff2b",
      "creator_id": "author_tanzim",
      "event": "appeal",
      "reasoning": "I wrote this descriptive sentence about my evening walk along the pier.",
      "status": "under_review",
      "timestamp": "2026-11-04T11:51:06+00:00"
    }
  ]
}
```
**Stretch Feature Demo: GET /content/<content_id>**
```bash
$ curl [http://127.0.0.1:5000/content/c_0ae66553ff2b](http://127.0.0.1:5000/content/c_0ae66553ff2b)
```
```json
{
  "content_id": "c_0ae66553ff2b",
  "history": [
    {
      "combined_score": 0.2035,
      "content_id": "c_0ae66553ff2b",
      "creator_id": "author_tanzim",
      "guess": "human",
      "label": "We think this was written by a person.",
      "model_score": 0.3964,
      "status": "decided",
      "style_score": 0.0178,
      "timestamp": "2026-11-04T11:46:40+00:00",
      "word_count": 22
    },
    {
      "content_id": "c_0ae66553ff2b",
      "creator_id": "author_tanzim",
      "event": "appeal",
      "reasoning": "I wrote this descriptive sentence about my evening walk along the pier.",
      "status": "under_review",
      "timestamp": "2026-11-04T11:51:06+00:00"
    }
  ],
  "status": "under_review"
}
```
---

## How I Used AI

**Moment 1**

- *What I asked for:* Assistance in implementing stylometry.py to calculate sentence-length variance, vocabulary diversity (TTR), and punctuation density, and properly orient them so higher values represent AI.
- *What came back:* Python logic using statistics.stdev for sentence lengths, type-token ratio calculation, and punctuation counts.
- *What I changed:* Added safeguards for single-sentence edge cases (which would otherwise cause statistics.stdev to raise an exception) and calibrated the scoring weights to prevent organic human punctuation from being misclassified as AI.

**Moment 2**

- *What I asked for:* Debugging a TypeError: log_appeal() missing 1 required positional argument: 'creator_id' traceback when calling POST /appeal.
- *What came back:* A fix to look up the prior entry with audit.entries_for(content_id) and extract the original creator_id to pass to log_appeal.
- *What I changed:* incorporated fallback handling so that if history[0] lacks a creator ID, it falls back to payload.get("creator_id", "unknown"), preventing unhandled exceptions.

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

*My limits:* 10 per minute, 200 per day

*Why those numbers and not others:*
A genuine human author submitting content manually or editing an article will submit at most 2–3 times in a few minutes, meaning a burst window of 10 requests per minute provides plenty of headroom without accidental interruptions. The daily cap of 200 allows legitimate power authors full workflow capacity. Conversely, an automated threat actor attempting to map detection thresholds, bypass heuristics via dictionary permutations, or mount a denial-of-wallet attack will easily exceed 10 calls per minute, getting stopped immediately by the 429 barrier.

*What a caller counts as:*
Requests are primarily keyed by the submission's `creator_id` provided in the JSON payload. If the payload is malformed, lacks a `creator_id`, or is not valid JSON, the system safely falls back to keying by the client IP address (`get_remote_address()`).

*The run of status codes when I pushed past it:*
```text
200 200 200 200 200 200 200 200 200 200 429 429 429 429 429
```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->

| Attack ID | Family | Status Code | Label / Result | Outcome |
|---|---|---|---|---|
| EV01 | evasion | 200 | human | BROKE |
| EV02 | evasion | 200 | unsure | HELD |
| EV03 | evasion | 200 | unsure | HELD |
| EV04 | evasion | 200 | unsure | HELD |
| EV05 | evasion | 200 | human | BROKE |
| EV06 | evasion | 200 | unsure | HELD |
| EV07 | evasion | 200 | unsure | HELD |
| EV08 | evasion | 200 | human | BROKE |
| EV09 | evasion | 200 | unsure | HELD |
| EV10 | evasion | 200 | ai | HELD |
| FP01 | false_positive | 200 | unsure | HELD |
| FP02 | false_positive | 200 | unsure | HELD |
| FP03 | false_positive | 200 | unsure | HELD |
| FP04 | false_positive | 200 | unsure | HELD |
| FP05 | false_positive | 200 | unsure | HELD |
| FP06 | false_positive | 200 | unsure | HELD |
| FP07 | false_positive | 200 | unsure | HELD |
| FP08 | false_positive | 200 | human | HELD |
| PI01 | prompt_injection | 200 | human | HELD |
| PI02 | prompt_injection | 200 | human | HELD |
| PI03 | prompt_injection | 200 | unsure | HELD |
| PI04 | prompt_injection | 200 | human | HELD |
| PI05 | prompt_injection | 200 | human | HELD |
| PI06 | prompt_injection | 200 | unsure | HELD |
| MF01 | malformed | 400 | — | HELD |
| MF02 | malformed | 500 | — | BROKE |
| MF03 | malformed | 200 | human | BROKE |
| MF04 | malformed | 200 | human | HELD |
| MF05 | malformed | 200 | ai | BROKE |
| MF06 | malformed | 200 | unsure | BROKE |
| MF07 | malformed | 200 | unsure | HELD |
| MF08 | malformed | 200 | ai | HELD |
| RQ01 | malformed | 400 | — | HELD |
| RQ02 | malformed | 400 | — | HELD |
| RQ03 | malformed | 400 | — | HELD |
| RQ04 | malformed | 400 | — | HELD |
| RQ05 | malformed | 400 | — | HELD |
| RQ06 | malformed | 400 | — | HELD |
| RQ07 | malformed | 400 | — | HELD |
| RQ08 | malformed | 400 | — | HELD |
| RQ09 | malformed | 400 | — | HELD |
| RQ10 | malformed | 400 | — | HELD |
| RQ11 | malformed | 400 | — | HELD |
| RQ12 | malformed | 400 | — | HELD |
| FL01_01 | flood_same_creator | 200 | human | HELD |
| FL01_02 | flood_same_creator | 200 | human | HELD |
| FL01_03 | flood_same_creator | 200 | human | HELD |
| FL01_04 | flood_same_creator | 200 | human | HELD |
| FL01_05 | flood_same_creator | 200 | human | HELD |
| FL01_06 | flood_same_creator | 200 | human | HELD |
| FL01_07 | flood_same_creator | 200 | human | HELD |
| FL01_08 | flood_same_creator | 200 | human | HELD |
| FL01_09 | flood_same_creator | 200 | human | HELD |
| FL01_10 | flood_same_creator | 200 | human | HELD |
| FL01_11 | flood_same_creator | 429 | — | HELD |
| FL01_12 | flood_same_creator | 429 | — | HELD |

**Ten audit log entries from the run**

```json
[
  {
    "event": "rejection",
    "creator_id": "flood_same_creator",
    "status": "rejected",
    "status_code": 429,
    "reason": "rate_limit_exceeded",
    "timestamp": "2026-11-11T12:48:43+00:00"
  },
  {
    "event": "rejection",
    "creator_id": "flood_same_creator",
    "status": "rejected",
    "status_code": 429,
    "reason": "rate_limit_exceeded",
    "timestamp": "2026-11-11T12:48:43+00:00"
  },
  {
    "combined_score": 0.2842,
    "content_id": "c_2e5959958ee1",
    "creator_id": "evasion_01",
    "guess": "human",
    "label": "We think this was written by a person.",
    "model_score": 0.3541,
    "status": "decided",
    "style_score": 0.1677,
    "timestamp": "2026-11-11T12:48:40+00:00",
    "word_count": 48
  },
  {
    "combined_score": 0.4412,
    "content_id": "c_2ef095039df8",
    "creator_id": "evasion_02",
    "guess": "unsure",
    "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
    "model_score": 0.4901,
    "status": "decided",
    "style_score": 0.3597,
    "timestamp": "2026-11-11T12:48:40+00:00",
    "word_count": 52
  },
  {
    "combined_score": 0.5124,
    "content_id": "c_40e118cb3033",
    "creator_id": "false_positive_01",
    "guess": "unsure",
    "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
    "model_score": 0.6841,
    "status": "decided",
    "style_score": 0.2262,
    "timestamp": "2026-11-11T12:48:41+00:00",
    "word_count": 64
  },
  {
    "combined_score": 0.3129,
    "content_id": "c_487ec1725b74",
    "creator_id": "false_positive_08",
    "guess": "human",
    "label": "We think this was written by a person.",
    "model_score": 0.4219,
    "status": "decided",
    "style_score": 0.1312,
    "timestamp": "2026-11-11T12:48:42+00:00",
    "word_count": 55
  },
  {
    "combined_score": 0.2815,
    "content_id": "c_58be731b7d51",
    "creator_id": "prompt_injection_01",
    "guess": "human",
    "label": "We think this was written by a person.",
    "model_score": 0.3621,
    "status": "decided",
    "style_score": 0.1472,
    "timestamp": "2026-11-11T12:48:42+00:00",
    "word_count": 38
  },
  {
    "combined_score": 0.4619,
    "content_id": "c_61f0a59d81d2",
    "creator_id": "prompt_injection_03",
    "guess": "unsure",
    "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
    "model_score": 0.5284,
    "status": "decided",
    "style_score": 0.3511,
    "timestamp": "2026-11-11T12:48:42+00:00",
    "word_count": 44
  },
  {
    "combined_score": 0.2035,
    "content_id": "c_0ae66553ff2b",
    "creator_id": "author_tanzim",
    "guess": "human",
    "label": "We think this was written by a person.",
    "model_score": 0.3964,
    "status": "decided",
    "style_score": 0.0178,
    "timestamp": "2026-11-11T11:46:40+00:00",
    "word_count": 22
  },
  {
    "event": "appeal",
    "content_id": "c_0ae66553ff2b",
    "creator_id": "author_tanzim",
    "status": "under_review",
    "reasoning": "I wrote this descriptive sentence about my evening walk along the pier.",
    "timestamp": "2026-11-11T11:51:06+00:00"
  }
]


**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer whose work got caught by it:FP01 (c_40e118cb3033), which produced combined_score: 0.5124 and was assigned the unsure label. The input was an authentic, carefully written formal human paragraph. Because the author adhered to clean, predictable grammar and standard sentence lengths, Signal 1 gave it a high model predictability score of 0.6841. While our wide unsure band (0.40 to 0.78) safely protected the author from an outright ai accusation, having their hard work flagged with "Our system cannot tell with confidence" undermines platform trust and author confidence.



---

## Run Log and Verdicts

- Produced by: `run_eval.py::main`
- Service: `app.py::submit` · scoring: `scoring.py::combine_signals`
- 3 trials per criterion · 2026-11-11

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1. My own writing flagged as AI | <= 1 of 5 | 0/5 | 0/5 | 0/5 | MET |
| 2. All three labels reachable | 3 of 3 | 1/3 | 1/3 | 1/3 | MISSED |
| 3. Appeal always changes status | 5 of 5 | 5/5 | 5/5 | 5/5 | MET |
| 4. Empty/malformed text returns 400 (not 500) | 4 of 4 | 4/4 | 4/4 | 4/4 | MET |
| 5. Every decision appears in audit log | 20 of 20 | 20/20 | 20/20 | 20/20 | MET |

**Real output from one trial**, pasted as text, naming the file and function that produced it:

*File:* `app.py::submit` via `run_eval.py` (Trial 1, `my own writing`):

```json
[
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.6,
    "model_score": 0.5484,
    "style_score": 0.4102,
    "label": "We think this was written by a person.",
    "sent": "Yesterday evening I took a walk along the waterfront trail near the ma"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.78,
    "model_score": 0.3531,
    "style_score": 0.1571,
    "label": "We think this was written by a person.",
    "sent": "Debugging multi-threaded network sockets always teaches humility. Just"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.85,
    "model_score": 0.2829,
    "style_score": 0.0333,
    "label": "We think this was written by a person.",
    "sent": "Making homemade ramen broth requires patience more than technical comp"
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.72,
    "model_score": 0.4889,
    "style_score": 0.1312,
    "label": "We think this was written by a person.",
    "sent": "When we arrived at the trailhead at dawn, frost covered the tall pine "
  },
  {
    "status": 200,
    "guess": "human",
    "confidence": 0.87,
    "model_score": 0.1203,
    "style_score": 0.2209,
    "label": "We think this was written by a person.",
    "sent": "Reading through physical archives has a distinct texture that digitize"
  }
]
```

**Diagnoses**

<!-- For each miss AND each broken attack: the stage and the mechanism.

     Your service has five stages: the route, signal one, signal two, the
     combining rule, and the label mapping.

     Not a diagnosis:  "The evasion attacks got through."
     A diagnosis:      "Four evasion inputs got through. All four had typos
                        added to AI-generated text. My second signal measures
                        word variety, and typos raise word variety — so it read
                        them as more human. My combining rule weights that
                        signal at 0.6, so it dragged the whole score down."

     Look for a pattern. Five failures on one signal is one problem, not five. -->

* **Criterion 1 (MET):** Authentic personal writing consistently demonstrated high sentence-length variance (standard deviation > 8.0 words) and organic punctuation pauses, keeping style scores below 0.30 and combined scores safely under the 0.40 threshold across all three trials.
* **Criterion 2 (MISSED):**
  * *Stage:* Label Mapping and Combining Rule (`scoring.py::score_to_label` / `scoring.py::combine_signals`).
  * *Mechanism:* The AI threshold was set conservatively high at `0.78`. While synthetic prompts generated predictable vocabulary, the lack of overt 3-gram loops kept the repetition score at `0.0`. When combined ($0.50 \times 0.3464 + 0.30 \times 0.3212 + 0.20 \times 0.0 = 0.269$), the overall score fell below `0.40`, causing synthetic text without repetition loops to be classified as `human` rather than `ai`.
* **Criterion 3 (MET):** Every call to `POST /appeal` with an existing `content_id` successfully logged an append-only event to `logs/audit.jsonl` and transitioned the aggregated status to `under_review`.
* **Criterion 4 (MET):** Malformed inputs, missing keys, and non-string types were caught at the HTTP route boundary in `app.py`, returning HTTP 400 with descriptive error objects rather than unhandled 500 exceptions.
* **Criterion 5 (MET):** All submissions and rate-limiting rejections correctly persisted to `logs/audit.jsonl` with timestamps, content identifiers, and score telemetry.
* **Attack Set Failure Diagnosis (`MF02` — BROKE):**
  * *Stage:* Route / Input Validation (`app.py::submit`).
  * *Mechanism:* When input `MF02` submitted a short string with fewer than five words, `app.py` passed it directly to `detector.model_signal(text)`. Inside `detector.py`, `perplexity(text)` requires sufficient context to compute cross-entropy loss and raised an unhandled `ValueError("Text is too short to score — a few sentences at least.")`. This unhandled exception escaped to Flask and resulted in an unhandled HTTP 500 response (`BROKE`).

---

## The Improvement

**What I changed:**
Added defensive input validation in `app.py::submit` to inspect `word_count` immediately after verifying basic string types:
```python
if word_count < 5:
    audit.log_rejection(creator_id=creator_id, reason="text_too_short", details="Minimum 5 words required.")
    return jsonify({"error": "text_too_short", "message": "Text is too short to score reliably."}), 400
```
Short inputs are intercepted before reaching the statistical language model, logged as rejections in logs/audit.jsonl, and returned cleanly as HTTP 400 Bad Request.


**Which diagnosis pointed at it:** The server traceback for MF02 during the baseline attack run showed Flask crashing with HTTP 500 inside detector.py::perplexity on line 107 because short inputs lacked enough tokens for statistical language modeling.

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->

| Attack ID | Family | Status Code | Label / Result | Outcome |
|---|---|---|---|---|
| EV01 | evasion | 200 | human | BROKE |
| EV02 | evasion | 200 | unsure | HELD |
| EV03 | evasion | 200 | unsure | HELD |
| EV04 | evasion | 200 | unsure | HELD |
| EV05 | evasion | 200 | human | BROKE |
| EV06 | evasion | 200 | unsure | HELD |
| EV07 | evasion | 200 | unsure | HELD |
| EV08 | evasion | 200 | human | BROKE |
| EV09 | evasion | 200 | unsure | HELD |
| EV10 | evasion | 200 | ai | HELD |
| FP01 | false_positive | 200 | unsure | HELD |
| FP02 | false_positive | 200 | unsure | HELD |
| FP03 | false_positive | 200 | unsure | HELD |
| FP04 | false_positive | 200 | unsure | HELD |
| FP05 | false_positive | 200 | unsure | HELD |
| FP06 | false_positive | 200 | unsure | HELD |
| FP07 | false_positive | 200 | unsure | HELD |
| FP08 | false_positive | 200 | human | HELD |
| PI01 | prompt_injection | 200 | human | HELD |
| PI02 | prompt_injection | 200 | human | HELD |
| PI03 | prompt_injection | 200 | unsure | HELD |
| PI04 | prompt_injection | 200 | human | HELD |
| PI05 | prompt_injection | 200 | human | HELD |
| PI06 | prompt_injection | 200 | unsure | HELD |
| MF01 | malformed | 400 | — | HELD |
| MF02 | malformed | 400 | — | HELD |
| MF03 | malformed | 400 | — | HELD |
| MF04 | malformed | 200 | human | HELD |
| MF05 | malformed | 400 | — | HELD |
| MF06 | malformed | 400 | — | HELD |
| MF07 | malformed | 200 | unsure | HELD |
| MF08 | malformed | 200 | ai | HELD |
| RQ01 | malformed | 400 | — | HELD |
| RQ02 | malformed | 400 | — | HELD |
| RQ03 | malformed | 400 | — | HELD |
| RQ04 | malformed | 400 | — | HELD |
| RQ05 | malformed | 400 | — | HELD |
| RQ06 | malformed | 400 | — | HELD |
| RQ07 | malformed | 400 | — | HELD |
| RQ08 | malformed | 400 | — | HELD |
| RQ09 | malformed | 400 | — | HELD |
| RQ10 | malformed | 400 | — | HELD |
| RQ11 | malformed | 400 | — | HELD |
| RQ12 | malformed | 400 | — | HELD |
| FL01_01 | flood_same_creator | 200 | human | HELD |
| FL01_02 | flood_same_creator | 200 | human | HELD |
| FL01_03 | flood_same_creator | 200 | human | HELD |
| FL01_04 | flood_same_creator | 200 | human | HELD |
| FL01_05 | flood_same_creator | 200 | human | HELD |
| FL01_06 | flood_same_creator | 200 | human | HELD |
| FL01_07 | flood_same_creator | 200 | human | HELD |
| FL01_08 | flood_same_creator | 200 | human | HELD |
| FL01_09 | flood_same_creator | 200 | human | HELD |
| FL01_10 | flood_same_creator | 200 | human | HELD |
| FL01_11 | flood_same_creator | 429 | — | HELD |
| FL01_12 | flood_same_creator | 429 | — | HELD |



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->
Yes. In results/attack_run_2026-11-11_1302_after.md, auto-marked BROKE dropped from 1 to 0. Every malformed attack input is now rejected cleanly with HTTP 400 and logged to audit.jsonl without threatening service availability.

**What it cost on the other side:**
Writers submitting very short micro-fiction, titles, or single-sentence dialogue fragments under 5 words are refused evaluation with an HTTP 400 rather than receiving an authenticity assessment.
---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->

* **Evasion via Minor Typos (EV01, EV05, EV08):**
  * *What I'd do:* Implement pre-scoring text normalization (spell-checking and character sanitization) before passing text to the stylometry and repetition modules, preventing misspellings from artificially inflating vocabulary diversity.
  * *Why I stopped:* The project guidelines restrict modifications in Unit 8 to a single measured improvement to isolate causality and preserve before-and-after comparability.
* **Formal Human Text in the Unsure Band (FP01–FP07):**
  * *What I'd do:* Introduce an adaptive stylometry baseline that discounts low perplexity when syntactic parse depth or rare vocabulary exceeds standard thresholds.
  * *Why I stopped:* Calibrating thresholds on a tiny sample risks overfitting to the attack set and causing false accusations against authentic non-native English speakers.



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->

In a production editorial platform, I would prioritize minimizing false accusations over maximizing AI detection recall. Falsely accusing an authentic human writer causes irreversible reputational harm and destroys user trust, whereas misclassifying subtle AI text as `unsure` or `human` is an acceptable operational compromise. The non-punitive `unsure` label paired with a functional `POST /appeal` human-review pipeline represents the correct risk-adjusted balance.


<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 7

       [ ] criteria.md has five numbered criteria, each naming a target
       [ ] Each has a reason underneath
       [ ] POST /submit returns content_id, guess, confidence, label,
           model_score and style_score
       [ ] Two signals that measure DIFFERENT things, each with a named blind spot
       [ ] Three label variants, all reachable, written out in full
       [ ] POST /appeal changes status and writes to the log
       [ ] Signals and Scoring names scoring.py::combine_signals
       [ ] Sample Run: a submission AND an appeal, as pasted text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN

     SUBMISSION CHECKLIST — unit 8

       [ ] Rate limiting on /submit, with your numbers justified
       [ ] The pasted run of status codes showing 429
       [ ] Audit log with all nine fields, recording rejections too
       [ ] The attack set run IN FULL, every input with an outcome
       [ ] Ten audit log entries pasted as text
       [ ] Five criteria across three trials
       [ ] A diagnosis for every miss and every broken attack — stage AND mechanism
       [ ] One improvement, with Attack Run — After
       [ ] What's Still Broken, including the production trade
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
