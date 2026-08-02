from dotenv import load_dotenv 
from anthropic import Anthropic, RateLimitError, APIStatusError, APITimeoutError 
import os, time, random 
 
load_dotenv() 
 
api_key = os.getenv("ANTHROPIC_API_KEY") 
if not api_key: 
    raise ValueError("ANTHROPIC_API_KEY not found in environment variables") 
 
client = Anthropic(api_key=api_key) 
 
def summarize_with_retry(text, max_retries=3): 
    """Summarize text with exponential backoff retry logic.""" 
    for attempt in range(max_retries): 
        try: 
            return client.messages.create( 
                model="claude-sonnet-5", 
                max_tokens=150, 
                messages=[{"role": "user", "content": f"Summarize: {text}"}], 
                timeout=60.0 
            ).content[0].text 
        except (RateLimitError, APITimeoutError): 
            time.sleep((2 ** attempt) + random.uniform(0, 0.5)) 
        except APIStatusError as e: 
            if e.status_code >= 500: 
                time.sleep(2 ** attempt) 
            else: 
                raise 
    raise RuntimeError(f"Failed after {max_retries} attempts") 
