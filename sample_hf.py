import pandas as pd

df_hf = pd.read_csv('data/hf_it_troubleshooting.csv')
print("=== HF CATEGORIES ===")
print(df_hf['Category'].value_counts())

print("\n=== SAMPLE HF ENTRIES ===")
for i, r in df_hf.head(8).iterrows():
    print(f"ID {r['ID']} | Cat: {r['Category']} | Issue: {r['Issue']}")
    print(f"  Symptoms: {str(r['Symptoms'])[:90]}")
    print(f"  Causes: {str(r['Common Causes'])[:90]}")
    print(f"  Solution: {str(r['Solution Steps'])[:90]}")
    print("-" * 50)
