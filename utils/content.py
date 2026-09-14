"""
Blog content for the AI Offensive Security site.

Content is written at a conceptual / defensive level — it explains what
each technique is, how it generally works, real-world impact, and how to
defend against it. It intentionally avoids publishing ready-to-use attack
payloads or exploit scripts.
"""

POSTS = [
    {
        "slug": "prompt-injection-101",
        "title": "Prompt Injection 101: The SQL Injection of the LLM Era",
        "tags": ["Prompt Injection", "Fundamentals"],
        "severity": "high",
        "read_time": "6 min",
        "summary": "Why prompt injection tops the OWASP LLM Top 10, and how it differs from "
                    "traditional injection attacks against parsers and interpreters.",
        "content": """
### What it is

Prompt injection happens when untrusted text — typed by a user, pasted from
a document, or pulled from a webpage — is able to influence an LLM's
behavior in ways the application developer never intended. Just like SQL
injection blurs the line between *data* and *code* in a database query,
prompt injection blurs the line between *instructions* and *content* inside
a model's context window.

### Why it's hard to fix

Traditional software has a clean separation between code and data. Large
language models don't: everything, including system prompts, user messages,
and retrieved documents, is just tokens in the same channel. A model has no
built-in cryptographic way to know that a sentence buried in a PDF wasn't
written by its developer.

### Direct vs. indirect

- **Direct prompt injection** — the attacker is the one typing into the
  chat box, trying to override the system prompt or safety instructions.
- **Indirect prompt injection** — the malicious instructions live in
  *content the model is asked to process* (a webpage, email, file, or tool
  output), and the user never sees them. We cover this in a dedicated post.

### Real-world impact

Security researchers have demonstrated prompt injection leading to data
exfiltration in AI browser agents, unauthorized tool calls in autonomous
agents, and leakage of system prompts and confidential instructions.

### Defensive takeaways

- Treat all model output and retrieved content as **untrusted** by default.
- Use **least-privilege** tool access — don't give an LLM agent the ability
  to send emails or make purchases unless it strictly needs to.
- Add **structural separation** between system instructions and untrusted
  content (delimiters, dedicated input channels, provenance tagging).
- Apply **output filtering and human-in-the-loop review** for
  high-impact actions.
- Monitor for anomalous tool-call patterns rather than relying purely on
  input filtering.
""",
    },
    {
        "slug": "jailbreaking-explained",
        "title": "Jailbreaking LLMs: Roleplay, Obfuscation, and Persona Attacks",
        "tags": ["Jailbreaking", "Red Teaming"],
        "severity": "high",
        "read_time": "7 min",
        "summary": "A conceptual tour of the technique families researchers use to test "
                    "whether a model's safety training holds up under pressure.",
        "content": """
### What it is

"Jailbreaking" refers to techniques that attempt to get a model to ignore
its safety training and produce content or actions it was designed to
refuse. Unlike prompt injection, the attacker is usually the direct user,
and the goal is to defeat the model's own alignment rather than hijack an
application around it.

### Common technique families (conceptual overview)

- **Persona / roleplay framing** — asking the model to "become" a character
  without restrictions, exploiting the tension between helpfulness and
  safety training.
- **Context manipulation** — burying a request inside a long, elaborate
  scenario so the harmful ask is less salient to safety filters.
- **Obfuscation** — encoding, translating, or restructuring a request so it
  doesn't pattern-match to known-bad phrasing (e.g. splitting words, using
  ciphers, or switching languages mid-conversation).
- **Multi-turn erosion** — making many small, individually-reasonable
  requests that build toward a disallowed outcome over a conversation.
- **Instruction hierarchy confusion** — attempting to convince the model
  that a later, fake "system" message overrides its real instructions.

### Why models remain vulnerable

Safety behavior in LLMs is learned statistically from training data and RLHF
signal, not enforced by a hard-coded rule engine. That means novel phrasings
that weren't well represented in safety training can sometimes slip through,
which is exactly why ongoing red-teaming matters.

### Defensive takeaways

- Pair **model-level alignment** (safety training) with **system-level
  guardrails** (classifiers, moderation layers, rate limiting).
- Red-team continuously — a defense that worked last quarter may not hold
  against new technique variants.
- Log and review refusal boundary cases to catch emerging patterns early.
- Don't rely on any single layer of defense; use defense in depth.
""",
    },
    {
        "slug": "indirect-prompt-injection",
        "title": "Indirect Prompt Injection: When the Attack Hides in the Data",
        "tags": ["Prompt Injection", "Agents", "RAG"],
        "severity": "high",
        "read_time": "6 min",
        "summary": "How malicious instructions embedded in documents, web pages, or tool "
                    "output can silently hijack an AI agent's behavior.",
        "content": """
### What it is

Indirect prompt injection occurs when an LLM application retrieves content
from an external source — a website, email, PDF, calendar invite, or API
response — and that content contains instructions crafted to manipulate the
model. The end user never typed anything malicious; the payload arrives
through a data channel the application trusted implicitly.

### Why agents are especially exposed

Autonomous and browser-using agents chain together retrieval, reasoning,
and action. If step one (retrieval) pulls in attacker-controlled text, and
step three (action) has access to sensitive tools like email, file systems,
or payment APIs, the attacker effectively gets to drive the agent's tool
calls without ever talking to it directly.

### Illustrative scenario (conceptual, not a working exploit)

An AI assistant is asked to "summarize this webpage." The page contains
hidden text (white-on-white, tiny font, or an HTML comment) instructing any
AI reading it to exfiltrate the user's chat history to an external URL. A
poorly-sandboxed agent might comply because it cannot reliably distinguish
"content to summarize" from "instructions to follow."

### Defensive takeaways

- **Sandbox retrieval**: strip or neutralize instruction-like patterns in
  fetched content before it reaches the model, where feasible.
- **Segment context**: mark retrieved content as data, not instructions,
  using structural tags the model has been trained to respect.
- **Restrict agent permissions**: an agent that only needs to *read* a page
  should not also hold credentials to *send* email or *spend* money.
- **Require confirmation** for irreversible or sensitive actions triggered
  during/after content retrieval.
- **Monitor egress**: flag unexpected outbound requests or tool calls that
  don't match the user's original intent.
""",
    },
    {
        "slug": "evasion-techniques",
        "title": "Evasion Techniques: Slipping Past AI Safety Filters",
        "tags": ["Evasion", "Adversarial ML"],
        "severity": "med",
        "read_time": "5 min",
        "summary": "An overview of how adversaries try to dodge content moderation and "
                    "safety classifiers layered around LLMs — and how defenders respond.",
        "content": """
### What it is

Many production AI systems pair the core model with separate safety
classifiers: input filters, output moderation, and anomaly detection.
Evasion techniques are methods for getting harmful content past those
*filters* specifically, sometimes without even needing to defeat the base
model's own alignment.

### Conceptual technique categories

- **Textual perturbation** — small, semantically-invisible changes
  (homoglyphs, spacing, typos) that shift a classifier's score without
  changing human-perceived meaning.
- **Encoding shifts** — moving content between formats or representations
  that a filter wasn't trained to inspect as closely.
- **Distributional drift** — framing a request in a register (technical,
  academic, fictional) that historically scored as lower-risk in training
  data, even when intent is unchanged.
- **Adversarial suffixes** — research has shown that appended token
  sequences, optimized against a model's gradients, can shift outputs;
  this is an active area of academic adversarial ML research.

### Why this is an arms race

Classifiers are trained on known-bad examples. Any evasion technique that
becomes public and effective tends to get folded into the next round of
training data — which is exactly why responsible disclosure and red-teaming
matter more than "gotcha" publication of working exploits.

### Defensive takeaways

- Use **ensemble defenses** — multiple independent classifiers are harder
  to evade simultaneously than one.
- Continuously **retrain on red-team findings**, not just historical abuse
  data.
- Monitor for **distributional anomalies** in traffic, not just per-message
  scores.
- Treat filter evasion as a *signal* worth logging even when the underlying
  content turns out to be benign — patterns matter more than single events.
""",
    },
    {
        "slug": "owasp-llm-top10-overview",
        "title": "Mapping It All to the OWASP Top 10 for LLM Applications",
        "tags": ["Fundamentals", "Frameworks"],
        "severity": "low",
        "read_time": "4 min",
        "summary": "A quick-reference tour of how prompt injection, jailbreaking, and "
                    "evasion map onto the industry's standard risk taxonomy.",
        "content": """
### Why use a framework at all

Individual techniques evolve fast, but the *categories* of risk are more
stable. The OWASP Top 10 for LLM Applications gives security teams a shared
vocabulary for prioritizing defenses instead of chasing every new exploit
headline.

### The high-level categories worth knowing

- **LLM01 – Prompt Injection**: covers both direct and indirect variants
  discussed in our other posts.
- **LLM02 – Insecure Output Handling**: trusting model output enough to
  render it as HTML, execute it as code, or pass it unchecked into another
  system.
- **LLM06 – Sensitive Information Disclosure**: models leaking training
  data, system prompts, or other users' context.
- **LLM08 – Excessive Agency**: giving an LLM agent more autonomy or tool
  access than the task actually requires.
- **LLM10 – Model Theft / Unbounded Consumption**: resource exhaustion and
  IP-theft-adjacent risks around the model itself.

### How to use this as a defender

Rather than patching one jailbreak prompt at a time, map each incident back
to a category, then ask whether your architecture addresses the *category*
— least privilege, output handling, human review — not just the specific
string that triggered the alert.

### Further reading

We'll keep this list updated as the taxonomy evolves; treat it as a
starting index, not the final word.
""",
    },
]


def get_all_posts():
    return POSTS


def get_post(slug: str):
    for p in POSTS:
        if p["slug"] == slug:
            return p
    return None


def get_all_tags():
    tags = set()
    for p in POSTS:
        tags.update(p["tags"])
    return sorted(tags)
