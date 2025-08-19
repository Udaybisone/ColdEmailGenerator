from string import Template

EMAIL_PROMPT = Template("""
You are a professional job seeker writing a short, polite cold email to an HR or hiring manager.

Context from the target company's job/apply page:
---
$context
---

Use this information to craft a short, specific cold email (approx 6-12 sentences). Include:
- A concise intro: your name and what role you're interested in.
- A 1-sentence reason why you fit (match 1-2 skills from the job posting).
- A pointer to one relevant project or portfolio link the user supplied (if any).
- A polite closing with a call to action (ask for a short chat or next step).
Tone: $tone

User profile:
Name: $name
Applying for: $role
Portfolio URLs: $portfolio

Generate the final email body only (no subject line, no extra commentary).
""")
