import pandas as pd
import numpy as np
accounts = pd.read_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\accounts.csv")


print(accounts.shape)
print(accounts.head())
print(accounts.duplicated().sum())
print(accounts.isnull().sum())
print(accounts.dtypes)

accounts = accounts.drop_duplicates()
accounts["account_status"] = accounts["account_status"].fillna(accounts["account_status"].mode()[0])
print(accounts["account_status"].value_counts())

accounts.to_csv(r"c:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\cleaned\accounts_cleaned.csv", index=False)
print("cleaned shape:", accounts.shape)