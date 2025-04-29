import pandas as pd
import numpy as np
import re

# ---- Sample Loan Data ----
data = {
    'LoanID': [101, 102, 103, 104, 105],
    'LoanAmount': [250000, 500000, np.nan, 1200000, 300000],
    'FICOScore': [720, np.nan, 680, 790, 610],
    'LoanPurpose': [' Home purchase ', 'Refinance', None, 'Debt Consolidation', 'home Purchase'],
    'ZipCode': ['60616', '6061-6', 'IL 60616', np.nan, '60616']
}

df = pd.DataFrame(data)

print("Original Data:")
print(df)

# ---- Step 1: Handle Missing Values ----
num_cols = df.select_dtypes(include='number').columns
df[num_cols] = df[num_cols].fillna(df[num_cols].median())

str_cols = df.select_dtypes(include='object').columns
df[str_cols] = df[str_cols].fillna('Unknown')

# ---- Step 2: Remove Outliers from LoanAmount ----
Q1 = df['LoanAmount'].quantile(0.25)
Q3 = df['LoanAmount'].quantile(0.75)
IQR = Q3 - Q1
df = df[(df['LoanAmount'] >= Q1 - 1.5 * IQR) & (df['LoanAmount'] <= Q3 + 1.5 * IQR)]

# ---- Step 3: Normalize Formats ----
# ZIP code cleanup (keep only digits, first 5 characters)
df['ZipCode'] = df['ZipCode'].astype(str).apply(lambda x: re.sub(r'\D', '', x)[:5])

# Normalize LoanPurpose
df['LoanPurpose'] = df['LoanPurpose'].str.lower().str.strip()

# ---- Output Cleaned Data ----
print("\nCleaned Data:")
print(df)

# Save to CSV (optional)
df.to_csv('loan_data_cleaned.csv', index=False)
