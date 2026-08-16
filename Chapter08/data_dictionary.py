import pandas as pd 
import json 
import anthropic 
 
client = anthropic.Anthropic() 
 

def generate_data_dictionary(df, table_name="customers"): 
   """Generate a data dictionary from a DataFrame using Claude.""" 
    
   # Build schema description for AI 
   schema_description = "" 
   for col in df.columns: 
       sample_values = df[col].dropna().head(3).tolist() 
       unique_count = df[col].nunique() 
       missing_pct = (df[col].isnull().sum() / len(df)) * 100 
        
       schema_description += f""" 
       Column: {col} 
       - Data type: {df[col].dtype} 
       - Sample values: {sample_values} 
       - Unique values: {unique_count} 
       - Missing: {missing_pct:.1f}% 
       """ 
     
   prompt = f""" 
   Generate a data dictionary for the table '{table_name}'. 
    
   Schema information: 
  {schema_description} 
    
   For each column, provide: 
   1. Column name 
   2. Business name (what stakeholders call this field) 
   3. Description (what this field represents) 
   4. Data type (business meaning, not technical) 
   5. Example values 
   6. Constraints or rules (e.g., "must be > 0", "can be null") 
   7. Related columns (if any) 
    
   Return as a markdown table. 
   """ 
    
   response = client.messages.create( 
       model="claude-sonnet-5", 
       max_tokens=2048, 
       messages=[{"role": "user", "content": prompt}] 
   ) 
    
   return response.content[0].text 
 
# Usage 
df = pd.read_csv("customer_data.csv") 
dictionary = generate_data_dictionary(df, "customers") 
print(dictionary) 
