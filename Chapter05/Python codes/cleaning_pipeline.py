import pandas as pd 
 
class CleaningPipeline: 
   """Reusable, auditable cleaning pipeline.""" 
    
   def __init__(self, verbose=True): 
       self.verbose = verbose 
       self.log = [] 
       self.flagged_rows = pd.DataFrame() 
    
   def _record(self, step, detail): 
       self.log.append({'step': step, 'detail': detail}) 
       if self.verbose: 
           print(f'[{step}] {detail}') 
    
   def run(self, df): 
       df = df.copy() 
       start = len(df) 
        
      # Type coercion 
       df['order_date'] = pd.to_datetime(df['order_date'], errors='coerce') 
       self._record('TYPE COERCION', f"{df['order_date'].isnull().sum()} bad dates") 
        
       # Standardize categories 
       df = self._standardise_categories(df, 'product_category') 
       self._record('STANDARDISE', 'categories normalised') 
        
       # Missing values 
       df, flagged = self._handle_missing(df) 
       self.flagged_rows = flagged 
       self._record('MISSING', f'{len(flagged)} rows flagged') 
        
       # Outliers 
       df = self._flag_outliers(df, ['unit_price', 'quantity']) 
       self._record('OUTLIERS', 'outliers flagged') 
        
       # Deduplication 
       before = len(df) 
       df = self._deduplicate(df, ['order_id']) 
       self._record('DEDUP', f'{before - len(df)} duplicates removed') 
        
       self._record('COMPLETE', f'{start:,} -> {len(df):,} rows') 
       return df, pd.DataFrame(self.log), self.flagged_rows 
    
   def _standardise_categories(self, df, col): 
       mapping = {'electronics': 'Electronics', 'clothing': 'Clothing',  
                  'books': 'Books', 'home': 'Home Goods'} 
       df[col] = df[col].str.lower().str.strip().replace(mapping).fillna('Other') 
       return df 
    
   def _handle_missing(self, df): 
       flagged = df[df['revenue'].isnull()].copy() if 'revenue' in df.columns else pd.DataFrame() 
        
       for col in df.select_dtypes(include=['number']).columns: 
           df[col] = df[col].fillna(df[col].median()) 
        
       for col in df.select_dtypes(include=['object']).columns: 
           df[col] = df[col].fillna('Unknown') 
        
       return df, flagged 
    
   def _flag_outliers(self, df, cols): 
       for col in cols: 
           if col in df.columns: 
               q1, q3 = df[col].quantile(0.25), df[col].quantile(0.75) 
               iqr = q3 - q1 
               lb, ub = q1 - 1.5*iqr, q3 + 1.5*iqr 
               df[f'{col}_outlier'] = (df[col] < lb) | (df[col] > ub) 
       return df 
    
   def _deduplicate(self, df, key_cols): 
       return df.drop_duplicates(subset=key_cols, keep='first') 
