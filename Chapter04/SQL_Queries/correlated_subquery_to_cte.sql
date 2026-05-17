WITH customer_last_order AS ( 
   SELECT  
       customer_id, 
       MAX(order_date) AS last_order_date 
   FROM orders 
   GROUP BY customer_id 
) 
SELECT  
   c.customer_id, 
   c.email, 
   clo.last_order_date 
FROM customers c 
LEFT JOIN customer_last_order clo ON c.customer_id = clo.customer_id; 
