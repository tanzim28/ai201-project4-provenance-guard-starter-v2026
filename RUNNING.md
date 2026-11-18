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
