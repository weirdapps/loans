# Loans

[![CI](https://github.com/weirdapps/loans/actions/workflows/ci.yml/badge.svg)](https://github.com/weirdapps/loans/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-3776AB.svg)](https://www.python.org/downloads/)

Auto-loan effective-rate calculator that accounts for the partner's one-off commission. Compares lender quotes where the headline interest rate hides a large upfront fee that materially changes the effective cost.

## The Problem

Greek auto-loan offers are commonly quoted as "X% interest" but bake in a one-off broker commission of 1-3% of principal that's amortised over the loan term. A loan advertised at 8.5% with a 2% commission actually costs **9.4% effective** — this tool surfaces the real number.

## Quick Start

### Web App

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000). Enter loan amount, duration (months), interest rate (%), and commission rate (%) — the page shows the effective annual rate and the post-commission remaining rate.

### CLI

```bash
python cli.py --amount 25000 --months 60 --rate 8.5 --commission 2.0
```

```text
Effective Annual Rate: 9.42%
Post-Commission Rate:  8.89%
Monthly Payment:       €512.35
Total Commission:      €500.00
```

## How It Works

1. **Commission deduction** — the broker's percentage is subtracted from the disbursed principal upfront
2. **Monthly payment** — computed on the full loan amount at the headline rate (you still repay the full principal)
3. **Effective rate** — derived via Newton-Raphson iteration: the true annual rate that equates the reduced disbursement to the payment stream

## Project Structure

```text
app.py            Flask web UI
cli.py            Command-line interface
templates/        Jinja2 templates
static/           CSS
tests/            pytest suite
requirements.txt  Flask
```

## Development

```bash
pip install ruff pytest pytest-cov
ruff check .            # lint
pytest                  # test
```

## License

[MIT](LICENSE)
