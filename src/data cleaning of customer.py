import pandas as pd
import numpy as np

customers = pd.read_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\customers.csv")

# 1. Check what you're working with first
print(customers.shape)
print(customers.dtypes)
print(customers.isnull().sum())

# 2. Standardize gender values (fix inconsistent spelling)
customers["gender"] = customers["gender"].replace({
    "M": "Male",
    "m": "Male",
    "F": "Female",
    "female": "Female"
})

# 3. Fill missing annual_income with median (income is usually skewed, not symmetric)
customers["annual_income"] = customers["annual_income"].abs()
customers["annual_income"] = customers["annual_income"].fillna(
    customers["annual_income"].median()
)

# 4. Handle unrealistic ages (negative or too high)
customers = customers[(customers["age"] >= 18) & (customers["age"] <= 100)]

# 5. Clean up city text (remove extra spaces, fix casing)
customers["city"] = customers["city"].str.strip().str.title()

# 6. Remove duplicate rows
customers = customers.drop_duplicates()

# 7. Remove duplicate customer_id specifically (shouldn't have 2 rows with same ID)
customers = customers.drop_duplicates(subset="customer_id")

customers.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\cleaned\customers_cleaned.csv", index=False)
print("Cleaned shape:", customers.shape)
