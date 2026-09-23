import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)
Faker.seed(42)

# Load the files loans depends on
customers = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\customers.csv")
branches = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\branches.csv")

n_loans = 6000

loans = pd.DataFrame({
    "loan_id": [f"LN{i:05d}" for i in range(n_loans)],
    "customer_id": np.random.choice(customers["customer_id"], n_loans),
    "branch_id": np.random.choice(branches["branch_id"], n_loans),
    "loan_type": np.random.choice(["Personal", "Home", "Vehicle", "Education"], n_loans),
    "application_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(n_loans)],
    "loan_amount": np.random.uniform(10000, 500000, n_loans).round(2),
    "interest_rate": np.random.uniform(6, 18, n_loans).round(2),
    "tenure_months": np.random.choice([12, 24, 36, 60, 120], n_loans),
    "credit_score": np.random.randint(300, 900, n_loans),
    "loan_status": np.random.choice(["Approved", "Rejected", "Active", "Closed", "Defaulted"], n_loans),
})

# derived column: 1 if defaulted, else 0
loans["default_flag"] = (loans["loan_status"] == "Defaulted").astype(int)

loans.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\loans.csv", index=False)

print(loans.head())
print("loans.csv created!")




# Negative loan amounts (data entry error)
neg_amt_idx = loans.sample(frac=0.01, random_state=1).index
loans.loc[neg_amt_idx, "loan_amount"] *= -1

# Broken foreign key
bad_cust_idx = loans.sample(frac=0.02, random_state=2).index
loans.loc[bad_cust_idx, "customer_id"] = "CUST99999"

# Missing interest_rate
missing_rate_idx = loans.sample(frac=0.03, random_state=3).index
loans.loc[missing_rate_idx, "interest_rate"] = np.nan

# Duplicate row
loans = pd.concat([loans, loans.iloc[[0]]], ignore_index=True)

loans = loans.sample(frac=1, random_state=4).reset_index(drop=True)

loans.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\loans.csv", index=False)
print(loans.head())
print("loans.csv created with intentional messiness!")
print("Shape:", loans.shape)