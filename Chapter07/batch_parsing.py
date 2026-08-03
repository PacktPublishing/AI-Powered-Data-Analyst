def submit_and_parse_batch(client, batch_requests, poll_interval=60): 
   """ 
   Submits the batch, waits for it to finish, and returns a dict mapping 
   custom_id to the parsed list of listings extracted from that page. 
   """ 
   batch = client.messages.batches.create(requests=batch_requests) 
   print(f"Batch {batch.id} submitted, waiting for it to finish...") 
 
   while True: 
       batch = client.messages.batches.retrieve(batch.id) 
       if batch.processing_status == "ended": 
           break 
       time.sleep(poll_interval) 
 
   batch_results = {} 
   for entry in client.messages.batches.results(batch.id): 
       if entry.result.type != "succeeded": 
           print(f"Skipping {entry.custom_id}: {entry.result.type}") 
           continue 
 
       raw_text = entry.result.message.content[0].text.strip() 
       raw_text = strip_code_fence(raw_text) 
 
       try: 
           batch_results[entry.custom_id] = json.loads(raw_text) 
       except json.JSONDecodeError: 
           print(f"Could not parse JSON for {entry.custom_id}, skipping") 
           batch_results[entry.custom_id] = [] 
 
   return batch_results 
 
 
def strip_code_fence(text): 
   if text.startswith("```"): 
       text = text.strip("`") 
       if text.startswith("json"): 
           text = text[4:].strip() 
   return text 
