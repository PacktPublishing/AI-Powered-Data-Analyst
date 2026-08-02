import asyncio, random 
from anthropic import AsyncAnthropic, RateLimitError 
 
client = AsyncAnthropic() 
semaphore = asyncio.Semaphore(5)  # concurrency + throttling cap 
 
async def classify(ticket_id, text, max_retries=4): 
   async with semaphore: 
       for attempt in range(max_retries): 
           try: 
               r = await client.messages.create( 
                   model="claude-sonnet-5", max_tokens=50, 
                   messages=[{"role": "user", "content": f"Classify: {text}"}]) 
               return ticket_id, r.content[0].text.strip() 
           except RateLimitError as e: 
               wait = float(e.response.headers.get("retry-after", 2 ** attempt)) + random.uniform(0, 1) 
               await asyncio.sleep(wait) 
       return ticket_id, "Failed after retries" 
 
async def main(tickets): 
   results = await asyncio.gather(*(classify(t, x) for t, x in tickets), return_exceptions=True) 
   for r in results: 
       print(r if isinstance(r, Exception) else f"{r[0]}: {r[1]}") 
 
asyncio.run(main([("t1", "Order never arrived"), ("t2", "App won't open"), ("t3", "Wrong item shipped")])) 
