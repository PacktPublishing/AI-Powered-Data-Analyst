# total_spent: fill with median 
df['total_spent'] = df['total_spent'].fillna(df['total_spent'].median()) 
 
# preferred_category: fill with 'Unknown' 
df['preferred_category'] = df['preferred_category'].fillna('Unknown') 
 
# email: drop rows with missing email 
df = df.dropna(subset=['email']) 
 
# delivery_date: add is_pending column 
df['is_pending'] = df['delivery_date'].isnull() 
 
# Drop numeric columns with >30% missing 
numeric_cols = df.select_dtypes(include=['number']).columns 
missing_pct = df[numeric_cols].isnull().sum() / len(df) 
cols_to_drop = missing_pct[missing_pct > 0.3].index 
df = df.drop(columns=cols_to_drop) 
 
# Flag rows with null revenue for investigation 
df_investigate = df[df['revenue'].isnull()].copy() if 'revenue' in df.columns else pd.DataFrame() 
