# Sample MVP Python App

A tiny MVP for testing AI code review agents. This is intentionally imperfect and contains bugs, security issues, and performance problems.

## What it does
- Simple "notes" app with login, search, and reporting.
- Uses SQLite for storage.
- Minimal HTML output for quick testing.

## Setup
1. Create a virtual environment.
2. Install deps: `pip install -r requirements.txt`
3. Initialize DB: `python app.py --init-db`
4. Run: `python app.py`

## Endpoints
- `/` list notes
- `/login` login (POST)
- `/notes` create note (POST)
- `/search` search notes (GET)
- `/report` generate report (GET)

## Known intentional issues
- SQL injection risk
- Hard-coded secrets
- Missing auth checks
- Insecure password handling
- Path traversal risk
- Inefficient loops and per-request DB work
- No input validation

Use this only for testing review agents.
