import os 
import requests 
from dotenv import load_dotenv 
 
load_dotenv() 
 
admin_key = os.getenv("ANTHROPIC_ADMIN_KEY") 
 
response = requests.get( 
   "https://api.anthropic.com/v1/organizations/usage_report/messages", 
   headers={ 
       "x-api-key": admin_key, 
       "anthropic-version": "2023-06-01", 
   }, 
   params={ 
       "starting_at": "2026-07-21T00:00:00Z", 
       "ending_at": "2026-07-28T00:00:00Z", 
       "bucket_width": "1d", 
   }, 
) 
 
usage_data = response.json() 
print(usage_data) 
