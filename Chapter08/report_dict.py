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

audience = "regional_manager" 
config = report_config[audience] 
 
if config["by_region"]: 
   selected_metrics = weekly_metrics[ 
       weekly_metrics["Metric"].isin(config["metrics"]) 
   ].groupby(["Region", "Metric"], as_index=False)["Value"].sum() 
else: 
   selected_metrics = weekly_metrics[ 
       weekly_metrics["Metric"].isin(config["metrics"]) 
   ] 
