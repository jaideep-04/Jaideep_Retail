import pandas as pd

# Load data
df = pd.read_excel('data/sample_data/online_retail.xlsx')

print("DATA QUALITY FINDINGS:")
print("=" * 80)

issues = []

# Check 1: Missing Values
missing = df.isnull().sum().sum()
if missing > 0:
    issues.append(f"✓ Found {missing} missing values")
    print(f"\n1. MISSING VALUES ({missing} total):")
    print(df.isnull().sum()[df.isnull().sum() > 0])

# Check 2: Duplicates
dup = df.duplicated(subset=['Invoice', 'StockCode', 'Customer ID']).sum()
if dup > 0:
    issues.append(f"✓ Found {dup} duplicate transactions")
    print(f"\n2. DUPLICATES ({dup} total):")
    print("   Some transactions appear more than once")

# Check 3: Negative Quantities
neg_qty = (df['Quantity'] < 0).sum()
if neg_qty > 0:
    issues.append(f"✓ Found {neg_qty} negative quantities (RETURNS)")
    print(f"\n3. NEGATIVE QUANTITIES ({neg_qty} total):")
    print("   Example:")
    print(df[df['Quantity'] < 0].head(3))

# Check 4: Negative Prices
neg_price = (df['Price'] < 0).sum()
if neg_price > 0:
    issues.append(f"✓ Found {neg_price} negative prices (CREDITS/ADJUSTMENTS)")
    print(f"\n4. NEGATIVE PRICES ({neg_price} total):")
    print("   Example:")
    print(df[df['Price'] < 0].head(3))

# Check 5: Zero Values
zero_qty = (df['Quantity'] == 0).sum()
zero_price = (df['Price'] == 0).sum()
if zero_qty > 0 or zero_price > 0:
    issues.append(f"✓ Found {zero_qty} zero quantities and {zero_price} zero prices")
    print(f"\n5. ZERO VALUES:")
    print(f"   Zero quantities: {zero_qty}")
    print(f"   Zero prices: {zero_price}")

# Check 6: Unusual Quantities
large_qty = (df['Quantity'] > 1000).sum()
if large_qty > 0:
    issues.append(f"✓ Found {large_qty} very large quantities (>1000)")
    print(f"\n6. UNUSUAL QUANTITIES (>1000):")
    print(df[df['Quantity'] > 1000].head(3))

# Check 7: Missing Text Fields
missing_desc = df['Description'].isnull().sum()
if missing_desc > 0:
    issues.append(f"✓ Found {missing_desc} missing descriptions")
    print(f"\n7. MISSING DESCRIPTIONS: {missing_desc}")

# Check 8: Missing Customer IDs
missing_cust = df['Customer ID'].isnull().sum()
if missing_cust > 0:
    issues.append(f"✓ Found {missing_cust} missing Customer IDs (GUEST PURCHASES)")
    print(f"\n8. MISSING CUSTOMER IDs: {missing_cust}")

print("\n" + "=" * 80)
print("SUMMARY OF QUALITY ISSUES:")
for i, issue in enumerate(issues, 1):
    print(f"{i}. {issue}")

print("\n" + "=" * 80)
print("INTERPRETATION:")
print("=" * 80)
print("""
✓ NEGATIVE QUANTITIES: These are LEGITIMATE returns/cancellations - KEEP THEM
✓ NEGATIVE PRICES: These are adjustments/credits - KEEP THEM for analysis
✓ ZERO PRICES: Some products given for free or adjustments - HANDLE CAREFULLY
✓ MISSING CUSTOMER ID: These are guest purchases without registration - NORMAL
✓ MISSING DESCRIPTION: Minor issue, can assign "UNKNOWN" - NOT CRITICAL
✓ DUPLICATES: Need to be reviewed and removed - HANDLE IN ETL
""")

print("=" * 80)
print("RECOMMENDATION: ETL pipeline will handle these issues appropriately")
print("=" * 80)