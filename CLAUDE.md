# loans

Greek auto-loan effective-rate calculator. Surfaces the true annual cost of loans where a one-off broker commission (1–3% of principal) is baked in. Uses Newton-Raphson iterative descent to find the real effective rate after commission.

## Tech Stack

- Python 3.11+ (CI uses 3.12)
- Flask 3.x — web UI, Jinja2 templates
- Only runtime dependency: `flask`
- Dev: `ruff`, `pytest`, `pytest-cov`
- Lock file managed via `uv`, installed via `pip`

## Install

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-lock.txt
```

## Run

```bash
python app.py              # web UI → http://localhost:5000
python cli.py              # interactive CLI (prompts for input)
FLASK_DEBUG=true python app.py
```

## Test / Lint

```bash
pytest                     # full suite + coverage (term-missing + coverage.xml)
ruff check .               # lint
```

## Code Organization

Flat layout — no packages:

| File | Purpose |
|------|---------|
| `app.py` | Flask app — single `GET /` + `POST /calculate` route, Newton-Raphson iteration, security headers middleware |
| `cli.py` | Standalone script — interactive `input()` prompts |
| `templates/` | `index.html` (form), `result.html` (output) |
| `static/style.css` | Styles |
| `tests/conftest.py` | Flask test fixtures |
| `tests/test_app.py` | `TestAppCreation`, `TestLoanCalculation`, `TestInputValidation` |

## Key Conventions

- `MAX_ITERATIONS = 1_000_000` guards the convergence loop in both `app.py` and `cli.py`
- Security headers on every response (`X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`)
- `ruff` line length 100, target py311
- Pre-commit hooks: trailing whitespace, YAML/JSON check, ruff + ruff-format, mypy, gitleaks, markdownlint

## CI

- **ci.yml** — push/PR to master: syntax compile, install from lock, lint (ruff), pytest (Node 22)
- **sonarcloud.yml** — push to master + human PRs: pytest with coverage → SonarCloud (skips Dependabot PRs)
- **deps-refresh.yml** — monthly (9th): uv lockfile refresh → opens PR `deps/monthly-refresh`
- **codeql.yml** — CodeQL security analysis
- **dependabot-auto-merge.yml** — auto-merge Dependabot PRs
