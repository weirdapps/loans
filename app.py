from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def calculate():
    loan_amount = float(request.form['loan_amount'])
    duration = int(request.form['duration'])
    annual_interest_rate = float(request.form['annual_interest_rate'])
    partner_rate = float(request.form['partner_commission_rate'])

    # Calculate the partner's commission
    commission = loan_amount * (partner_rate / 100)

    # Calculate the monthly payment
    monthly_interest_rate = annual_interest_rate / 12 / 100
    monthly_payment = loan_amount * monthly_interest_rate * \
        (1 + monthly_interest_rate) ** duration / \
        ((1 + monthly_interest_rate) ** duration - 1)

    monthly_payment_after_commission = monthly_payment - commission / duration

    # Estimate the remaining rate after commissions using an iterative approach
    remaining_balance = loan_amount  # Initializing the remaining balance
    annual_rate_guess = 0.25  # Initial guess for the annual rate

    while remaining_balance > 0.10:
        remaining_balance = loan_amount
        annual_rate_guess -= 0.0001
        monthly_rate_guess = (1 + annual_rate_guess) ** (1 / 12) - 1

        for _ in range(duration):
            remaining_balance *= (1 + monthly_rate_guess)
            remaining_balance -= monthly_payment_after_commission

    annual_rate = annual_rate_guess * 100

    return render_template('result.html', annual_rate=annual_rate)


if __name__ == '__main__':
    app.run(debug=True)
