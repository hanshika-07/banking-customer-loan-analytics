import pandas as pd
import numpy as np

# ---------- LOAD ALL 6 CLEANED TABLES ----------
customers = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\cleaned\\customers_cleaned.csv")
branches = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\cleaned\\branches_cleaned.csv")
accounts = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\cleaned\\accounts_cleaned.csv")
loans = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\cleaned\\loans_cleaned.csv")
transactions = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\cleaned\\transactions_cleaned.csv")
loan_payments = pd.read_csv("C:\\Users\\hanshika\\Desktop\\banking-customer-loan-analytics\\data\\cleaned\\loan_payments_cleaned.csv")


# ============================================================
# 1. MEAN, MEDIAN, MODE, MIN, MAX, STANDARD DEVIATION
# ============================================================
print("=" * 70)
print("1. CENTRAL TENDENCY & SPREAD FOR KEY NUMERIC COLUMNS")
print("=" * 70)

def summary_stats(df, column, label):
    print(f"\n-- {label} --")
    print(f"Mean:   {df[column].mean():.2f}")
    print(f"Median: {df[column].median():.2f}")
    print(f"Mode:   {df[column].mode().iloc[0]:.2f}")
    print(f"Min:    {df[column].min():.2f}")
    print(f"Max:    {df[column].max():.2f}")
    print(f"Std Dev:{df[column].std():.2f}")

summary_stats(customers, "annual_income", "Annual Income")
summary_stats(loans, "loan_amount", "Loan Amount")
summary_stats(transactions, "amount", "Transaction Amount")
summary_stats(loans, "credit_score", "Credit Score")
summary_stats(accounts, "initial_balance", "Account Initial Balance")
summary_stats(loan_payments, "due_amount", "Loan Payment Due Amount")
summary_stats(loan_payments, "paid_amount", "Loan Payment Paid Amount")


# ============================================================
# 2. COMPARE MEAN vs MEDIAN (income, loan amount, transaction amount)
# ============================================================
print("\n" + "=" * 70)
print("2. MEAN vs MEDIAN COMPARISON")
print("=" * 70)

def compare_mean_median(df, column, label):
    mean_val = df[column].mean()
    median_val = df[column].median()
    diff_pct = ((mean_val - median_val) / median_val) * 100
    print(f"\n{label}:")
    print(f"  Mean = {mean_val:.2f}, Median = {median_val:.2f}, Difference = {diff_pct:.1f}%")
    if abs(diff_pct) < 5:
        print("  -> Mean and median are close: distribution is roughly symmetric.")
    elif mean_val > median_val:
        print("  -> Mean > Median: right-skewed (a few very high values pull the average up).")
    else:
        print("  -> Mean < Median: left-skewed (a few very low values pull the average down).")

compare_mean_median(customers, "annual_income", "Annual Income")
compare_mean_median(loans, "loan_amount", "Loan Amount")
compare_mean_median(transactions, "amount", "Transaction Amount")


# ============================================================
# 3. IDENTIFY SKEWED DISTRIBUTIONS
# ============================================================
print("\n" + "=" * 70)
print("3. SKEWNESS")
print("=" * 70)

def check_skew(df, column, label):
    skew_val = df[column].skew()
    if skew_val > 1:
        interpretation = "Highly right-skewed"
    elif skew_val > 0.5:
        interpretation = "Moderately right-skewed"
    elif skew_val < -1:
        interpretation = "Highly left-skewed"
    elif skew_val < -0.5:
        interpretation = "Moderately left-skewed"
    else:
        interpretation = "Approximately symmetric"
    print(f"{label}: skew = {skew_val:.2f} -> {interpretation}")

check_skew(customers, "annual_income", "Annual Income")
check_skew(loans, "loan_amount", "Loan Amount")
check_skew(transactions, "amount", "Transaction Amount")
check_skew(accounts, "initial_balance", "Account Initial Balance")


# ============================================================
# 4. QUARTILES AND IQR (at least 2 variables)
# ============================================================
print("\n" + "=" * 70)
print("4. QUARTILES AND IQR")
print("=" * 70)

def quartiles_iqr(df, column, label):
    Q1 = df[column].quantile(0.25)
    Q2 = df[column].quantile(0.50)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    print(f"\n{label}:")
    print(f"  Q1 (25%): {Q1:.2f}")
    print(f"  Q2 (50%/median): {Q2:.2f}")
    print(f"  Q3 (75%): {Q3:.2f}")
    print(f"  IQR: {IQR:.2f}")
    return Q1, Q3, IQR

income_q1, income_q3, income_iqr = quartiles_iqr(customers, "annual_income", "Annual Income")
loan_q1, loan_q3, loan_iqr = quartiles_iqr(loans, "loan_amount", "Loan Amount")
txn_q1, txn_q3, txn_iqr = quartiles_iqr(transactions, "amount", "Transaction Amount")


# ============================================================
# 5. IDENTIFY POTENTIAL OUTLIERS
# ============================================================
print("\n" + "=" * 70)
print("5. OUTLIER DETECTION")
print("=" * 70)

