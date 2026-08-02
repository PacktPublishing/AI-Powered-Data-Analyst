import pandas as pd 

import time 
from anthropic import Anthropic 
 
data = { 
   "review_id": ["rev_001", "rev_002", "rev_003"], 
   "review_text": [ 
       "The shipping took two weeks and the box arrived damaged. Terrible service.", 
       "Absolutely love this product! It works exactly as advertised and feels durable.", 
       "It is okay, nothing special. A bit overpriced for what you actually get." 
   ] 
} 
 
df = pd.DataFrame(data) 
