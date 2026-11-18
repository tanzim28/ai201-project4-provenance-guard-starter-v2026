# Running Provenance Guard (Path B: Local with Logs)

This document provides the complete, self-contained run path for the Unit 9 Capstone extension of Provenance Guard. A reviewer can follow these steps from a fresh checkout to start the service, verify the defensive hardening and evasion boundaries, inspect structured logs, and reproduce the three-trial evaluation suite.

---

## 1. Environment & Hardware Requirements

* **Operating System:** macOS (Apple Silicon or Intel), Linux (Ubuntu 22.04+), or Windows 10/11 (via WSL2 or native PowerShell with `curl.exe`).
* **Python Version:** Python 3.11 or higher (Python 3.11.x recommended).
* **RAM / Memory Budget:** 4 GB system RAM minimum.
* **Model Storage & Cache:**
  * **Model:** Hugging Face causal language model (`gpt2`, ~124M parameters).
  * **Disk Footprint:** ~550 MB cached locally in `~/.cache/huggingface/hub/`.
  * **Memory Footprint:** ~500 MB loaded into memory during inference.
* **Why Path B is required:** Free cloud hosting tiers (e.g., Render, Railway free) allocate 512 MB total RAM. PyTorch alone takes 200–800 MB, and the GPT-2 weights require ~550 MB. Because local causal inference exceeds 512 MB, this microservice runs locally with persistent file-backed structured logging (`logs/audit.jsonl`).

---

## 2. Setup from a Clean Checkout

Clone the repository and set up a clean Python virtual environment:

```bash
# 1. Clone repository
git clone [https://github.com/tanzim28/ai201-project4-provenance-guard-starter-v2026.git](https://github.com/tanzim28/ai201-project4-provenance-guard-starter-v2026.git)
cd ai201-project4-provenance-guard-starter-v2026

# 2. Create and activate a clean virtual environment
python3 -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1

# 3. Install pinned dependencies
pip install --upgrade pip
pip install -r requirements.txt

# 4. Verify environment & download GPT-2 weights (one-time ~550 MB download)
python detector.py
```

---

## 3. Starting the Service

Open **Terminal 1** and start the Flask microservice with the single documented command:

```bash
python app.py
```

The service initializes on `http://127.0.0.1:5000` with rate limiting enabled (10 req/min, 200 req/day per creator) and structured audit logging active at `logs/audit.jsonl`.

### Production WSGI Alternative (Gunicorn)
To run with a multi-worker production WSGI server on Unix/macOS:
```bash
gunicorn -w 2 -b 127.0.0.1:5000 app:app
```

---

## 4. Verifying Health & Routes

In **Terminal 2**, verify that the microservice is active and healthy:

### Health Check (`GET /health`)
```bash
curl [http://127.0.0.1:5000/health](http://127.0.0.1:5000/health)
```
**Expected Response (HTTP 200):**
```json
{
  "detector_loaded": true,
  "model": "gpt2",
  "rate_limiting": true,
  "status": "healthy"
}
```

### Standard Submission (`POST /submit`)
```bash
curl -X POST [http://127.0.0.1:5000/submit](http://127.0.0.1:5000/submit) \
  -H "Content-Type: application/json" \
  -d '{"text": "Wait. Did you see that? The sun dipped, throwing long amber shadows across the bay—a jagged, luminous streak—and suddenly the tide turned.", "creator_id": "eval_reviewer"}'
```
**Expected Response (HTTP 200):**
Returns `content_id`, `guess: "human"`, `confidence`, `label`, `model_score`, `style_score`, `repetition_score`, `combined_score`, `status: "decided"`, and request execution `duration` (in seconds).

---

## 5. Testing the Unit 9 Capstone Hardening Extensions

The Capstone extension adds defensive validation to protect against memory exhaustion (DoS) and Unicode zero-width evasion attacks.

### Test A: Oversized Payload Rejection (>20,000 characters)
Send a 25,000-character payload to verify it is intercepted at the route boundary before tokenization:
```bash
python -c "
import requests
long_text = 'word ' * 5000
resp = requests.post('[http://127.0.0.1:5000/submit](http://127.0.0.1:5000/submit)', json={'text': long_text, 'creator_id': 'tester_dos'})
print('Status:', resp.status_code)
print('Response:', resp.json())
"
```
**Expected Outcome:** HTTP `400 Bad Request` with `{"error": "payload_too_large", "message": "Text exceeds maximum allowed length of 20,000 characters."}` and a rejection logged to `logs/audit.jsonl`.

