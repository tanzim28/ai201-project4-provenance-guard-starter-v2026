# Acceptance Criteria — Unit 9 Capstone

Five criteria that define what "working" means for the extended Provenance Guard service, written before testing. At least three criteria directly evaluate this unit's work: the defensive input hardening extension, the run path, and the structured logging instrumentation.

---

## 1. Authentic Human Writing False-Positive Ceiling

Across 5 authentic human writing samples, at most 1 is labelled `high-confidence AI` (a false-positive rate $\le 20\%$).

**Why this target:**
On a publishing platform, false accusations carry severe asymmetric harm: accusing authentic writers of machine generation alienates contributors and destroys platform trust. Conversely, subtle undetected AI text merely leaves unflagged prose on site. A ceiling of at most 1 in 5 protects genuine human creators from automated misclassification.

---

## 2. All Three Classification Labels Remain Reachable

Across representative synthetic and organic inputs, all three primary classification labels (`high-confidence human`, `unsure`, and `high-confidence AI`) are reachable.

**Why this target:**
If our combining weights ($0.50 \times \text{model} + 0.30 \times \text{style} + 0.20 \times \text{rep}$) or decision cutoffs ($0.40$ and $0.78$) are calibrated improperly, the service collapses into a binary flag or renders the high-confidence AI / unsure labels completely unreachable dead space.

---

## 3. Oversized Payload Rejection (Extension)

100% (3 of 3) of request payloads exceeding 20,000 characters sent to `POST /submit` are rejected at the route boundary with an HTTP 400 Bad Request status code.

**Why this target:**
This directly tests the defensive hardening extension. Unbounded input strings trigger severe memory allocation spikes and potential Denial of Service (DoS) inside the local PyTorch causal transformer during tokenization. Catching oversized text at the route boundary ensures system availability without crashing the inference worker.

---

## 4. Zero-Width Evasion Character Stripping (Extension)

100% (3 of 3) of payloads containing invisible zero-width Unicode characters (`\u200b`, `\u200c`, `\u200d`, `\ufeff`) are sanitized and scored cleanly, returning HTTP 200 OK with valid telemetry rather than breaking tokenizer boundaries.

**Why this target:**
This directly tests the evasion-hardening extension. Adversarial actors inject zero-width invisibles between characters to split words, artificially inflate perplexity, and break n-gram repetitions. The pre-scoring sanitization step must neutralize these evasion vectors before the text enters the statistical language model.

---

## 5. Structured Audit Logging of Rejections (Instrumentation)

100% (7 of 7) of rejected or malformed submissions (oversized strings, missing text, non-string types, or missing creator IDs) write an append-only structured entry to `logs/audit.jsonl` recording `event: "rejection"`, `reason`, and a descriptive message.

**Why this target:**
This directly tests the operational instrumentation requirement. In a production safety microservice, failures and rejected inputs cannot simply vanish into silence; every bad request must leave an immutable telemetry record so platform administrators can audit abuse patterns and identify attack spikes.


<!--# Acceptance criteria — Provenance Guard

Five criteria that say what "working" means for this service, written in unit 7
**before** you built it.

**All five are yours.** None are given.

An acceptance criterion names a number or something plainly observable. *"The
detector is accurate"* is an opinion — and perfect AI detection isn't possible
anyway, so it's an opinion about something nobody can deliver. *"Of 10 pieces I
wrote myself, at most 1 is labelled high-confidence AI"* is a criterion.

Under each, write a sentence or two on **why that target**. *"I allow at most 1
false positive in 10 because on a writing site a wrong accusation costs more
than a missed detection"* is a real answer.

> Missing your own targets next unit costs you nothing. Setting a target so
> easy you can't miss it does.

---

## Pick numbers you can defend

**Cover at least three of these five areas.** They're prompts, not a form.

| Area | A question it could answer |
|---|---|
| False positives | How often may a human's writing get called AI? |
| Score spread | How far apart should clearly-AI and clearly-human text score? |
| Label coverage | Is every one of your three labels actually reachable? |
| The appeal path | Does an appeal always change status and always get recorded? |
| Bad input | What happens when `text` is missing, empty, or enormous? |

Two things worth knowing before you pick numbers:

- **The expensive mistake is one-sided.** Missing some AI text costs the site a
  little. Accusing a real writer costs that person a lot. A criterion that
  treats both errors as equally bad is describing a system nobody would ship.
- **Unit 8 tests across three trials, and the target has to hold across all
  three.** Your first signal runs a model, so identical input can score
  differently twice. A target of "at most 1 in 10" against trials of 2, 1, 2 is
  a **miss**.

---
## 1.

Across a calibration set of 10 human-authored writing samples, at most 1 is labelled `high-confidence AI` (a false positive rate $\le$ 10%).

**Why this target:**
On a publishing platform, false positives carry severe asymmetric costs: accusing authentic writers of cheating breaks platform trust and drives contributors away, whereas false negatives merely leave unflagged text on site. Setting a strict upper bound of 1 in 10 protects genuine human authors from automated over-blocking.

---

## 2.

The combined score spread between a known benchmark human text and an unedited raw LLM generation on the same topic is at least 0.35 points on a 0.0 to 1.0 scale.

**Why this target:**
Because our scoring combines predictability (perplexity via GPT-2) and stylometric variety (sentence length variance and type-token ratio), texts with genuine organic variation versus uniform synthetic token flow must separate distinctly rather than clustering tightly around the uncertain middle band.

---

## 3.

Across a diverse test suite of 15 varied text submissions, all three label variants (`high-confidence human`, `unsure`, and `high-confidence AI`) are reached, with at least 3 examples assigned to each label.

**Why this target:**
This ensures our two thresholds create genuine, balanced decision boundaries rather than collapsing into a binary switch or rendering the `unsure` middle zone unreachable dead space.

---

## 4.

100% (5 of 5) of valid POST requests to `/appeal` update the item status in `logs/audit.jsonl` from `decided` to `under_review` while preserving the original scores and appending the creator's explanation.

**Why this target:**
An ethical safety layer must provide an immutable, accountable paper trail. When a user disputes a classification, the system must reliably record their appeal without overwriting the original diagnostic telemetry needed for auditing.

---

## 5.

100% of malformed submissions (missing `text`, empty string `""`, whitespace-only, or missing `creator_id`) return an HTTP 400 bad request status code with a descriptive JSON error object without raising unhandled 500 exceptions or writing corrupt entries to `logs/audit.jsonl`.

**Why this target:**
In a production microservice, edge-case inputs and empty payloads must be caught at the schema validation boundary so they do not crash the downstream tokenizer or log invalid records into the audit database.

---
-->

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 8 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath, like this:

         ## 2. Uncertain cases land in the unsure band

         The system handles uncertain cases well.

         **Why this target:** ...

         > **Revised in unit 8:** Text I judged borderline scores between
         > 0.4 and 0.6 in at least 4 of 5 cases.
         >
         > **Why revised:** "well" gave me nothing to check. I couldn't
         > reach a verdict from it at all.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "At most 1 of 10 of my own pieces flagged as AI" → "at most 3
            of 10", because 1 of 10 turned out to be hard.

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
