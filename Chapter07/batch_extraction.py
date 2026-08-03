import requests 
from bs4 import BeautifulSoup 
 
def build_page_extraction_batch(pages): 

    """ 
   pages is a list of (page_url, competitor_name) tuples 
   """ 
   batch_requests = [] 
   custom_id_map = {} 
 
   for i, (page_url, competitor_name) in enumerate(pages): 
       response = requests.get(page_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15) 
       soup = BeautifulSoup(response.text, "html.parser") 
        
       for tag in soup(["script", "style", "nav", "footer"]): 
           tag.decompose() 
        
       page_text = soup.get_text(separator=" ", strip=True)[:15000] 
 
       custom_id = f"{competitor_name}-page{i}" 
       custom_id_map[custom_id] = competitor_name 
 
       prompt = f"""Extract every car listing on this page into a JSON array. 
For each listing include these fields: title, year, make, model, trim, mileage, 
price, location, condition, seller_type, listing_date, description, url. 
Use null for any field that isn't present. Respond with only the JSON array, 
no other text. 
 
Page content: 
{page_text}""" 
 
       batch_requests.append({ 
           "custom_id": custom_id, 
           "params": { 
               "model": "claude-sonnet-5", 
               "max_tokens": 2000, 
               "messages": [{ 
                   "role": "user", 
                   "content": prompt 
               }] 
           } 
       }) 
 
   return batch_requests, custom_id_map 
