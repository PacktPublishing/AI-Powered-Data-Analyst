SELECT 
   -- DATE_TRUNC syntax differs: BigQuery uses DATE_TRUNC(date, part) 
   -- PostgreSQL: DATE_TRUNC('week', order_date)::date 
   -- BigQuery: DATE_TRUNC(order_date, WEEK)  
   -- Also: BigQuery's DATE_TRUNC returns DATE type directly, no ::date cast needed 
   DATE_TRUNC(order_date, WEEK) AS week_start, 
   region, 
   SUM(total_amount) AS revenue, 
   -- RANK() function works the same in BigQuery 
   -- Window syntax is identical 
   RANK() OVER ( 
       PARTITION BY DATE_TRUNC(order_date, WEEK) 
       ORDER BY SUM(total_amount) DESC 
   ) AS revenue_rank 
FROM orders 
WHERE order_date >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY) 
   -- ^ INTERVAL syntax differs: 
   -- PostgreSQL: NOW() - INTERVAL '90 days' 
   -- BigQuery: TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY) 
   -- Note: BigQuery requires DAY (not 'days' string) and uppercase interval units 
 AND status = 'completed' 
GROUP BY 1, 2; 
