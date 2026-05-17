SELECT 
   s.name, 
   SUM(o.total_amount)   AS quarterly_revenue, 
   COUNT(o.order_id)     AS order_count 
FROM orders o 
JOIN salespeople s ON o.salesperson_id = s.id 
WHERE o.order_date >= '2026-01-01' 
 AND o.order_date <  '2026-04-01' 
GROUP BY s.name 
HAVING SUM(o.total_amount) > 10000 
ORDER BY quarterly_revenue DESC; 
