def sanitize_dataframe(df, cols): 
   """ 
   Sanitize PII columns in a DataFrame before sharing with AI. 
    
   Parameters: 
   ----------- 
   df : pandas DataFrame 
   cols : dict 
       {column_name: method} 
       Methods: 'hash', 'fake_email', 'fake_name', 'fake_address',  
                'fake_phone', 'mask' 
   """ 
   df_san = df.copy() 
    
   for col, method in cols.items(): 
       if col not in df_san.columns: 
           continue 
            
       if method == 'hash': 
           df_san[col] = df_san[col].apply( 
               lambda x: hashlib.sha256(str(x).encode()).hexdigest()[:16]  
               if pd.notna(x) else x 
           ) 
       elif method.startswith('fake_'): 
           f = getattr(fake, method.replace('fake_', '')) 
           df_san[col] = df_san[col].apply(lambda x: f() if pd.notna(x) else x) 
       elif method == 'mask': 
           df_san[col] = df_san[col].apply( 
               lambda x: f"{str(x)[:2]}***{str(x)[-2:]}"  
               if pd.notna(x) and len(str(x)) > 4 else x 
           ) 
    
   return df_san 


 

df_clean = sanitize_dataframe(df, { 
   'email': 'fake_email', 
   'first_name': 'fake_name', 
   'customer_id': 'hash', 
   'phone': 'mask' 
}) 
