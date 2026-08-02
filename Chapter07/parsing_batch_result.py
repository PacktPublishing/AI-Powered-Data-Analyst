if status_check.status == "ended": 
   results_map = {} 
   for result_line in client.messages.batches.results(batch_id): 
       if result_line.result.type == "succeeded": 
           results_map[result_line.custom_id] = result_line.result.message.content[0].text.strip() 
       else: 
           results_map[result_line.custom_id] = "Processing Error" 
 
   df["sentiment"] = df["review_id"].astype(str).map(results_map) 
   print(df) 
