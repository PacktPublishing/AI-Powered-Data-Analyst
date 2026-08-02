client = Anthropic() 
 
batch = client.messages.batches.create(requests=batch_requests) 
batch_id = batch.id 
print(f"Batch job created: {batch_id}") 
 
while True: 
   status_check = client.messages.batches.retrieve(batch_id) 
   print(f"Status: {status_check.status}") 
   if status_check.status in ["ended", "canceling", "canceled"]: 
       break 
   time.sleep(10) 
