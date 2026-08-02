def log_weekly_report(analysis, report_text, filepath="market_pricing_tracking.csv"): 
   row = pd.DataFrame([{ 
       "date": pd.Timestamp.now().date(), 
       "model": analysis["model"], 
       "listing_count": analysis["count"], 
       "avg_price": analysis["avg_price"], 
       "min_price": analysis["min_price"], 
       "max_price": analysis["max_price"], 
       "avg_mileage": analysis["avg_mileage"], 
       "report": report_text 
   }]) 
   write_header = not os.path.exists(filepath) 
   row.to_csv(filepath, mode="a", header=write_header, index=False) 
