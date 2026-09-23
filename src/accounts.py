import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)
Faker.seed(42)

# Load the files accounts depends on+

customers = pd.read_csv(r"C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\customers.csv")
branches = pd.read_csv(r"C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\branches.csv")

n_accounts = 12000

accounts = pd.DataFrame({
    "account_id": [f"ACC{i:05d}" for i in range(n_accounts)],
    "customer_id": np.random.choice(customers["customer_id"], n_accounts),
    "branch_id": np.random.choice(branches["branch_id"], n_accounts),
    "account_type": np.random.choice(["Savings", "Current", "Salary"], n_accounts),
    "account_open_date": [fake.date_between(start_date="-3y", end_date="today") for _ in range(n_accounts)],
    "initial_balance": np.random.uniform(500, 100000, n_accounts).round(2),
    "account_status": np.random.choice(["Active", "Dormant", "Closed"], n_accounts),
})


print(accounts.head())

# Broken foreign key: some customer_id values don't exist
bad_cust_idx = accounts.sample(frac=0.02, random_state=1).index
accounts.loc[bad_cust_idx, "customer_id"] = "CUST99999"

# Negative balances (data entry errors)
neg_bal_idx = accounts.sample(frac=0.01, random_state=2).index
accounts.loc[neg_bal_idx, "initial_balance"] *= -1

# Missing account_status
missing_status_idx = accounts.sample(frac=0.02, random_state=3).index
accounts.loc[missing_status_idx, "account_status"] = np.nan

# Duplicate rows
accounts = pd.concat([accounts, accounts.iloc[[0, 1]]], ignore_index=True)

accounts = accounts.sample(frac=1, random_state=4).reset_index(drop=True)

accounts.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\accounts.csv", index=False)
print(accounts.head())
print("accounts.csv created with intentional messiness!")
print("Shape:", accounts.shape)