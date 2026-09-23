import pandas as pd
import numpy as np
# pyrefly: ignore [missing-import]
import matplotlib.pyplot as plt

# ---------- LOAD DATA ----------
customers = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/customers_cleaned.csv")
branches  = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/branches_cleaned.csv")
accounts = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/accounts_cleaned.csv")
loans = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/loans_cleaned.csv")
transactions = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/transactions_cleaned.csv")
loan_payments = pd.read_csv(r"C:/Users/hanshika/Desktop/banking-customer-loan-analytics/data/cleaned/loan_payments_cleaned.csv")

plt.style.use("seaborn-v0_8-darkgrid")  # clean look; falls back gracefully if unavailable


# ============================================================
# CHART 1: Income Distribution (Histogram)
# ============================================================
plt.figure(figsize=(8, 5))
plt.hist(customers["annual_income"].dropna(), bins=40, color="steelblue", edgecolor="black")
plt.title("Distribution of Customer Annual Income")
plt.xlabel("Annual Income")
plt.ylabel("Number of Customers")
plt.tight_layout()
plt.savefig("chart1_income_distribution.png")
plt.close()
print("Chart 1 saved: Income distribution — shows whether most customers cluster around "
      "a typical income or if a few high earners skew the average upward.")


# ============================================================
# CHART 2: Loan Amount Distribution (Histogram)
# ============================================================
plt.figure(figsize=(8, 5))
plt.hist(loans["loan_amount"].dropna(), bins=40, color="darkorange", edgecolor="black")
plt.title("Distribution of Loan Amounts")
plt.xlabel("Loan Amount")
plt.ylabel("Number of Loans")
plt.tight_layout()
plt.savefig("chart2_loan_amount_distribution.png")
plt.close()
print("Chart 2 saved: Loan amount distribution — helps identify the typical loan size "
      "and whether large loans are rare outliers or common.")


# ============================================================
# CHART 3: Loan Disbursement Trend Over Time (Line chart)
# ============================================================
loans["application_date"] = pd.to_datetime(loans["application_date"], errors="coerce")
monthly_disbursement = loans.groupby(loans["application_date"].dt.to_period("M"))["loan_amount"].sum()

plt.figure(figsize=(10, 5))
monthly_disbursement.plot(kind="line", marker="o", color="seagreen")
plt.title("Monthly Loan Disbursement Trend")
plt.xlabel("Month")
plt.ylabel("Total Loan Amount Disbursed")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("chart3_disbursement_trend.png")
plt.close()
print("Chart 3 saved: Disbursement trend — shows whether lending activity is growing, "
      "shrinking, or seasonal over time.")


# ============================================================
# CHART 4: Default Rate by Loan Type (Bar chart)
# ============================================================
default_by_type = loans.groupby("loan_type")["default_flag"].mean() * 100

plt.figure(figsize=(8, 5))
default_by_type.sort_values(ascending=False).plot(kind="bar", color="crimson", edgecolor="black")
plt.title("Default Rate by Loan Type")
plt.xlabel("Loan Type")
plt.ylabel("Default Rate (%)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart4_default_rate_by_type.png")
plt.close()
print("Chart 4 saved: Default rate by loan type — highlights which loan products carry "
      "the highest risk and may need stricter approval criteria.")


# ============================================================
# CHART 5: Credit Score vs Loan Amount (Scatter plot)
# ============================================================
plt.figure(figsize=(8, 5))
plt.scatter(loans["credit_score"], loans["loan_amount"], alpha=0.4, color="purple", s=15)
plt.title("Credit Score vs Loan Amount")
plt.xlabel("Credit Score")
plt.ylabel("Loan Amount")
plt.tight_layout()
plt.savefig("chart5_creditscore_vs_loanamount.png")
plt.close()
print("Chart 5 saved: Credit score vs loan amount — reveals whether higher-scored "
      "customers tend to take larger loans, or if the relationship is weak.")


# ============================================================
# CHART 6: Account Status Breakdown (Pie chart)
# ============================================================
status_counts = accounts["account_status"].value_counts()

plt.figure(figsize=(6, 6))
plt.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%",
        colors=["mediumseagreen", "gold", "lightcoral"], startangle=90)
plt.title("Account Status Breakdown")
plt.tight_layout()
plt.savefig("chart6_account_status_pie.png")
plt.close()
print("Chart 6 saved: Account status breakdown — shows what portion of accounts are "
      "active vs dormant vs closed, relevant to customer engagement and retention.")


# ============================================================
# CHART 7: Transaction Volume by Channel (Bar chart)
# ============================================================
txn_by_channel = transactions.groupby("channel")["amount"].sum().sort_values(ascending=False)

plt.figure(figsize=(8, 5))
txn_by_channel.plot(kind="bar", color="teal", edgecolor="black")
plt.title("Total Transaction Volume by Channel")
plt.xlabel("Channel")
plt.ylabel("Total Transaction Amount")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart7_transaction_by_channel.png")
plt.close()
print("Chart 7 saved: Transaction volume by channel — shows which channels (branch, "
      "ATM, online, mobile) customers rely on most, useful for digital strategy decisions.")


# ============================================================
# CHART 8: Branch Type Distribution (Bar chart) — uses branches.csv
# ============================================================
branch_type_counts = branches["branch_type"].value_counts()

plt.figure(figsize=(7, 5))
branch_type_counts.plot(kind="bar", color="slateblue", edgecolor="black")
plt.title("Number of Branches by Type")
plt.xlabel("Branch Type")
plt.ylabel("Number of Branches")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart8_branch_type_distribution.png")
plt.close()
print("Chart 8 saved: Branch type distribution — shows the bank's urban/semi-urban/rural footprint.")


# ============================================================
# CHART 9: Loan Payment Status Breakdown (Bar chart) — uses loan_payments.csv
# ============================================================
payment_status_counts = loan_payments["payment_status"].value_counts()

plt.figure(figsize=(7, 5))
payment_status_counts.plot(kind="bar", color=["mediumseagreen", "gold", "indianred"], edgecolor="black")
plt.title("Loan Payment Status Breakdown")
plt.xlabel("Payment Status")
plt.ylabel("Number of Payments")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("chart9_payment_status.png")
plt.close()
print("Chart 9 saved: Payment status breakdown — shows how much repayment is on-time vs late vs missed.")

print("\nALL CHARTS SAVED. PHASE 5 COMPLETE.")