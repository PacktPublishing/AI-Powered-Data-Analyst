def flag_price_outliers(df, column_name='Unit_Price'): 
   """ 
   Flag outliers in a numeric column using the IQR method. 
    
   Parameters: 
   ----------- 
   df : pandas DataFrame 
       The dataset to process 
   column_name : str, default='Unit_Price' 
       The column to check for outliers 
    
   Returns: 
   -------- 
   pandas DataFrame with an added 'is_outlier' boolean column 
   """ 
   q1 = df[column_name].quantile(0.25) 
   q3 = df[column_name].quantile(0.75) 
   iqr = q3 - q1 
    
   lower_bound = q1 - (1.5 * iqr) 
   upper_bound = q3 + (1.5 * iqr) 
    
   df['is_outlier'] = (df[column_name] < lower_bound) | (df[column_name] > upper_bound) 
    
   return df 
