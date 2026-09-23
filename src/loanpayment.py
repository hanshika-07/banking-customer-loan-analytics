import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)
Faker.seed(42)

# Load the file loan_payments depends on
loans = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\loans.csv")

n_payments = 46000

loan_payments = pd.DataFrame({
    "payment_id": [f"PAY{i:06d}" for i in range(n_payments)],
    "loan_id": np.random.choice(loans["loan_id"], n_payments),
    "payment_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(n_payments)],
    "due_amount": np.random.uniform(1000, 20000, n_payments).round(2),
    "paid_amount": np.random.uniform(1000, 20000, n_payments).round(2),
    "days_late": np.random.choice([0, 0, 0, 3, 10, 30], n_payments),
})

# derived column: payment status based on days_late
loan_payments["payment_status"] = np.where(
    loan_payments["days_late"] == 0, "On Time",
    np.where(loan_payments["days_late"] < 15, "Late", "Missed")
)

loan_payments.to_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\loan_payments.csv", index=False)

print(loan_payments.head())
print("loan_payments.csv created!")


# Broken foreign key
bad_loan_idx = loan_payments.sample(frac=0.02, random_state=1).index
loan_payments.loc[bad_loan_idx, "loan_id"] = "LN99999"

# Missing paid_amount
missing_paid_idx = loan_payments.sample(frac=0.03, random_state=2).index
loan_payments.loc[missing_paid_idx, "paid_amount"] = np.nan

# Negative days_late
neg_days_idx = loan_payments.sample(frac=0.01, random_state=3).index
loan_payments.loc[neg_days_idx, "days_late"] *= -1

# Duplicate row
loan_payments = pd.concat([loan_payments, loan_payments.iloc[[0]]], ignore_index=True)

loan_payments = loan_payments.sample(frac=1, random_state=4).reset_index(drop=True)

loan_payments.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\loan_payments.csv", index=False)
print(loan_payments.head())
print("loan_payments.csv created with intentional messiness!")
print("Shape:", loan_payments.shape)