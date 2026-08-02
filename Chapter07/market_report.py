def analyze_model(df, model_name, competitor_urls=None): 
   subset = df[df["model"].str.lower() == model_name.lower()].dropna(subset=["price"]) 
 
   if subset.empty: 
       return None 
 
   return { 
       "model": model_name, 
       "count": len(subset), 
       "avg_price": subset["price"].mean(), 
       "min_price": subset["price"].min(), 
       "max_price": subset["price"].max(), 
       "avg_mileage": subset["mileage"].mean(), 
       "by_competitor": subset.groupby("competitor")["price"].mean().to_dict(), 
       "sample_listings": subset[["competitor", "year", "trim", "mileage", 
                                  "price", "location", "description"]] 
                           .head(5).to_dict("records") 
   } 
 
 
def generate_market_report(your_car, analysis): 
   prompt = f"""My car: {your_car} 
 
Market analysis for {analysis['model']}: 
- {analysis['count']} comparable listings found 
- Average price: ${analysis['avg_price']:,.0f} 
- Price range: ${analysis['min_price']:,.0f} to ${analysis['max_price']:,.0f} 
- Average mileage: {analysis['avg_mileage']:,.0f} 
- Average price by competitor: {analysis['by_competitor']} 
- Sample listings: {analysis['sample_listings']} 
 
Write a short market research report covering: a recommended listing price 
for my car, which competitor is priced most aggressively on this model, and 
what's likely driving any price spread you see across the sample listings.""" 
 
   message = client.messages.create( 
       model="claude-sonnet-5", 
       max_tokens=500, 
       messages=[{ 
           "role": "user", 
           "content": prompt 
       }] 
   ) 
   return message.content[0].text 
