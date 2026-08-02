import os 
from dotenv import load_dotenv 
import anthropic 
 
load_dotenv() 
 
api_key = os.getenv("ANTHROPIC_API_KEY") 
 
client = anthropic.Anthropic(api_key=api_key) 
 
message = client.messages.create( 
    model="claude-sonnet-5", 
    max_tokens=1000, 
    thinking={ 
        "type": "disabled" 
    }, 
    messages=[ 
        { 
            "role": "user", 
            "content": """ 
Sales Data: Jan: $10k, Feb: $12k, Mar: $9k, Apr: $15k 
 
Analyze: 
1. Average monthly revenue 
2. Month-over-month growth 
3. Best and worst month 
""" 
        } 
    ] 
) 
 
print(message.content[0].text) 
