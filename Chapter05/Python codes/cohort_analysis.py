import pandas as pd 
 
df['order_month'] = ( 
   df['order_date'] 
   .dt.to_period('M') 
) 
 
cohort = pd.pivot_table( 
   df, 
   index='cohort_month', 
   columns='order_month', 
   values='customer_id', 
   aggfunc='nunique' 
) 
