from itertools import combinations 
import pandas as pd 
from rapidfuzz import fuzz  # pip install rapidfuzz 
 

def find_duplicates_from_series(name_series, threshold=80): 
   """ 
   Identifies potential duplicates from an isolated pandas Series 
   and returns a DataFrame referencing the original index positions. 
    
   Parameters: 
   ----------- 
   name_series : pandas Series 
       Series containing text values to check for duplicates 
   threshold : int, default=80 
       Similarity score threshold (0-100) above which pairs are flagged as duplicates 
    
   Returns: 
   -------- 
   pandas DataFrame with columns: 
       - Match_Score: Similarity score between the two names 
       - Original_Index_A: Index of first matching record 
       - Name_A: First matching name 
       - Original_Index_B: Index of second matching record 
       - Name_B: Second matching name 
   """ 
   # Clean the text data to improve matching accuracy 
   cleaned_series = name_series.astype(str).str.strip().str.lower() 
    
   # Extract a 'blocking key' (first letter) to optimize scalability 
   blocking_keys = cleaned_series.str[0] 
    
   duplicate_pairs = [] 
    
   # Group by the blocking key and find matches within those groups 
   for key in blocking_keys.unique(): 
       # Get the subset of the original series for this specific block 
       block = name_series[blocking_keys == key] 
        
       if len(block) < 2: 
           continue  # Skip blocks with only one name 
        
       # Compare unique pairs within the block using their indices 
       for idx1, idx2 in combinations(block.index, 2): 
           name1 = cleaned_series.loc[idx1] 
           name2 = cleaned_series.loc[idx2] 
            
           # Calculate similarity score (handles word reordering well) 
           score = fuzz.token_sort_ratio(name1, name2) 
            
           if score >= threshold: 
               duplicate_pairs.append({ 
                   "Match_Score": round(score, 1), 
                   "Original_Index_A": idx1, 
                   "Name_A": name_series.loc[idx1], 
                   "Original_Index_B": idx2, 
                   "Name_B": name_series.loc[idx2], 
               }) 
    
   return pd.DataFrame(duplicate_pairs)