### Test B: Single Continuous String DoS Ceiling
Verify that an oversized continuous word (`"a" * 25000`) is caught by `payload_too_large` rather than being misclassified by word-count:
```bash
python -c "
import requests
huge_word = 'a' * 25000
resp = requests.post('[http://127.0.0.1:5000/submit](http://127.0.0.1:5000/submit)', json={'text': huge_word, 'creator_id': 'tester_continuous'})
print('Status:', resp.status_code)
print('Response:', resp.json())
"
```
**Expected Outcome:** HTTP `400 Bad Request` with `{"error": "payload_too_large"}`.

### Test C: Zero-Width Unicode Evasion Sanitization
Send text containing invisible zero-width spaces (`\u200b`, `\u200c`, `\u200d`, `\ufeff`) injected between letters:
```bash
curl -X POST [http://127.0.0.1:5000/submit](http://127.0.0.1:5000/submit) \
  -H "Content-Type: application/json" \
  -d '{"text": "This\u200b is\u200b generated\u200b by\u200b an\u200b artificial\u200b intelligence\u200b model\u200b to\u200b test\u200b detection.", "creator_id": "tester_evasion"}'
```
**Expected Outcome:** HTTP `200 OK`. The server strips the invisible codepoints, calculates `word_count = 11`, scores token perplexity on the cleaned string, and returns valid telemetry.

---

## 6. Inspecting Structured Audit Logs

Every decision and rejection is appended to `logs/audit.jsonl` with structured fields:
* **Decisions:** `timestamp`, `content_id`, `creator_id`, `guess`, `model_score`, `style_score`, `combined_score`, `label`, `status`, `word_count`, `duration`.
* **Rejections:** `timestamp`, `creator_id`, `status: "rejected"`, `status_code`, `reason`, `details`, `duration`.

View the last 5 entries directly from the terminal:
```bash
tail -n 5 logs/audit.jsonl | jq .
```
Or query via the microservice HTTP endpoint:
```bash
curl "[http://127.0.0.1:5000/log?limit=5](http://127.0.0.1:5000/log?limit=5)"
```

---

## 7. Running the Full Three-Trial Evaluation Suite

To reproduce the acceptance criteria results reported in `README.md`:

```bash
# In Terminal 2, ensure virtualenv is active:
source .venv/bin/activate

# Execute the 3-trial test harness:
python run_eval.py --label capstone_eval
```

This sends all scenarios defined in `scenarios.py` across three independent trials against the running service, writes structured output files to `results/run_<timestamp>_capstone_eval.md`, and prints per-trial classification verdicts.
Everything about how the starter works.

This is a **web service**. It runs on your machine and you talk to it with
`curl` from another terminal. If you've not built a backend before, that's
assumed — the starter ships one that already answers.

---

## Before your first class

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python test.py
```

**You're ready when `python test.py` passes.**

You'll see `[WARN] Detector model — not downloaded yet`:

```bash
python detector.py
```

That downloads about 550 MB and scores a sample.

> **No API key for this pair.** Nothing here calls a hosted service. The model
> that reads your text runs on your own laptop.

---

## Your first five minutes

Two terminals. In the first:

```bash
python app.py
```

In the second:

```bash
curl -X POST http://127.0.0.1:5000/ping \
  -H "Content-Type: application/json" \
  -d '{"message": "hello"}'
```

You should get JSON back. That's the whole idea of a web service — something
sent it data, it sent something back.

> **On Windows, use `curl.exe` and keep it on one line.**
>
> In PowerShell, `curl` is an alias for a different tool and the command above
> fails with `Cannot bind parameter 'Headers'` before it ever reaches your
> service. The `\` line breaks don't work there either. This does:
>
> ```powershell
> curl.exe -X POST http://127.0.0.1:5000/ping -H "Content-Type: application/json" -d '{\"message\": \"hello\"}'
> ```
>
> Every `curl` command in this file and in the brief works the same way: swap
> `curl` for `curl.exe` and put it on one line. Git Bash needs no change.

**Leave `/ping` alone.** It's your control. When something breaks later, check
`/ping` still answers: if it does, the problem is in your handler; if it
doesn't, it's the service itself, and that's a help-channel question.

Then try the route you're going to build:

```bash
curl -X POST http://127.0.0.1:5000/submit \
  -H "Content-Type: application/json" \
  -d '{"text": "some writing", "creator_id": "me"}'
