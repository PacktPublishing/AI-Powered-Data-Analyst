import pandas as pd 
 
df = pd.read_csv('customer_data.csv') 
 
print(df.info()) 
print(df.describe()) 
print(df.isnull().sum()) 
