SELECT 
   product_category, 
   clicks, 
   impressions, 
   (clicks / NULLIF(impressions, 0)) AS ctr 
FROM ad_performance; 
