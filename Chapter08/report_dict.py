report_config = { 
   "executive": { 
       "metrics": ["Revenue", "Gross Margin", "New Customers", "Returns"], 
       "by_region": False, 
       "detail_level": "high" 
   }, 
   "regional_manager": { 
       "metrics": ["Revenue", "Orders", "Conversion Rate", "Returns"], 
       "by_region": True, 
       "detail_level": "medium" 
   }, 
   "analyst": { 
       "metrics": [ 
           "Revenue", "Orders", "Average Order Value", 
           "Conversion Rate", "Gross Margin", "Returns" 
       ], 
       "by_region": False, 
       "detail_level": "high" 
   } 
} 
