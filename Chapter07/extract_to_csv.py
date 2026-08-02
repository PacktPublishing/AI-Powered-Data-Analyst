def listings_to_dataframe(all_listings): 
   columns = [ 
       "collected_at", "competitor", "year", "make", "model", "trim", 
       "mileage", "price", "condition", "seller_type", "location", 
       "listing_date", "title", "description", "url" 
   ] 
   df = pd.DataFrame(all_listings) 
   df = df.reindex(columns=columns) 
 
   df["price"] = pd.to_numeric(df["price"], errors="coerce") 
   df["mileage"] = pd.to_numeric(df["mileage"], errors="coerce") 
   df["year"] = pd.to_numeric(df["year"], errors="coerce") 
 
   return df 
 
 
def append_to_csv(df, filepath="competitor_listings.csv"): 
   write_header = not os.path.exists(filepath) 
   df.to_csv(filepath, mode="a", header=write_header, index=False) 
