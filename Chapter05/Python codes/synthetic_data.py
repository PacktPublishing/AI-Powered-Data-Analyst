from faker import Faker 
import pandas as pd 
import numpy as np 
 
fake = Faker() 
 
customers = [] 
 
for customer_id in range(100000): 
   customers.append({ 
       "customer_id": customer_id, 
       "age": np.random.randint(18, 70), 
       "country": fake.country(), 
       "signup_date": fake.date_between( 
           start_date='-5y', 
           end_date='today' 
       ) 
   }) 
 
customers_df = pd.DataFrame(customers) 
customers_df.head() 
