def sum_numbers(numbers): 
   		# Handle None input 
   		if numbers is None: 
       		return 0 
    
   		total = 0 
   		for i in range(len(numbers)): 
       		total += numbers[i] 
   		return total
