# loan_amount = float(input("Enter the loan amount: $"))
# duration = int(input("Enter the loan duration (in months): "))
# annual_interest_rate = float(
#     input("Enter the annual interest rate (in percentage): "))
# partner_rate = float(
#     input("Enter the partner's commission rate (in percentage): "))

loan_amount = 10000
duration = 48
annual_interest_rate = 11.90
partner_rate = 7.50

# Calculate the partner's commission
commission = loan_amount * (partner_rate / 100)

print(commission)

# Calculate the monthly payment
monthly_interest_rate = annual_interest_rate / 12 / 100
monthly_payment = loan_amount * monthly_interest_rate * \
    (1 + monthly_interest_rate) ** duration / \
    ((1 + monthly_interest_rate) ** duration - 1)

print(monthly_interest_rate)
print(monthly_payment)

monthly_payment_after_commission = monthly_payment - commission / duration

print(monthly_payment_after_commission)

# Estimate the remaining rate after commissions using an iterative approach
remaining_balance = loan_amount  # Initializing the remaining balance
annual_rate_guess = 0.25  # Initial guess for the annual rate

while remaining_balance > 0.10:
    remaining_balance = loan_amount
    annual_rate_guess -= 0.0001
    monthly_rate_guess = (1 + annual_rate_guess) ** (1 / 12) - 1

    print(annual_rate_guess * 100)
    print(monthly_rate_guess * 100)

    for _ in range(duration):
        remaining_balance *= (1 + monthly_rate_guess)
        remaining_balance -= monthly_payment_after_commission

        print(remaining_balance)

print("Annual Rate (after deducting partner's commission): {:.2f}%".format(
    annual_rate_guess * 100))
