import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)
Faker.seed(42)

# Load the file transactions depends on
accounts = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\accounts.csv")

n_transactions = 140000

transactions = pd.DataFrame({
    "transaction_id": [f"TXN{i:06d}" for i in range(n_transactions)],
    "account_id": np.random.choice(accounts["account_id"], n_transactions),
    "transaction_date": [fake.date_between(start_date="-2y", end_date="today") for _ in range(n_transactions)],
    "transaction_type": np.random.choice(["Deposit", "Withdrawal", "Transfer", "Payment"], n_transactions),
    "amount": np.random.uniform(100, 50000, n_transactions).round(2),
    "channel": np.random.choice(["Branch", "ATM", "Online", "Mobile"], n_transactions),
})

transactions.to_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\transactions.csv", index=False)

print(transactions.head())
print("transactions.csv created!")


# Inconsistent category spelling
transactions.loc[::300, "channel"] = "online"

# Negative amounts
neg_idx = transactions.sample(frac=0.01, random_state=1).index
transactions.loc[neg_idx, "amount"] *= -1

# Broken foreign key
bad_acc_idx = transactions.sample(frac=0.02, random_state=2).index
transactions.loc[bad_acc_idx, "account_id"] = "ACC99999"

# Missing transaction_type
missing_type_idx = transactions.sample(frac=0.02, random_state=3).index
transactions.loc[missing_type_idx, "transaction_type"] = np.nan

# Duplicate rows
transactions = pd.concat([transactions, transactions.iloc[[0, 1]]], ignore_index=True)

transactions = transactions.sample(frac=1, random_state=4).reset_index(drop=True)

transactions.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\transactions.csv", index=False)
print(transactions.head())
print("transactions.csv created with intentional messiness!")
print("Shape:", transactions.shape)