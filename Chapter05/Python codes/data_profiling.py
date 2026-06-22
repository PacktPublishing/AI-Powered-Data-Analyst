import pandas as pd 
import numpy as np 
 

def profile_dataframe(df): 
   """Generate comprehensive data quality report for a DataFrame.""" 
    
   # Basic info 
   print("=" * 80) 
   print("DATA QUALITY REPORT") 
   print("=" * 80) 
   print(f"\nShape: {df.shape[0]} rows, {df.shape[1]} columns") 
   print(f"Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB") 
   print(f"Duplicate rows: {df.duplicated().sum()}") 
    
   # Initialize summary list 
   summary_rows = [] 
    
   # Analyze each column 
   for col in df.columns: 
       row = {'column': col, 'dtype': str(df[col].dtype)} 
        
       # Missing values 
       missing_count = df[col].isnull().sum() 
       missing_pct = (missing_count / len(df)) * 100 
       row['missing_count'] = missing_count 
       row['missing_pct'] = round(missing_pct, 2) 
        
       # Unique values 
       unique_count = df[col].nunique() 
       row['unique_count'] = unique_count 
        
       # Type-specific analysis 
       if pd.api.types.is_numeric_dtype(df[col]): 
           row['min'] = df[col].min() 
           row['max'] = df[col].max() 
           row['mean'] = df[col].mean() 
           row['median'] = df[col].median() 
           row['std'] = df[col].std() 
           row['skew'] = df[col].skew() 
            
           # Outlier detection (values beyond 3 standard deviations) 
           mean = df[col].mean() 
           std = df[col].std() 
           if std > 0: 
               outliers = df[(df[col] < mean - 3*std) | (df[col] > mean + 3*std)][col].count() 
               row['outlier_count'] = outliers 
               row['outlier_pct'] = round((outliers / len(df)) * 100, 2) 
           else: 
               row['outlier_count'] = 0 
               row['outlier_pct'] = 0 
                
       elif pd.api.types.is_datetime64_any_dtype(df[col]): 
           row['min_date'] = df[col].min() 
           row['max_date'] = df[col].max() 
           row['date_range_days'] = (df[col].max() - df[col].min()).days 
            
       else:  # Categorical/text 
           value_counts = df[col].value_counts() 
           top_values = value_counts.head(5) 
           row['top_values'] = ', '.join([f"{v}: {c} ({c/len(df)*100:.1f}%)"  
                                         for v, c in top_values.items()]) 
        
       summary_rows.append(row) 
    
   # Create summary DataFrame 
   summary_df = pd.DataFrame(summary_rows) 
    
   # Print column summaries 
   print("\n" + "=" * 80) 
   print("COLUMN SUMMARIES") 
   print("=" * 80) 
    
   for _, row in summary_df.iterrows(): 
       print(f"\n--- {row['column']} ({row['dtype']}) ---") 
       print(f"  Missing: {row['missing_count']} ({row['missing_pct']}%)") 
       print(f"  Unique values: {row['unique_count']}") 
        
       if 'mean' in row: 
           print(f"  Range: {row['min']:.2f} to {row['max']:.2f}") 
           print(f"  Mean: {row['mean']:.2f}, Median: {row['median']:.2f}") 
           if 'outlier_count' in row: 
               print(f"  Outliers: {row['outlier_count']} ({row['outlier_pct']}%)") 
       elif 'min_date' in row: 
           print(f"  Date range: {row['min_date']} to {row['max_date']} ({row['date_range_days']} days)") 
       elif 'top_values' in row: 
           print(f"  Top values: {row['top_values']}") 
    
   # Correlation matrix for numeric columns 
   numeric_cols = df.select_dtypes(include=[np.number]).columns 
   if len(numeric_cols) > 1: 
       print("\n" + "=" * 80) 
       print("CORRELATION MATRIX (Top 10 correlations)") 
       print("=" * 80) 
       corr_matrix = df[numeric_cols].corr() 
        
       # Get top correlations (excluding self-correlations) 
       corr_pairs = [] 
       for i in range(len(corr_matrix.columns)): 
           for j in range(i+1, len(corr_matrix.columns)): 
               corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j],  
                                  corr_matrix.iloc[i, j])) 
       corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True) 
        
       for col1, col2, corr in corr_pairs[:10]: 
           print(f"  {col1} vs {col2}: {corr:.3f}") 
    
   return summary_df 
 
# Usage 
# summary = profile_dataframe(df) 
