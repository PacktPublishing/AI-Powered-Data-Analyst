EXPLAIN ANALYZE 
-- Correlated subquery (Slow) 
SELECT c.customer_id, c.email, 
  (SELECT MAX(order_date) FROM orders o WHERE o.customer_id = c.customer_id) AS last_order_date 
FROM customers c; 
