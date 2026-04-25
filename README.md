# loans

Auto-loan effective-rate calculator that accounts for the partner's one-off commission. Useful when comparing lender quotes where the headline interest rate hides a large upfront fee that materially changes the effective cost.

## Web app

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Then open http://localhost:5000. Enter loan amount, duration (months), interest rate (%), and one-off commission rate (%); the page shows the effective annual rate and the post-commission remaining rate.

## CLI

```bash
python cli.py --amount 25000 --months 60 --rate 8.5 --commission 2.0
```

## Layout

```
app.py            # Flask web entrypoint
cli.py            # command-line entrypoint
templates/        # Jinja2 templates for the web UI
static/           # CSS/JS
requirements.txt  # Flask + numpy
```

## Why this exists

Greek auto-loan offers are commonly quoted as "X% interest" but bake in a one-off broker commission of 1-3% of principal that's amortised over the loan term — making the true effective rate noticeably higher than the headline. This tool surfaces the real number.
