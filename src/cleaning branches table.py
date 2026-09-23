import pandas as pd
import numpy as np

branches = pd.read_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\branches.csv")

print(branches.shape)
print(branches.isnull().sum())
print(branches.dtypes)
print(branches.head())


branches = branches.drop_duplicates()
branches = branches.drop_duplicates()


branches['branch_type'] = branches["branch_type"].fillna(branches["branch_type"].mode()[0])
print(branches.isnull().sum())
branches["opening_date"] = pd.to_datetime(branches["opening_date"], errors='coerce')

print(branches.head())

branches.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\cleaned\branches_cleaned.csv", index=False)
print("Cleaned shape:", branches.shape)