def find_outliers(df, column, Q1, Q3, IQR, label):
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    print(f"\n{label}:")
    print(f"  Normal range: {lower_bound:.2f} to {upper_bound:.2f}")
    print(f"  Outliers found: {len(outliers)} ({len(outliers)/len(df)*100:.2f}% of data)")
    return outliers

income_outliers = find_outliers(customers, "annual_income", income_q1, income_q3, income_iqr, "Annual Income")
loan_outliers = find_outliers(loans, "loan_amount", loan_q1, loan_q3, loan_iqr, "Loan Amount")
txn_outliers = find_outliers(transactions, "amount", txn_q1, txn_q3, txn_iqr, "Transaction Amount")


# ============================================================
# 6. PERCENTAGES AND PROPORTIONS
# ============================================================
print("\n" + "=" * 70)
print("6. KEY BUSINESS RATES")
print("=" * 70)

default_rate = loans["default_flag"].mean() * 100
print(f"\nOverall default rate: {default_rate:.2f}%")

active_account_rate = (accounts["account_status"] == "Active").mean() * 100
print(f"Active account rate: {active_account_rate:.2f}%")

dormant_rate = (accounts["account_status"] == "Dormant").mean() * 100
print(f"Dormant account rate: {dormant_rate:.2f}%")

approval_rate = (loans["loan_status"].isin(["Approved", "Active", "Closed"])).mean() * 100
print(f"Loan approval rate: {approval_rate:.2f}%")

# From loan_payments table
on_time_rate = (loan_payments["payment_status"] == "On Time").mean() * 100
missed_rate = (loan_payments["payment_status"] == "Missed").mean() * 100
print(f"\nOn-time payment rate: {on_time_rate:.2f}%")
print(f"Missed payment rate: {missed_rate:.2f}%")

# From branches table
urban_branch_pct = (branches["branch_type"] == "Urban").mean() * 100
print(f"\nUrban branch percentage: {urban_branch_pct:.2f}%")


# ============================================================
# 7. CORRELATION ANALYSIS (at least 3 meaningful relationships)
# ============================================================
print("\n" + "=" * 70)
print("7. CORRELATION ANALYSIS")  
print("=" * 70)

corr1 = loans["credit_score"].corr(loans["loan_amount"])
print(f"\nCredit Score vs Loan Amount: r = {corr1:.3f}")

corr2 = loans["credit_score"].corr(loans["interest_rate"])
print(f"Credit Score vs Interest Rate: r = {corr2:.3f}")

corr3 = loans["credit_score"].corr(loans["default_flag"])
print(f"Credit Score vs Default Flag: r = {corr3:.3f}")

# Using loan_payments: days_late vs due_amount
merged_payments = loan_payments.merge(loans[["loan_id", "loan_amount"]], on="loan_id", how="left")
corr4 = merged_payments["days_late"].corr(merged_payments["loan_amount"])
print(f"Days Late vs Loan Amount: r = {corr4:.3f}")

def interpret_corr(r):
    strength = "strong" if abs(r) > 0.7 else "moderate" if abs(r) > 0.3 else "weak"
    direction = "positive" if r > 0 else "negative"
    return f"{strength} {direction}"

print(f"\nInterpretation:")
print(f"  Credit Score vs Loan Amount: {interpret_corr(corr1)} relationship")
print(f"  Credit Score vs Interest Rate: {interpret_corr(corr2)} relationship")
print(f"  Credit Score vs Default: {interpret_corr(corr3)} relationship")
print(f"  Days Late vs Loan Amount: {interpret_corr(corr4)} relationship")


# ============================================================
# 8. BUSINESS INTERPRETATION SUMMARY
# ============================================================
print("\n" + "=" * 70)
print("8. BUSINESS INTERPRETATION SUMMARY")
print("=" * 70)

print(f"""
- Income distribution: mean vs median gap suggests {'a right-skew' if customers['annual_income'].mean() > customers['annual_income'].median() else 'a fairly symmetric spread'}, 
  meaning a small group of high earners may be pulling the average up.

- Default rate of {default_rate:.2f}% gives the bank a baseline risk level for provisioning and monitoring.

- Active account rate ({active_account_rate:.2f}%) vs dormant rate ({dormant_rate:.2f}%) shows how 
  engaged the customer base is — relevant for retention strategy.

- On-time payment rate of {on_time_rate:.2f}% (vs missed rate {missed_rate:.2f}%) indicates overall 
  repayment health across the loan book.

- Credit score vs interest rate correlation ({corr2:.3f}) shows whether pricing appropriately 
  rewards lower-risk customers.

- Credit score vs default correlation ({corr3:.3f}) tests whether credit score is actually 
  predictive of default risk in this data — if weak, other risk factors may need more weight.

- {urban_branch_pct:.1f}% of branches are Urban — useful context when comparing branch performance later.
""")

print("=" * 70)
print("STATISTICAL ANALYSIS COMPLETE")
print("=" * 70)
