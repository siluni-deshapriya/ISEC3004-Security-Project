# Log Injection Demo — ISEC3004 Assignment 1 (Group 6)

Demonstrates a log injection vulnerability (CWE-117), an exploit, and a mitigation.

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

**Exploit** — with the vulnerable app running, run the exploit script in a second terminal. It submits a crafted username containing CRLF characters, forging fake entries in `app.log`.

```bash
cd exploit && python3 exploit.py
```

**Mitigated app** → http://127.0.0.1:5000 (stop the vulnerable app first)

```bash
cd mitigated && python3 app.py
```

Re-run the exploit against it — the crafted input is rejected/sanitized, so no forged lines appear in the log.

## Login

```
admin / admin
```

## What's here

- `vulnerable/` — app that writes the raw username into `app.log`
- `exploit/`    — script that injects forged log lines
- `mitigated/`  — fixed version (input validation + CRLF sanitization)

Each app writes its log to `app.log` in its own folder.

See the report for the full analysis.