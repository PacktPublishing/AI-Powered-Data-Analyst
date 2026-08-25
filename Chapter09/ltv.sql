SELECT 
   acquisition_channel, 
   ROUND(AVG(total_lifetime_revenue), 2) AS avg_ltv 
FROM customer_summary 
WHERE acquisition_date BETWEEN '2025-10-01' AND '2025-12-31' 
GROUP BY acquisition_channel 
ORDER BY avg_ltv DESC; 
