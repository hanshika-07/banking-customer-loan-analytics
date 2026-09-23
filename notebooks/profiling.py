import pandas as pd

files = {
    "customers": "C:\\Users\\Darshan Soni\\pythonproject\\customers.csv",
    "branches": "C:\\Users\\Darshan Soni\\pythonproject\\branches.csv",
    "accounts": "C:\\Users\\Darshan Soni\\pythonproject\\accounts.csv",
    "loans": "C:\\Users\\Darshan Soni\\pythonproject\\loans.csv",
    "transactions": "C:\\Users\\Darshan Soni\\pythonproject\\transactions.csv",
    "loan_payments": "C:\\Users\\Darshan Soni\\pythonproject\\loan_payments.csv",
}

data = {name: pd.read_csv(path) for name, path in files.items()}

for name, df in data.items():
    print(f"\n========== {name} ==========")
    print("Shape (rows, cols):", df.shape)
    print("\nData types:\n", df.dtypes)
    print("\nMissing values:\n", df.isnull().sum())
    print("\nDuplicate rows:", df.duplicated().sum())
    print("\nBasic stats:\n", df.describe(include="all"))