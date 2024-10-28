def calculate_loan_eligibility(age, monthly_income, employment_status, years_employed):
    # Base calculations
    max_age_at_end = 75
    max_duration = min(75 - age, 30)
    
    # Basic eligibility checks
    if age + max_duration > max_age_at_end:
        return {
            'eligible': False,
            'reason': 'Age limit exceeded',
            'max_duration': max_duration
        }
    
    if employment_status == 'SANS_EMPLOI':
        return {
            'eligible': False,
            'reason': 'Employment required'
        }
    
    # Calculate maximum loan amount (40% of monthly income)
    monthly_capacity = monthly_income * 0.4
    
    # Determine interest rate based on income
    interest_rate = 0.01 if monthly_income < 100000 else 0.03
    
    # Calculate maximum loan amount based on capacity and duration
    max_loan = calculate_max_loan_amount(monthly_capacity, interest_rate, max_duration)
    
    return {
        'eligible': True,
        'max_loan_amount': max_loan,
        'max_duration': max_duration,
        'interest_rate': interest_rate,
        'monthly_capacity': monthly_capacity
    }

def calculate_monthly_payment(loan_amount, duration, monthly_income):
    # Validate duration
    if duration > 30:
        raise ValueError('Maximum loan duration is 30 years')
    
    # Determine interest rate
    interest_rate = 0.01 if monthly_income < 100000 else 0.03
    
    # Monthly interest rate
    monthly_rate = interest_rate / 12
    
    # Total number of payments
    n_payments = duration * 12
    
    # Monthly payment calculation using the loan amortization formula
    if monthly_rate == 0:
        monthly_payment = loan_amount / n_payments
    else:
        monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**n_payments) / ((1 + monthly_rate)**n_payments - 1)
    
    return round(monthly_payment, 2)

def calculate_max_loan_amount(monthly_capacity, interest_rate, duration):
    # Monthly interest rate
    monthly_rate = interest_rate / 12
    
    # Total number of payments
    n_payments = duration * 12
    
    # Maximum loan amount calculation (inverse of monthly payment formula)
    if monthly_rate == 0:
        max_loan = monthly_capacity * n_payments
    else:
        max_loan = monthly_capacity * ((1 - (1 + monthly_rate)**-n_payments) / monthly_rate)
    
    return round(max_loan, 2)