-- Step 1 (CTE: monthly_orders): Get one row per customer per month for completed orders in the last 6 months 
-- This ensures each customer appears at most once per calendar month, preventing duplicate counts 
-- if they place multiple orders in the same month. The 6-month window is the last 6 complete months 
-- excluding the current month to ensure consistent analysis periods. 

WITH monthly_orders AS ( 
   SELECT DISTINCT 
       customer_id, 
       DATE_TRUNC('month', order_date) AS order_month 
   FROM orders 
   WHERE status = 'completed' 
       AND order_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '6 months' 
       AND order_date < DATE_TRUNC('month', CURRENT_DATE)  -- Excludes current partial month 
), 
 
-- Step 2 (CTE: customer_activity): Count distinct active months per customer 
-- By counting how many distinct months each customer appears in the monthly_orders CTE, 
-- we identify customers who have been consistently active over the 6-month window. 
-- The threshold for "consistent" will be applied in the next step (3+ months). 
customer_activity AS ( 
   SELECT 
       customer_id, 
       COUNT(DISTINCT order_month) AS active_months 
   FROM monthly_orders 
   GROUP BY customer_id 
), 
 
-- Step 3 (CTE: qualifying_customers): Filter to customers with 3+ active months 
-- This applies the business rule: "least 3 of the last 6 calendar months" 
-- Customers who meet this threshold are considered "consistently active" and move to final analysis. 
qualifying_customers AS ( 
   SELECT 
       customer_id, 
       active_months 
   FROM customer_activity 
   WHERE active_months >= 3 
), 
 
-- Step 4 (Final SELECT): Join back to orders to calculate average order value and total revenue per qualifying customer 
-- We join the qualifying customers back to the original orders table to calculate: 
-- 1. Average Order Value (AOV) = total revenue / number of orders 
-- 2. Total Revenue = sum of all order amounts for the 6-month window 
-- Using only completed orders ensures revenue data is accurate (no refunds/cancellations). 
SELECT  
   qc.customer_id, 
   qc.active_months, 
   COUNT(o.order_id) AS total_orders, 
   ROUND(SUM(o.amount)::NUMERIC, 2) AS total_revenue, 
   ROUND(AVG(o.amount)::NUMERIC, 2) AS average_order_value 
FROM qualifying_customers qc 
JOIN orders o ON qc.customer_id = o.customer_id 
WHERE o.status = 'completed' 
   AND o.order_date >= DATE_TRUNC('month', CURRENT_DATE) - INTERVAL '6 months' 
   AND o.order_date < DATE_TRUNC('month', CURRENT_DATE) 
GROUP BY qc.customer_id, qc.active_months 
ORDER BY total_revenue DESC; 
