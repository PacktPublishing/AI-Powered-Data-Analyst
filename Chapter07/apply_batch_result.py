def apply_page_extraction_results(batch_results, custom_id_map): 
   all_listings = [] 
   for custom_id, listings in batch_results.items(): 
       competitor_name = custom_id_map[custom_id] 
       for listing in listings if isinstance(listings, list) else []: 
           listing["competitor"] = competitor_name 
           listing["collected_at"] = pd.Timestamp.now().isoformat() 
           all_listings.append(listing) 
   return all_listings
