import pandas as pd

df_ora = pd.read_csv('data/ora_aggregate_202507.csv', usecols=['id', 'product_category', 'problem', 'repair_barrier_if_end_of_life', 'repair_status'])
pc_df = df_ora[df_ora['product_category'].isin(['Laptop', 'Desktop computer', 'Flat screen'])].dropna(subset=['problem'])
print(f"Total PC/Laptop/Monitor rows with non-empty problem in ORA: {len(pc_df)}")
print("\nSample 15 ORA problem descriptions:")
for i, r in pc_df.head(15).iterrows():
    # encode to ascii safe
    prob = r['problem'].encode('ascii', errors='replace').decode('ascii')
    print(f"[{r['product_category']}] {prob}")
