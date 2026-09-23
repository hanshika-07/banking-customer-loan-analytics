import pandas as pd
import numpy as np

loans = pd.read_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\loans.csv")
print(loans.shape)
print(loans.head())
print(loans.duplicated().sum())
print(loans.isnull().sum())
print(loans.dtypes)

loans = loans.drop_duplicates()
loans["interest_rate"] = loans["interest_rate"].fillna(loans["interest_rate"].median())
print(loans.isnull().sum())
loans.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\cleaned\loans_cleaned.csv", index=False)
print("cleaned shape:", loans.shape)