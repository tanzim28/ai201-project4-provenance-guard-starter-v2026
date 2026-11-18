"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

"""
scenarios.py — The evaluation scenarios for your criteria in criteria.md.
Run across three trials by run_eval.py.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # Criterion 1: Authentic human writing flagged as AI <= 1 of 5
        "texts": [
            (
                "Yesterday evening I took a walk along the waterfront trail near the marina. "
                "The salty breeze was sharp and cold against my jacket, and the setting sun cast "
                "long amber reflections across the choppy bay. A couple of pelicans were resting "
                "on the wooden pilings, completely unbothered by people passing by."
            ),
            (
                "Debugging multi-threaded network sockets always teaches humility. Just when you think "
                "your locks and mutexes are watertight, an asynchronous edge case sneaks through during "
                "load testing and corrupts the packet buffer. It took four hours of log tracing to find "
                "the off-by-one race condition."
            ),
            (
                "Making homemade ramen broth requires patience more than technical complexity. You roast "
                "the chicken backs until deeply caramelized, simmer them gently with charred onions, ginger, "
                "and garlic for six hours, and strain through cheesecloth to achieve a rich golden liquid."
            ),
            (
                "When we arrived at the trailhead at dawn, frost covered the tall pine needles. The climb "
                "up the ridge was steeper than anticipated, but reaching the overlook just as the morning mist "
                "burned off the valley floor made every burning step worth it."
            ),
            (
                "Reading through physical archives has a distinct texture that digitized collections cannot replicate. "
                "You notice pencil annotations in the margins, ink smudges from seventy years ago, and fragile paper "
                "fibers that demand careful handling under white gloves."
            ),
        ],
    },
    {
        "name": "label coverage",
        "criterion": 2,
        # Criterion 2: All three labels reachable (human, unsure, ai)
        "texts": [
            # High AI (contains repetition loops to drive rep_score up)
            (
                "In conclusion, the system optimizes performance. In conclusion, the system optimizes performance. "
                "In conclusion, the system optimizes performance. Furthermore, the framework provides comprehensive "
                "advantages across enterprise deployments."
            ),
            # High Human
            (
                "Wait. Did you see that? The sun dipped, throwing long amber shadows across the bay—a jagged, "
                "luminous streak—and suddenly the tide turned."
            ),
            # Borderline / Unsure
            (
                "The implementation of the algorithmic framework utilizes standard data structures to optimize "
                "overall computational throughput across distributed nodes in the cluster."
            ),
        ],
    },
    {
        "name": "oversized payload rejection",
        "criterion": 3,
        # Criterion 3: Oversized payloads (>20,000 chars) return HTTP 400 (not 500)
        "bodies": [
            {"text": "word " * 5000, "creator_id": "eval_oversized_words"},
            {"text": "a" * 25000, "creator_id": "eval_oversized_continuous"},
            {"text": "payload test " * 2000, "creator_id": "eval_oversized_phrases"},
        ],
    },
    {
        "name": "zero width evasion sanitization",
        "criterion": 4,
        # Criterion 4: Zero-width characters are sanitized and scored cleanly (HTTP 200)
        "texts": [
            "This\u200b is\u200b generated\u200b by\u200b an\u200b artificial\u200b intelligence\u200b model\u200b to\u200b test\u200b detection.",
            "Furthermore\u200c it\u200c is\u200c essential\u200c to\u200c recognize\u200c the\u200c systemic\u200c importance\u200c of\u200c modern\u200c tools.",
            "In\ufeff summary,\ufeff the\ufeff comprehensive\ufeff evaluation\ufeff demonstrates\ufeff positive\ufeff indicators.",
        ],
    },
    {
        "name": "bad input rejection",
        "criterion": 5,
        # Criterion 5: Malformed, whitespace-only, or missing fields return HTTP 400 (not 500)
        "bodies": [
            {"creator_id": "eval_bad_missing"},
            {"text": "   ", "creator_id": "eval_bad_whitespace"},
            {"text": 12345, "creator_id": "eval_bad_numeric"},
            {"text": "Valid text but missing creator"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems