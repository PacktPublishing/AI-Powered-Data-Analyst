SELECT  
   s.name,  
   SUM(o.total_amount) AS quarterly_revenue,  
   COUNT(o.order_id) AS order_count  
FROM orders o  
JOIN salespeople s ON o.salesperson_id = s.id  
WHERE o.order_date BETWEEN '2026-01-01' AND '2026-03-31'  
GROUP BY s.name  
HAVING quarterly_revenue > 10000; 
 
-- Error: column 'quarterly_revenue' does not exist  
-- Database: MySQL 8.0 
