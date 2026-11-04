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
$ curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "...", "creator_id": "..."}'
```

```json

```

**An appeal**

```bash
$ curl -X POST http://127.0.0.1:5000/appeal \
  -H "Content-Type: application/json" \
  -d '{"content_id": "...", "reasoning": "..."}'
```

```json

```

**What the log shows afterwards**

```bash
$ curl "http://127.0.0.1:5000/log?limit=3"
```

```json

```

---

## How I Used AI

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 8 — THE TEST ═══════════════════════ -->

---

## Rate Limiting

**My limits:** ___ per minute, ___ per day

**Why those numbers and not others:**
<!-- Think about two people: a real writer submitting their own work a few
     times an hour, and a script sending a thousand variations to map your
     thresholds. Your numbers have to be liveable for the first and hostile to
     the second. -->

**What a caller counts as:** <!-- per address, or per creator_id? They fail
differently — one script can look like a thousand callers, and one household
can look like one. -->

**The run of status codes when I pushed past it:**

<!-- python run_attacks.py --flood 15 -->

```

```

---

## Attack Run — Before

<!-- Every attack with its outcome and a held-or-broke mark.
     `run_attacks.py --label before` produces the table. -->



**Ten audit log entries from the run**

<!-- Choose entries that show the interesting failures, not the ten easiest. -->

```json

```

**The single worst outcome** — the one I'd least want to explain to a writer
whose work got caught by it:



---

## Run Log and Verdicts

<!-- Your five criteria across three trials. `run_eval.py --label before`. -->

| Criterion | Target | Run 1 | Run 2 | Run 3 | Verdict |
|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |
| 2.  |  |  |  |  |  |
| 3.  |  |  |  |  |  |
| 4.  |  |  |  |  |  |
| 5.  |  |  |  |  |  |

**Real output from one trial**, pasted as text, naming the file and function
that produced it:

```json

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



---

## The Improvement

**What I changed:**

**Which diagnosis pointed at it:**

### Attack Run — After

<!-- Same format. `run_attacks.py --label after` -->



**Did it help, and how do I know:**

<!-- Widening the unsure band usually fixes one problem and creates another.
     Reporting that trade honestly is worth full credit. -->



---

## What's Still Broken

<!-- For each attack still getting through and each criterion still missed:
     what you'd do, and why you stopped. -->



**The trade I'd make if this ran for real:**

<!-- Two sentences. Fewer wrong accusations means more AI text getting through.
     Say which way you'd go and WHO PAYS FOR IT. -->



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
