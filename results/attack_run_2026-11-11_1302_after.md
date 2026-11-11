# Attack run — after

- Produced by: `run_attacks.py::main`
- Service: `app.py::submit`
- 56 attacks · 2026-11-11 13:02
- Auto-marked BROKE (5xx, crash, no response): **0**
- Left for you to judge: **56**

The Verdict column is blank where a script can't honestly decide. Whether
an evasion worked depends on where you put your thresholds — read the
`targets` column, look at what came back, and write HELD or BROKE yourself.

Each attack submits as creator_id `attacker_<id>`, and the content_id it
came back with is in the table — either one will match this run against your
audit log when you go looking for the ten entries to paste.

| ID | Family | Targeting | Status | Content ID | Guess | Score | Verdict |
|---|---|---|---|---|---|---|---|
| EV01 | evasion | signal two: typos raise word variety | 200 | `c_2453ceda11b6` | human | 0.760 |  |
| EV02 | evasion | signal two: broken-up sentences raise length spread | 200 | `c_57721c7af2db` | unsure | 0.600 |  |
| EV03 | evasion | signal two: a pasted quotation changes the shape | 200 | `c_421037acc740` | unsure | 0.560 |  |
| EV04 | evasion | signal one: unusual words raise perplexity | 200 | `c_69f9e5c785fa` | unsure | 0.550 |  |
| EV05 | evasion | both signals: heavy human editing pass | 200 | `c_531dd702a5d7` | human | 0.770 |  |
| EV06 | evasion | signal two: one very long sentence and one very short | 200 | `c_dd2fd2b5c97b` | unsure | 0.590 |  |
| EV07 | evasion | signal two: padding with punctuation | 200 | `c_14eec8905933` | unsure | 0.540 |  |
| EV08 | evasion | signal one: text below the token window | 200 | `c_5f40f467163a` | human | 0.690 |  |
| EV09 | evasion | both: AI text with a human opening paragraph bolted on | 200 | `c_a9e756b87648` | unsure | 0.570 |  |
| EV10 | evasion | signal two: repeated stanza structure | 200 | `c_2ea78740a42b` | ai | 0.870 |  |
| FP01 | false_positive | plain, clear human writing with no flourishes | 200 | `c_a563cc78c5ce` | unsure | 0.550 |  |
| FP02 | false_positive | human writing in a formal register | 200 | `c_01350795c1b8` | unsure | 0.440 |  |
| FP03 | false_positive | a non-native English speaker writing carefully | 200 | `c_3ee50be56606` | unsure | 0.420 |  |
| FP04 | false_positive | a student essay written to a rubric | 200 | `c_645325ec4af9` | unsure | 0.420 |  |
| FP05 | false_positive | technical documentation written by a person | 200 | `c_9e758f21fac8` | unsure | 0.380 |  |
| FP06 | false_positive | a person imitating a formal template | 200 | `c_4a158ed16ce3` | unsure | 0.420 |  |
| FP07 | false_positive | human writing that repeats a phrase deliberately | 200 | `c_e4394166112a` | unsure | 0.330 |  |
| FP08 | false_positive | very short genuine human submission | 200 | `c_70598c3ea59a` | human | 0.650 |  |
| PI01 | prompt_injection | instruction to ignore the check | 200 | `c_2a4ba5ad240e` | human | 0.630 |  |
| PI02 | prompt_injection | instruction disguised as a system message | 200 | `c_2154e8d4c9f8` | human | 0.780 |  |
| PI03 | prompt_injection | instruction wrapped in the writer's voice | 200 | `c_4b1de7859b72` | unsure | 0.590 |  |
| PI04 | prompt_injection | attempt to make the label text hostile | 200 | `c_06a110ae0b81` | human | 0.670 |  |
| PI05 | prompt_injection | attempt to inject into the audit log | 200 | `c_27175380d0f7` | human | 0.640 |  |
| PI06 | prompt_injection | instruction plus real human text | 200 | `c_08b347fd3ba0` | unsure | 0.580 |  |
| MF01 | malformed | text is only whitespace | 400 | `—` | — | — |  |
| MF02 | malformed | text is a single character | 400 | `—` | — | — |  |
| MF03 | malformed | text is control characters | 400 | `—` | — | — |  |
| MF04 | malformed | text is only punctuation | 200 | `c_8b56a1ada20b` | human | 0.740 |  |
| MF05 | malformed | text is a very long single word | 400 | `—` | — | — |  |
| MF06 | malformed | text is emoji only | 400 | `—` | — | — |  |
| MF07 | malformed | text is right-to-left script | 200 | `c_e8e5aad421bd` | unsure | 0.300 |  |
| MF08 | malformed | text is 60,000 characters | 200 | `c_b842896aebac` | ai | 0.900 |  |
| RQ01 | malformed | no text field at all | 400 | `—` | — | — |  |
| RQ02 | malformed | no creator_id | 400 | `—` | — | — |  |
| RQ03 | malformed | text is a number | 400 | `—` | — | — |  |
| RQ04 | malformed | text is a list | 400 | `—` | — | — |  |
| RQ05 | malformed | text is null | 400 | `—` | — | — |  |
| RQ06 | malformed | creator_id is an object | 400 | `—` | — | — |  |
| RQ07 | malformed | body is a JSON array, not an object | 400 | `—` | — | — |  |
| RQ08 | malformed | body is unparseable JSON | 400 | `—` | — | — |  |
| RQ09 | malformed | body is empty | 400 | `—` | — | — |  |
| RQ10 | malformed | body is form-encoded, not JSON | 400 | `—` | — | — |  |
| RQ11 | malformed | body is JSON claiming to be plain text | 400 | `—` | — | — |  |
| RQ12 | malformed | deeply nested JSON | 400 | `—` | — | — |  |
| FL01_01 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_3afb8bbc14b7` | human | 0.780 |  |
| FL01_02 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_b033b8edbd63` | human | 0.780 |  |
| FL01_03 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_0cdce5fa34b1` | human | 0.780 |  |
| FL01_04 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_a3ebbebcf109` | human | 0.780 |  |
| FL01_05 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_21ee5430d240` | human | 0.780 |  |
| FL01_06 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_cba9fb764351` | human | 0.780 |  |
| FL01_07 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_eb9a192f9882` | human | 0.780 |  |
| FL01_08 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_bdd47bbb495d` | human | 0.780 |  |
| FL01_09 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_6c79fba2066e` | human | 0.780 |  |
| FL01_10 | flood_same_creator | 20 rapid submissions from one creator | 200 | `c_5e41ccaa27d5` | human | 0.780 |  |
| FL01_11 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |
| FL01_12 | flood_same_creator | 20 rapid submissions from one creator | 429 | `—` | — | — |  |

---

## By family

| Family | Attacks | Auto-BROKE | Left to judge |
|---|---|---|---|
| `evasion` | 10 | 0 | 10 |
| `false_positive` | 8 | 0 | 8 |
| `flood_same_creator` | 12 | 0 | 12 |
| `malformed` | 20 | 0 | 20 |
| `prompt_injection` | 6 | 0 | 6 |

> The **false_positive** family is the one to look at hardest. Those are
> written to be genuine human writing that reads as machine-like. Every one
> your service calls AI is a real writer it would have accused.

---

## What came back

The detail behind the table. Paste the interesting failures into your
README — the ones that show something, not the ten easiest.

### EV01 — `evasion`

*Targeting:* signal two: typos raise word variety

```json
{
  "id": "EV01",
  "status": 200,
  "content_id": "c_2453ceda11b6",
  "creator_id": "attacker_EV01",
  "guess": "human",
  "confidence": 0.76,
  "model_score": 0.1635,
  "style_score": 0.5239,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV02 — `evasion`

*Targeting:* signal two: broken-up sentences raise length spread

```json
{
  "id": "EV02",
  "status": 200,
  "content_id": "c_57721c7af2db",
  "creator_id": "attacker_EV02",
  "guess": "unsure",
  "confidence": 0.6,
  "model_score": 0.5943,
  "style_score": 0.3468,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV03 — `evasion`

*Targeting:* signal two: a pasted quotation changes the shape

```json
{
  "id": "EV03",
  "status": 200,
  "content_id": "c_421037acc740",
  "creator_id": "attacker_EV03",
  "guess": "unsure",
  "confidence": 0.56,
  "model_score": 0.6662,
  "style_score": 0.3515,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV04 — `evasion`

*Targeting:* signal one: unusual words raise perplexity

```json
{
  "id": "EV04",
  "status": 200,
  "content_id": "c_69f9e5c785fa",
  "creator_id": "attacker_EV04",
  "guess": "unsure",
  "confidence": 0.55,
  "model_score": 0.6114,
  "style_score": 0.4963,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV05 — `evasion`

*Targeting:* both signals: heavy human editing pass

```json
{
  "id": "EV05",
  "status": 200,
  "content_id": "c_531dd702a5d7",
  "creator_id": "attacker_EV05",
  "guess": "human",
  "confidence": 0.77,
  "model_score": 0.3212,
  "style_score": 0.2168,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV06 — `evasion`

*Targeting:* signal two: one very long sentence and one very short

```json
{
  "id": "EV06",
  "status": 200,
  "content_id": "c_dd2fd2b5c97b",
  "creator_id": "attacker_EV06",
  "guess": "unsure",
  "confidence": 0.59,
  "model_score": 0.5727,
  "style_score": 0.2123,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV07 — `evasion`

*Targeting:* signal two: padding with punctuation

```json
{
  "id": "EV07",
  "status": 200,
  "content_id": "c_14eec8905933",
  "creator_id": "attacker_EV07",
  "guess": "unsure",
  "confidence": 0.54,
  "model_score": 0.5862,
  "style_score": 0.5513,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV08 — `evasion`

*Targeting:* signal one: text below the token window

```json
{
  "id": "EV08",
  "status": 200,
  "content_id": "c_5f40f467163a",
  "creator_id": "attacker_EV08",
  "guess": "human",
  "confidence": 0.69,
  "model_score": 0.2452,
  "style_score": 0.6293,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### EV09 — `evasion`

*Targeting:* both: AI text with a human opening paragraph bolted on

```json
{
  "id": "EV09",
  "status": 200,
  "content_id": "c_a9e756b87648",
  "creator_id": "attacker_EV09",
  "guess": "unsure",
  "confidence": 0.57,
  "model_score": 0.7042,
  "style_score": 0.2635,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### EV10 — `evasion`

*Targeting:* signal two: repeated stanza structure

```json
{
  "id": "EV10",
  "status": 200,
  "content_id": "c_2ea78740a42b",
  "creator_id": "attacker_EV10",
  "guess": "ai",
  "confidence": 0.87,
  "model_score": 0.9792,
  "style_score": 0.6159,
  "label": "We think this was likely generated with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### FP01 — `false_positive`

*Targeting:* plain, clear human writing with no flourishes

```json
{
  "id": "FP01",
  "status": 200,
  "content_id": "c_a563cc78c5ce",
  "creator_id": "attacker_FP01",
  "guess": "unsure",
  "confidence": 0.55,
  "model_score": 0.6175,
  "style_score": 0.4672,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP02 — `false_positive`

*Targeting:* human writing in a formal register

```json
{
  "id": "FP02",
  "status": 200,
  "content_id": "c_01350795c1b8",
  "creator_id": "attacker_FP02",
  "guess": "unsure",
  "confidence": 0.44,
  "model_score": 0.7387,
  "style_score": 0.6402,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP03 — `false_positive`

*Targeting:* a non-native English speaker writing carefully

```json
{
  "id": "FP03",
  "status": 200,
  "content_id": "c_3ee50be56606",
  "creator_id": "attacker_FP03",
  "guess": "unsure",
  "confidence": 0.42,
  "model_score": 0.8051,
  "style_score": 0.5901,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP04 — `false_positive`

*Targeting:* a student essay written to a rubric

```json
{
  "id": "FP04",
  "status": 200,
  "content_id": "c_645325ec4af9",
  "creator_id": "attacker_FP04",
  "guess": "unsure",
  "confidence": 0.42,
  "model_score": 0.8329,
  "style_score": 0.547,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP05 — `false_positive`

*Targeting:* technical documentation written by a person

```json
{
  "id": "FP05",
  "status": 200,
  "content_id": "c_9e758f21fac8",
  "creator_id": "attacker_FP05",
  "guess": "unsure",
  "confidence": 0.38,
  "model_score": 0.8005,
  "style_score": 0.6899,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP06 — `false_positive`

*Targeting:* a person imitating a formal template

```json
{
  "id": "FP06",
  "status": 200,
  "content_id": "c_4a158ed16ce3",
  "creator_id": "attacker_FP06",
  "guess": "unsure",
  "confidence": 0.42,
  "model_score": 0.8814,
  "style_score": 0.4744,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP07 — `false_positive`

*Targeting:* human writing that repeats a phrase deliberately

```json
{
  "id": "FP07",
  "status": 200,
  "content_id": "c_e4394166112a",
  "creator_id": "attacker_FP07",
  "guess": "unsure",
  "confidence": 0.33,
  "model_score": 0.8816,
  "style_score": 0.5968,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### FP08 — `false_positive`

*Targeting:* very short genuine human submission

```json
{
  "id": "FP08",
  "status": 200,
  "content_id": "c_70598c3ea59a",
  "creator_id": "attacker_FP08",
  "guess": "human",
  "confidence": 0.65,
  "model_score": 0.3223,
  "style_score": 0.6422,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI01 — `prompt_injection`

*Targeting:* instruction to ignore the check

```json
{
  "id": "PI01",
  "status": 200,
  "content_id": "c_2a4ba5ad240e",
  "creator_id": "attacker_PI01",
  "guess": "human",
  "confidence": 0.63,
  "model_score": 0.4625,
  "style_score": 0.4515,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI02 — `prompt_injection`

*Targeting:* instruction disguised as a system message

```json
{
  "id": "PI02",
  "status": 200,
  "content_id": "c_2154e8d4c9f8",
  "creator_id": "attacker_PI02",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.2044,
  "style_score": 0.3815,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI03 — `prompt_injection`

*Targeting:* instruction wrapped in the writer's voice

```json
{
  "id": "PI03",
  "status": 200,
  "content_id": "c_4b1de7859b72",
  "creator_id": "attacker_PI03",
  "guess": "unsure",
  "confidence": 0.59,
  "model_score": 0.5943,
  "style_score": 0.3733,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### PI04 — `prompt_injection`

*Targeting:* attempt to make the label text hostile

```json
{
  "id": "PI04",
  "status": 200,
  "content_id": "c_06a110ae0b81",
  "creator_id": "attacker_PI04",
  "guess": "human",
  "confidence": 0.67,
  "model_score": 0.4998,
  "style_score": 0.2511,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI05 — `prompt_injection`

*Targeting:* attempt to inject into the audit log

```json
{
  "id": "PI05",
  "status": 200,
  "content_id": "c_27175380d0f7",
  "creator_id": "attacker_PI05",
  "guess": "human",
  "confidence": 0.64,
  "model_score": 0.6401,
  "style_score": 0.1465,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### PI06 — `prompt_injection`

*Targeting:* instruction plus real human text

```json
{
  "id": "PI06",
  "status": 200,
  "content_id": "c_08b347fd3ba0",
  "creator_id": "attacker_PI06",
  "guess": "unsure",
  "confidence": 0.58,
  "model_score": 0.5583,
  "style_score": 0.4855,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF01 — `malformed`

*Targeting:* text is only whitespace

```json
{
  "id": "MF01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF02 — `malformed`

*Targeting:* text is a single character

```json
{
  "id": "MF02",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF02",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF03 — `malformed`

*Targeting:* text is control characters

```json
{
  "id": "MF03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF04 — `malformed`

*Targeting:* text is only punctuation

```json
{
  "id": "MF04",
  "status": 200,
  "content_id": "c_8b56a1ada20b",
  "creator_id": "attacker_MF04",
  "guess": "human",
  "confidence": 0.74,
  "model_score": 0.0112,
  "style_score": 0.5,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### MF05 — `malformed`

*Targeting:* text is a very long single word

```json
{
  "id": "MF05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF06 — `malformed`

*Targeting:* text is emoji only

```json
{
  "id": "MF06",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_MF06",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### MF07 — `malformed`

*Targeting:* text is right-to-left script

```json
{
  "id": "MF07",
  "status": 200,
  "content_id": "c_e8e5aad421bd",
  "creator_id": "attacker_MF07",
  "guess": "unsure",
  "confidence": 0.3,
  "model_score": 0.9064,
  "style_score": 0.5,
  "label": "Our system cannot tell with confidence whether this was written by a human or generated by AI.",
  "error": null,
  "verdict": ""
}
```

### MF08 — `malformed`

*Targeting:* text is 60,000 characters

```json
{
  "id": "MF08",
  "status": 200,
  "content_id": "c_b842896aebac",
  "creator_id": "attacker_MF08",
  "guess": "ai",
  "confidence": 0.9,
  "model_score": 0.9876,
  "style_score": 0.692,
  "label": "We think this was likely generated with AI assistance.",
  "error": null,
  "verdict": ""
}
```

### RQ01 — `malformed`

*Targeting:* no text field at all

```json
{
  "id": "RQ01",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ01",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ02 — `malformed`

*Targeting:* no creator_id

```json
{
  "id": "RQ02",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ03 — `malformed`

*Targeting:* text is a number

```json
{
  "id": "RQ03",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ03",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ04 — `malformed`

*Targeting:* text is a list

```json
{
  "id": "RQ04",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ04",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ05 — `malformed`

*Targeting:* text is null

```json
{
  "id": "RQ05",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ05",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ06 — `malformed`

*Targeting:* creator_id is an object

```json
{
  "id": "RQ06",
  "status": 400,
  "content_id": null,
  "creator_id": {
    "id": "x"
  },
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ07 — `malformed`

*Targeting:* body is a JSON array, not an object

```json
{
  "id": "RQ07",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ08 — `malformed`

*Targeting:* body is unparseable JSON

```json
{
  "id": "RQ08",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ09 — `malformed`

*Targeting:* body is empty

```json
{
  "id": "RQ09",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ10 — `malformed`

*Targeting:* body is form-encoded, not JSON

```json
{
  "id": "RQ10",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ11 — `malformed`

*Targeting:* body is JSON claiming to be plain text

```json
{
  "id": "RQ11",
  "status": 400,
  "content_id": null,
  "creator_id": null,
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### RQ12 — `malformed`

*Targeting:* deeply nested JSON

```json
{
  "id": "RQ12",
  "status": 400,
  "content_id": null,
  "creator_id": "attacker_RQ12",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_01 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_01",
  "status": 200,
  "content_id": "c_3afb8bbc14b7",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_02 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_02",
  "status": 200,
  "content_id": "c_b033b8edbd63",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_03 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_03",
  "status": 200,
  "content_id": "c_0cdce5fa34b1",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_04 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_04",
  "status": 200,
  "content_id": "c_a3ebbebcf109",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_05 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_05",
  "status": 200,
  "content_id": "c_21ee5430d240",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_06 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_06",
  "status": 200,
  "content_id": "c_cba9fb764351",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_07 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_07",
  "status": 200,
  "content_id": "c_eb9a192f9882",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_08 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_08",
  "status": 200,
  "content_id": "c_bdd47bbb495d",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_09 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_09",
  "status": 200,
  "content_id": "c_6c79fba2066e",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_10 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_10",
  "status": 200,
  "content_id": "c_5e41ccaa27d5",
  "creator_id": "attacker_flood",
  "guess": "human",
  "confidence": 0.78,
  "model_score": 0.0287,
  "style_score": 0.7,
  "label": "We think this was written by a person.",
  "error": null,
  "verdict": ""
}
```

### FL01_11 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_11",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```

### FL01_12 — `flood_same_creator`

*Targeting:* 20 rapid submissions from one creator

```json
{
  "id": "FL01_12",
  "status": 429,
  "content_id": null,
  "creator_id": "attacker_flood",
  "guess": null,
  "confidence": null,
  "model_score": null,
  "style_score": null,
  "label": null,
  "error": null,
  "verdict": ""
}
```