```

It returns a `501` saying it isn't built yet. **That's the correct starting
position.**

---

## The routes

| Route | State | What it does |
|---|---|---|
| `POST /ping` | **works** | The example. Don't edit it |
| `GET /health` | **works** | Is the service up, is the model loaded |
| `GET /log` | **works** | The audit log, as JSON |
| `POST /submit` | **you build it** | Milestones 3, 4, 5 |
| `POST /appeal` | **you build it** | Milestone 5 |

---

## Every command

| Command | What it does |
|---|---|
| `python test.py` | Checks your environment |
| `python app.py` | Runs the service |
| `python detector.py` | Downloads the model and scores a sample — **run before class** |
| `python detector.py "some text"` | Score one piece of text from the terminal |
| `python stylometry.py "some text"` | Your style measures, on one piece of text |
| `python run_attacks.py --set <folder>` | The attack set — **unit 8** |
| `python run_attacks.py --flood 15` | Push past your rate limit and print the status codes — **unit 8** |
| `python run_eval.py --label before` | Your five criteria, three trials — **unit 8** |

---

## Which piece goes with which milestone

### Unit 7 — the build

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Trace a submission on paper | Nothing to run |
| 2 | Write your criteria | `criteria.md` — all five are yours |
| 3 | The route, one signal, the log | `app.py::submit`, `detector.py`, `audit.py` |
| 4 | Second signal, combine, score | `stylometry.py`, `scoring.py::combine_signals` |
| 5 | Labels and the appeal path | `scoring.py::score_to_label`, `app.py::appeal` |
| 6 | Write it up | `README.md` |

### Unit 8 — the test

| Milestone | What you're doing | Where |
|---|---|---|
| 1 | Rate limiting and the full log | `config.py`, the decorator in `app.py` |
| 2 | Run the attack set | `run_attacks.py` |
| 3 | Run your own criteria | `scenarios.py`, `run_eval.py` |
| 4 | Verdicts and diagnoses | `README.md` |
| 5 | Fix one thing, re-run | `run_attacks.py --label after` |
| 6 | What's still broken | `README.md` |

---

## Building `/submit` in three passes

The ordering is deliberate. It's how you tell a broken route from a broken
signal.

**Milestone 3.** Return a hardcoded response. Confirm `curl` gets it back
**before** you add any logic. Then pull `text` and `creator_id` out. Then call
one signal. Then log it.

**Milestone 4.** Add the second signal. Combine them. Log both scores.

**Milestone 5.** Turn the score into a label.

> Test each signal from a terminal on its own before wiring it in. If you skip
> that you'll spend an hour not knowing whether the route or the signal is
> lying to you.

---

## Turning on rate limiting (unit 8)

Three steps:

1. In `config.py`, set `RATE_LIMITING_ENABLED = True` — or run with
   `AI201_RATE_LIMITS=1`.
2. Choose your numbers there.
3. In `app.py`, uncomment the `@limiter.limit(...)` line above `submit`.

Then push past your limit and watch for `429`:

```bash
python run_attacks.py --flood 15
```

That sends 15 submissions from one `creator_id` and prints the run of status
codes — `200 200 200 ... 429 429` — which is exactly what your README's **Rate
Limiting** section asks you to paste. It also writes `results/flood_<date>.md`.

The attack set can't do this for you. Every attack row submits under its own
`creator_id`, so a full attack run looks like forty-odd different callers and
never trips a limit however long it is.

No `429` at all? Either your limit is above 15 a minute, or rate limiting is
still off. `GET /health` reports which.

Rejections are logged for you. **An attack that shows up only as an absence is
one you'll never find** — a thousand requests that got a `429` and left no
trace look exactly like a quiet afternoon.

---

## Running it somewhere else (unit 9)

Unit 9 asks you to deploy one of your systems. **Read this before you pick
which one** — for this project the answer is already decided, and it isn't the
hosted one.

Flask's built-in server says "development server" on startup because that's
what it is. A real one comes from `gunicorn`, which is in
`requirements.txt` and unused until now:

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

Two settings do the work, and both read the environment:

| Variable | Default | What it does |
|---|---|---|
| `HOST` | `127.0.0.1` | Loopback — your machine only. A host needs `0.0.0.0`, or nothing outside the box can reach the service and it looks like the app is down |
| `PORT` | `5000` | Most hosts hand you a port in `PORT` and expect you to bind exactly that one |
| `AI201_DEBUG` | `1` | Debug mode. Off automatically whenever `HOST` isn't loopback — an interactive debugger on a public address is a stranger's Python prompt inside your process |

Nothing about your local workflow changes. With no variables set you get
`http://127.0.0.1:5000` and every `curl` above still works.

