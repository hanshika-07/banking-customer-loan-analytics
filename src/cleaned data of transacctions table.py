import pandas as pd
import numpy as np

transactions = pd.read_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\transactions.csv")
print(transactions.shape)
print(transactions.head())
print(transactions.duplicated().sum())
print(transactions.isnull().sum())
print(transactions.dtypes)

transactions = transactions.drop_duplicates()

print(transactions["transaction_type"].value_counts())
transactions["transaction_type"] = transactions["transaction_type"].fillna(transactions["transaction_type"].mode()[0])
print(transactions.isnull().sum())

transactions["transaction_date"] = pd.to_datetime(transactions["transaction_date"], errors='coerce')
print(transactions.dtypes)

transactions.to_csv(r"c:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\cleaned\transactions_cleaned.csv", index=False)
print("Cleaned transactions shape:", transactions.shape)