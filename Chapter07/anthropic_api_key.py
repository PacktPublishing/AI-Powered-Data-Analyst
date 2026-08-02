import os 
from dotenv import load_dotenv 
from openai import OpenAI 
import anthropic 
 
load_dotenv() 
 
api_key = os.getenv("ANTHROPIC_API_KEY") 
 
client = anthropic.Anthropic(api_key=api_key) 
