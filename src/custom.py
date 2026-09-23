import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)      # fixed seed = reproducible data
Faker.seed(42)

n_customers = 10000

customers = pd.DataFrame({
    "customer_id": [f"CUST{i:05d}" for i in range(n_customers)],
    "customer_name": [fake.name() for _ in range(n_customers)],
    "age": np.random.randint(18, 75, n_customers),
    "gender": np.random.choice(["Male", "Female"], n_customers),
    "annual_income": np.random.normal(50000, 15000, n_customers).round(2),
    "city": [fake.city() for _ in range(n_customers)],
})

customers.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\customers.csv", index=False)
print(customers.head())
print("customers.csv created!")


import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()
np.random.seed(42)      # fixed seed = reproducible data
Faker.seed(42)

n_customers = 10000

customers = pd.DataFrame({
    "customer_id": [f"CUST{i:05d}" for i in range(n_customers)],
    "customer_name": [fake.name() for _ in range(n_customers)],
    "age": np.random.randint(18, 75, n_customers),
    "gender": np.random.choice(["Male", "Female"], n_customers),
    "annual_income": np.random.normal(50000, 15000, n_customers).round(2),
    "city": [fake.city() for _ in range(n_customers)],
})

# ---------- INTRODUCE MESSINESS ----------

# 1. Missing values in annual_income (~3%)
missing_income_mask = np.random.random(n_customers) < 0.03
customers.loc[missing_income_mask, "annual_income"] = np.nan

# 2. Missing values in city (~2%)
missing_city_mask = np.random.random(n_customers) < 0.02
customers.loc[missing_city_mask, "city"] = np.nan

# 3. Inconsistent gender spelling (mix in "M", "F", "male", "female")
customers.loc[::400, "gender"] = "M"
customers.loc[::550, "gender"] = "F"
customers.loc[::700, "gender"] = "male"
customers.loc[::900, "gender"] = "female"

# 4. Unrealistic ages (a few negative or absurdly high values)
bad_age_idx = customers.sample(10, random_state=1).index
customers.loc[bad_age_idx[:5], "age"] = -5
customers.loc[bad_age_idx[5:], "age"] = 150

# 5. Outliers in annual_income (a few extreme values)
outlier_income_idx = customers.sample(8, random_state=2).index
customers.loc[outlier_income_idx, "annual_income"] = 5_000_000

# 6. Duplicate rows (exact copies)
duplicate_rows = customers.sample(15, random_state=3)
customers = pd.concat([customers, duplicate_rows], ignore_index=True)

# 7. Duplicate customer_id but different data (data entry error)
dup_id_row = customers.iloc[[0]].copy()
dup_id_row["age"] = 40
customers = pd.concat([customers, dup_id_row], ignore_index=True)

# 8. Extra whitespace / inconsistent casing in city names
whitespace_idx = customers.sample(10, random_state=4).index
customers.loc[whitespace_idx, "city"] = customers.loc[whitespace_idx, "city"].astype(str) + "   "

# shuffle so messiness isn't clustered at predictable spots
customers = customers.sample(frac=1, random_state=5).reset_index(drop=True)

customers.to_csv(r"C:\Users\hanshika\Desktop\banking-customer-loan-analytics\data\raw\customers.csv", index=False)
print(customers.head())
print("customers.csv created with intentional messiness!")
print("Shape:", customers.shape)