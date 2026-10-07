# CSRF Demo — ISEC3004 Assignment 1 (Group 6)

Demonstrates a CSRF vulnerability, an exploit, and a mitigation.

## Setup

Create and activate a virtual environment, then install Flask.

```bash
# Linux/macOS
python3 -m venv venv
source venv/bin/activate
pip install flask
```

```bat
:: Windows (Command Prompt)
python -m venv venv
venv\Scripts\activate
pip install flask
```

## Run

**Vulnerable app** → http://127.0.0.1:5000

```bash
# Linux/macOS
cd vulnerable && python3 app.py

# Windows
cd vulnerable
python app.py
```

**Exploit** — open `exploit/exploit.html` directly in the browser (no server needed).

For the mitigated version, run `mitigated/app-mitigated.py` the same way.

## Login

```
victim / victim123
attacker / attacker123
user / user123
```

## What's here

- `vulnerable/` — app with the CSRF flaw
- `exploit/`    — attacker page (hidden form submits a forged transfer)
- `mitigated/`  — fixed version (anti-CSRF token)

See the report for the full analysis.