SELECT 
   product_category, 
   clicks, 
   impressions, 
   (clicks / impressions) AS ctr 
FROM ad_performance; 
