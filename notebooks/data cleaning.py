import pandas as pd

import numpy as np

# file load

customers = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/customers_cleaned.csv")
branches  = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/branches_cleaned.csv")
accounts = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/accounts_cleaned.csv")
loans = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/loans_cleaned.csv")
transactions = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/transactions_cleaned.csv")
loan_payments = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/loan_payments_cleaned.csv")
# ============================================================
# 1. JOIN TABLES TOGETHER
# ============================================================ 
print("*" * 50)
print("1 join table")
print("*" * 50)

# Loans + Customers + Branches
loan_master = loans.merge(customers, on="customer_id", how="left") \
                    .merge(branches, on="branch_id", how="left")

# fix duplicate "city" column name from the two merges
loan_master = loan_master.rename(columns={
    "city_x": "customer_city",
    "city_y": "branch_city"
})

print("loan_master_shape", loan_master.shape)
print(loan_master.columns.tolist())

# Accounts + Customers + Branches
account_master = accounts.merge(customers, on="customer_id", how="left") \
                          .merge(branches, on="branch_id", how="left")

account_master = account_master.rename(columns={
    "city_x": "customer_city",
    "city_y": "branch_city"
})

print("account_master_shape", account_master.shape)

# Loan payments + Loans (this is the table with due_amount, paid_amount, days_late, payment_status)
loan_payment_master = loan_payments.merge(
    loans[["loan_id", "customer_id", "loan_type", "loan_amount"]],
    on="loan_id", how="left"
)

print("loan_payment_master_shape", loan_payment_master.shape)


# ============================================================
# 2. DERIVED METRICS
# ============================================================
print("=" * 50)
print("2 derived metrics")
print("=" * 50)

# Loan-to-income ratio
loan_master["loan_to_income_ratio"] = (loan_master["loan_amount"] / loan_master["annual_income"]).round(2)

# Age group buckets
loan_master["age_group"] = pd.cut(
    loan_master["age"],
    bins=[0, 25, 35, 45, 55, 100],
    labels=["18-25", "26-35", "36-45", "46-55", "56+"]
)

# Income bracket
loan_master["income_bracket"] = pd.cut(
    loan_master["annual_income"],
    bins=[0, 30000, 60000, 100000, np.inf],
    labels=["Low", "Mid", "High", "Very High"]
)

# Estimated EMI (simple approximation)
loan_master["estimated_emi"] = (loan_master["loan_amount"] / loan_master["tenure_months"]).round(2)

# Confirm the new columns actually exist before using them
print(loan_master.columns.tolist())

print("\nSample derived columns on loan_master:")
print(loan_master[["loan_id", "loan_amount", "annual_income", "loan_to_income_ratio",
                    "age_group", "income_bracket", "estimated_emi"]].head())

# Payment summary per loan (built from loan_payment_master, NOT loan_master)
payment_summary = loan_payment_master.groupby("loan_id").agg(
    total_due=("due_amount", "sum"),
    total_paid=("paid_amount", "sum"),
    avg_days_late=("days_late", "mean"),
    missed_payments=("payment_status", lambda x: (x == "Missed").sum())
).reset_index()

payment_summary["repayment_ratio"] = (payment_summary["total_paid"] / payment_summary["total_due"]).round(2)

print("\nSample payment_summary:")
print(payment_summary.head())


# ============================================================
# 3. GROUPBY ANALYSIS
# ============================================================
print("=" * 50)
print("3 groupby analysis")
print("=" * 50)

avg_loan_by_type = loan_master.groupby("loan_type")["loan_amount"].mean().round(2)
print("\nAverage loan amount by loan type:")
print(avg_loan_by_type)

default_by_branch_type = loan_master.groupby("branch_type")["default_flag"].mean() * 100
print("\nDefault rate by branch type (%):")
print(default_by_branch_type.round(2))

default_by_age = loan_master.groupby("age_group", observed=True)["default_flag"].mean() * 100
print("\nDefault rate by age group (%):")
print(default_by_age.round(2))

segment_lti = loan_master.groupby("customer_segment")["loan_to_income_ratio"].mean().round(2) \
    if "customer_segment" in loan_master.columns else "column not found - check customers.csv"
print("\nAverage loan-to-income ratio by customer segment:")
print(segment_lti)

txn_by_channel = transactions.groupby("channel")["amount"].agg(["count", "sum", "mean"]).round(2)
print("\nTransaction summary by channel:")
print(txn_by_channel)


# ============================================================
# 4. PIVOT TABLES
# ============================================================
print("=" * 50)
print("4 pivot tables")
print("=" * 50)

pivot1 = loan_master.pivot_table(
    values="loan_amount",
    index="loan_type",
    columns="branch_type",
    aggfunc="mean"
).round(2)
print("\nAvg loan amount: loan_type x branch_type")
print(pivot1)

pivot2 = loan_master.pivot_table(
    values="loan_id",
    index="loan_status",
    columns="loan_type",
    aggfunc="count",
    fill_value=0
)
print("\nLoan count: loan_status x loan_type")
print(pivot2)


# ============================================================
# 5. SAVE ANALYSIS-READY DATASETS
# ============================================================
loan_master.to_csv("loan_master_analysis.csv", index=False)
account_master.to_csv("account_master_analysis.csv", index=False)
payment_summary.to_csv("payment_summary_analysis.csv", index=False)

print("=" * 50)
print("Saved: loan_master_analysis.csv, account_master_analysis.csv, payment_summary_analysis.csv")
print("PHASE 4 COMPLETE")
print("=" * 50)
