batch_requests = [] 
 
for index, row in df.iterrows(): 
   request_line = { 
       "custom_id": str(row["review_id"]), 
       "params": { 
           "model": "claude-sonnet-5", 
           "max_tokens": 50, 
           "messages": [ 
               { 
                   "role": "user", 
                   "content": f"Classify this review into Positive, Negative, or Neutral. Output ONLY the word.\n\nReview: '{row['review_text']}'" 
               } 
           ] 
       } 
   } 
   batch_requests.append(request_line) 
