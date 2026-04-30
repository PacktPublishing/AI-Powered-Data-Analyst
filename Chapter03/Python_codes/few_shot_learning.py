def calculate_daily_revenue(transactions): 
   """ 
   Calculate total revenue per day from a list of transaction dictionaries. 
 
   Args: 
       transactions: List of dicts with 'amount' and 'created_at' keys 
 
   Returns: 
       dict: Date to total revenue mapping 
   """ 
   daily_totals = {} 
 
   for transaction in transactions: 
       transaction_date = transaction.get('created_at', '').split('T')[0] 
       transaction_amount = transaction.get('amount', 0) 
 
       if transaction_date: 
           daily_totals[transaction_date] = daily_totals.get(transaction_date, 0) + transaction_amount 
 
   return daily_totals 
