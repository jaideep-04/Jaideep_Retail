import pandas as pd
import numpy as np

# Load the data
df = pd.read_excel('data/sample_data/online_retail.xlsx')

print("=" * 80)
print("DATASET OVERVIEW")
print("=" * 80)

# 1. Basic Info
print("\n1. SHAPE (rows, columns):")
print(df.shape)

print("\n2. COLUMN NAMES:")
print(df.columns.tolist())

print("\n3. FIRST 10 ROWS:")
print(df.head(10))

print("\n4. DATA TYPES:")
print(df.dtypes)

print("\n5. BASIC STATISTICS:")
print(df.describe())

# 2. Missing Values
print("\n" + "=" * 80)
print("MISSING VALUES")
print("=" * 80)
print("\nNull counts per column:")
print(df.isnull().sum())

print("\nNull percentages:")
print((df.isnull().sum() / len(df) * 100).round(2))

# 3. Duplicates
print("\n" + "=" * 80)
print("DUPLICATES")
print("=" * 80)
print(f"\nTotal duplicate rows: {df.duplicated().sum()}")
print(f"\nDuplicates by Invoice+StockCode+Customer ID: {df.duplicated(subset=['Invoice', 'StockCode', 'Customer ID']).sum()}")

# 4. Value Ranges
print("\n" + "=" * 80)
print("VALUE RANGES & DISTRIBUTIONS")
print("=" * 80)

print(f"\nQuantity range: {df['Quantity'].min()} to {df['Quantity'].max()}")
print(f"Price range: {df['Price'].min()} to {df['Price'].max()}")
print(f"Date range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")

# 5. Unique Values
print("\n" + "=" * 80)
print("UNIQUE VALUES")
print("=" * 80)
print(f"\nUnique Invoices: {df['Invoice'].nunique()}")
print(f"Unique Products: {df['StockCode'].nunique()}")
print(f"Unique Customers: {df['Customer ID'].nunique()}")
print(f"Unique Countries: {df['Country'].nunique()}")

# 6. Countries Distribution
print("\n" + "=" * 80)
print("COUNTRIES (Top 15)")
print("=" * 80)
print(df['Country'].value_counts().head(15))

# 7. Negative/Zero Values
print("\n" + "=" * 80)
print("POTENTIAL DATA QUALITY ISSUES")
print("=" * 80)
print(f"\nNegative Quantities: {(df['Quantity'] < 0).sum()}")
print(f"Zero Quantities: {(df['Quantity'] == 0).sum()}")
print(f"Negative Prices: {(df['Price'] < 0).sum()}")
print(f"Zero Prices: {(df['Price'] == 0).sum()}")

# 8. Sample of each issue
print("\n" + "=" * 80)
print("SAMPLE RECORDS WITH ISSUES")
print("=" * 80)

if (df['Quantity'] < 0).sum() > 0:
    print("\nSample negative quantities:")
    print(df[df['Quantity'] < 0].head(3))

if (df['Price'] < 0).sum() > 0:
    print("\nSample negative prices:")
    print(df[df['Price'] < 0].head(3))

print("\n" + "=" * 80)
print("EDA COMPLETE")
print("=" * 80)

# 9. Summary for Dataset_Details.pdf
print("\n" + "=" * 80)
print("SUMMARY FOR DOCUMENTATION")
print("=" * 80)
print(f"\nTotal Records: {len(df)}")
print(f"Total Columns: {len(df.columns)}")
print(f"Date Range: {df['InvoiceDate'].min()} to {df['InvoiceDate'].max()}")
print(f"Unique Customers: {df['Customer ID'].nunique()}")
print(f"Unique Products: {df['StockCode'].nunique()}")
print(f"Unique Countries: {df['Country'].nunique()}")
print(f"\nMissing Values:")
print(f"  - Description: {df['Description'].isnull().sum()} ({(df['Description'].isnull().sum()/len(df)*100):.2f}%)")
print(f"  - Customer ID: {df['Customer ID'].isnull().sum()} ({(df['Customer ID'].isnull().sum()/len(df)*100):.2f}%)")
print(f"\nDuplicate Rows: {df.duplicated().sum()}")
print(f"Negative Quantities: {(df['Quantity'] < 0).sum()}")
print(f"Negative Prices: {(df['Price'] < 0).sum()}")