### This project will not fit a free host

Say it plainly, because the arithmetic is the point:

| What has to be in memory | Roughly |
|---|---|
| `torch` | ~200–800 MB depending on the build |
| the `gpt2` weights | ~550 MB on disk, loaded into RAM to score |
| Flask, gunicorn, your code | the rest |
| **A free tier gives you** | **512 MB** |

That's over budget before a single request arrives — and a free host has no
persistent disk, so the 550 MB download starts again after every idle
spin-down. There is no configuration that fixes this. The model is the size it
is.

**So pair 4 extensions take Path B — local, with logs.** That is the expected
answer for this project, not a fallback and not a failure. Working out that a
system doesn't fit its host *before* you spend an evening watching it get
killed is the skill unit 9 is actually testing. Write the arithmetic above in
your write-up; that's the deliverable.

---

## Where everything lives

| File | What it does |
|---|---|
| `config.py` | Every setting: thresholds, weights, rate limits, the model |
| `app.py` | The service. `/ping` and `/log` work; `/submit` and `/appeal` are yours |
| `detector.py` | Signal one — the local model. Given to you |
| `stylometry.py` | Signal two. **Stubs — you build these** |
| `scoring.py` | Combining and labelling. **Stubs — you build these** |
| `audit.py` | The audit log writer. Given to you |
| `run_attacks.py` | Runs the attack set — **unit 8** |
| `run_eval.py` | Runs your criteria three times — **unit 8** |
| `scenarios.py` | What your test runs. **You fill this in** |
| `criteria.md` | Your five criteria. **You write all five** |
| `logs/audit.jsonl` | Your audit log. **Commit it** |
| `results/` | Attack runs and run logs. **Commit them** |

---

## The two blind spots, up front

Both signals have one, and unit 8's attack set is built out of them. You have
to name them yourself in Milestone 1 — but knowing they exist now saves you
from being surprised.

**Signal one** measures how *predictable* your text is. Predictability isn't
authorship. What it really rewards is common words in short, ordinary
sentences — someone writing in a second language and staying with vocabulary
they're sure of, a younger writer, anyone writing plainly on purpose. Writing
like that scores about as machine-like as machine writing does. (Dense, ornate
prose often goes the other way and reads as human, because rare words are what
a language model fails to predict.) So the writers this signal is most likely
to accuse are the ones with the least room to argue back. That is the false
positive the whole project is about, and it's structural rather than a bug.

**Signal two** cannot read. It has no idea what the text says. Anything that
changes the shape without changing the substance moves it — typos, broken-up
sentences, a pasted quotation. That is very cheap to do on purpose.

---

## When something goes wrong

| What you see | What it means |
|---|---|
| `501 not_implemented` | Correct at the start — that's the TODO in `app.py` |
| `404` from curl | Is the server running? Is the path exactly what you typed? |
| `Cannot bind parameter 'Headers'` | You're in PowerShell, where `curl` is a different tool. Use `curl.exe`, on one line |
| Request body arrives empty | curl needs `-H "Content-Type: application/json"` |
| `Address already in use` | A server left running from an earlier attempt. Kill it, don't debug it |
| The first submission takes 10+ seconds | Signal one is loading the model into memory. Later ones take a second or two |
| *Every* submission takes 10+ seconds | Something is reloading the model each call. `GET /health` shows `detector_loaded` — if it goes back to `false`, look for a reload in your handler |
| `DetectorUnavailable` | Run `python detector.py` once to download the model |
| `/appeal` seems to do nothing | Does the `content_id` you sent actually exist in the log? A typo there fails silently |
| Every request gets through, no `429` ever | The decorator is uncommented but limiting is still off. Set `RATE_LIMITING_ENABLED` in `config.py` |
| Flask-Limiter warns about storage | Shouldn't happen — `storage_uri` is preconfigured. If you changed it, put it back |
| All three of your labels never appear | Your ranges have a gap. `scoring.label_ranges()` prints them |

If the route won't respond, go back to `/ping`. If that answers, the problem is
in your handler.

---

## A note on committing

At least four new commits in unit 7, four more in unit 8.

`logs/` and `results/` are deliberately **not** in `.gitignore`. Your audit log
is evidence, and the entries you paste into your README are what unit 8 grades.

**Do not delete and recreate this repository.** You submit the same URL both
units.
