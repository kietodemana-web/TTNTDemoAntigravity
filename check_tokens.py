import sys
import pandas as pd
sys.stdout.reconfigure(encoding='utf-8')
df = pd.read_csv('data/processed_computer_troubleshooting.csv')
m = df[df['normalized_text'].str.contains('blue_screen', na=False)]
print("Total rows containing 'blue_screen':", len(m))
print(m['category'].value_counts())
print("\nSample 3 rows in Màn hình containing blue_screen:")
for i, r in m[m['category'] == 'Màn hình'].head(3).iterrows():
    print(r['source'], "|", r['issue_name'], "|", r['raw_symptoms'])
