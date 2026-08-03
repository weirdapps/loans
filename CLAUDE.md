# loans

Greek auto-loan effective-rate calculator. Surfaces the true annual cost of loans where a one-off broker commission (1 to 3 percent of principal) is baked in. Uses a naive linear descent scan: starting from an initial guess of 0.25, it decrements the guess by 0.0001 each pass and simulates the full monthly amortisation schedule until the residual balance drops to 0.10 or below.

## Tech Stack

- Python 3.11+ (CI uses 3.12; SonarCloud uses 3.11)
- Flask 3.1+ for the web UI, Jinja2 templates
- Only runtime dependency: `flask`
- Dev: `ruff`, `pytest`, `pytest-cov`
- Dependency management: `uv` (lockfile `uv.lock` committed; installed via `uv sync --frozen`)

## Install

```bash
uv sync --frozen
```

Creates `.venv/` and installs the pinned versions from `uv.lock` without resolving.

## Run

```bash
uv run python app.py       # web UI at http://localhost:5000
uv run python cli.py       # interactive CLI (prompts for input)
FLASK_DEBUG=true uv run python app.py
```

## Test / Lint

```bash
uv run pytest              # full suite + coverage (term-missing + coverage.xml)
uv run ruff check .        # lint
```

## Code Organization

Flat layout, not an installed package (`[tool.uv] package = false` in `pyproject.toml`):

| File | Purpose |
|------|---------|
| `app.py` | Flask app: `GET /` + `POST /calculate`, linear-descent rate solver, security headers middleware |
| `cli.py` | Standalone script: interactive `input()` prompts, same math as `app.py` |
| `templates/` | `index.html` (form), `result.html` (output) |
| `static/style.css` | Styles |
| `tests/conftest.py` | Flask test fixtures (`app`, `client`) |
| `tests/test_app.py` | `TestAppCreation`, `TestLoanCalculation`, `TestInputValidation` |

## Key Conventions

- `MAX_ITERATIONS = 1_000_000` guards the convergence loop in both `app.py` and `cli.py`; on breach, `app.py` re-renders the form and `cli.py` exits with status 1
- `app.py` passes an `error` string to `index.html` on every validation and non-convergence failure, but the template never renders it, so the user sees a blank form and no reason. Fixing this means editing `templates/index.html`, not `app.py`
- The solver is a naive linear decrement (`annual_rate_guess -= 0.0001`), not Newton-Raphson; step size is fixed at 0.0001 and the initial guess is 0.25
- The headline monthly rate uses simple division (`annual / 12 / 100`); the solved rate uses compound monthly conversion (`(1 + guess) ** (1/12) - 1`), so the two are not directly comparable even at zero commission
- Security headers on every response (`X-Content-Type-Options`, `X-Frame-Options`, `X-XSS-Protection`, `Referrer-Policy`)
- `ruff` line length 100, target py311
- Pre-commit hooks: trailing whitespace, YAML/JSON check, ruff + ruff-format, mypy, gitleaks, yamllint (workflows only), markdownlint

## CI

Five workflows under `.github/workflows/`:

- **ci.yml**: push/PR to `master`. `uv sync --frozen`, `py_compile app.py cli.py`, `ruff check`, `pytest`. Python 3.12.
- **sonarcloud.yml**: push to `main`/`master` and human-authored PRs (skips Dependabot). `uv sync --frozen`, `pytest` with coverage, SonarCloud scan. Python 3.11.
- **deps-refresh.yml**: monthly cron `41 4 9 * *` (day 9 at 04:41 UTC) + manual dispatch. `uv lock --upgrade`, `uv sync --frozen`, `pytest`, opens PR `deps/monthly-refresh`.
- **codeql.yml**: CodeQL security analysis.
- **dependabot-auto-merge.yml**: thin caller of `weirdapps/shared-workflows/.github/workflows/dependabot-auto-merge.yml@main` (passes no inputs, so the reusable's defaults apply). Auto-merges patch, minor, and grouped updates; standalone majors stay open. Change the merge logic in `shared-workflows`, not here.

Dependabot (`.github/dependabot.yml`) watches both `github-actions` and the `uv` ecosystem weekly, with minor and patch updates grouped.
