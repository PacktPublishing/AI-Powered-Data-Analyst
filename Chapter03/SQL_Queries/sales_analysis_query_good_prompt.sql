SELECT 
   TO_CHAR(DATE_TRUNC('month', order_date), 'YYYY-MM') AS month, 
   region, 
   SUM(sales_amount) AS total_sales 
FROM sales_fact 
WHERE 
   EXTRACT(YEAR FROM order_date) = 2026 
   AND EXTRACT(QUARTER FROM order_date) = 1 
   AND status = 'completed' 
   AND region != 'TEST' 
GROUP BY DATE_TRUNC('month', order_date), region 
ORDER BY 
   DATE_TRUNC('month', order_date) ASC, 
   total_sales DESC; 
