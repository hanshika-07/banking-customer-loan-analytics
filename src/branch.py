import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)
Faker.seed(42)

n_branches = 50

branches = pd.DataFrame({
    "branch_id": [f"BR{i:03d}" for i in range(n_branches)],
    "branch_name": [f"{fake.city()} Branch" for _ in range(n_branches)],
    "city": [fake.city() for _ in range(n_branches)],
    "state": [fake.state() for _ in range(n_branches)],
    "branch_type": np.random.choice(["Urban", "Semi-Urban", "Rural"], n_branches),
    "opening_date": [fake.date_between(start_date="-10y", end_date="-1y") for _ in range(n_branches)],
})

branches.to_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\raw\\branches.csv", index=False)

print(branches.head())
print("branches.csv created!")

# Missing branch_type (~5%)
missing_idx = branches.sample(3, random_state=1).index
branches.loc[missing_idx, "branch_type"] = np.nan

# Inconsistent state naming (abbreviate a few)
abbrev_idx = branches.sample(5, random_state=2).index
branches.loc[abbrev_idx, "state"] = branches.loc[abbrev_idx, "state"].str[:2].str.upper()

# Duplicate rows
branches = pd.concat([branches, branches.iloc[[0, 5]]], ignore_index=True)

branches = branches.sample(frac=1, random_state=3).reset_index(drop=True)

branches.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\branches.csv", index=False)
print(branches.head())
print("branches.csv created with intentional messiness!")
print("Shape:", branches.shape)