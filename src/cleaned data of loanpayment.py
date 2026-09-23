import pandas as pd 
import numpy as mpp

loanpayment = pd.read_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\loan_payments.csv")

print(loanpayment.head())
print(loanpayment.shape)
print(loanpayment.duplicated().sum())
print(loanpayment.isnull().sum())
print(loanpayment.dtypes)

loanpayment = loanpayment.drop_duplicates()
loanpayment["payment_date"] = pd.to_datetime(loanpayment["payment_date"], errors='coerce')

loanpayment["paid_amount"] = loanpayment["paid_amount"].fillna(loanpayment["paid_amount"].median())
loanpayment.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\cleaned\loan_payments_cleaned.csv", index=False)
print("cleaned shape:", loanpayment.shape)