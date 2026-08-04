-- Step 1: Assign each customer to a cohort based on their signup month 
WITH cohorts AS ( 
   SELECT 
       customer_id, 
       DATE_TRUNC('month', signup_date)::date AS cohort_month 
   FROM customers 
), 
 
-- Step 2: Get each customer's completed order activity by month 
customer_activity AS ( 
   SELECT 
       o.customer_id, 
       DATE_TRUNC('month', o.order_date)::date AS activity_month 
   FROM orders o 
   WHERE o.status = 'completed' 
   GROUP BY o.customer_id, DATE_TRUNC('month', o.order_date) 
), 
 
-- Step 3: Join activity to cohort and calculate the month offset 
-- (number of months between signup month and activity month) 
cohort_activity AS ( 
   SELECT 
       c.customer_id, 
       c.cohort_month, 
       ca.activity_month, 
       (DATE_PART('year', ca.activity_month) - DATE_PART('year', c.cohort_month)) * 12 
           + (DATE_PART('month', ca.activity_month) - DATE_PART('month', c.cohort_month)) AS month_offset 
   FROM cohorts c 
   JOIN customer_activity ca 
       ON c.customer_id = ca.customer_id 
   WHERE ca.activity_month >= c.cohort_month 
), 
 
-- Step 4: Calculate the total size of each cohort 
cohort_size AS ( 
   SELECT 
       cohort_month, 
       COUNT(DISTINCT customer_id) AS cohort_size 
   FROM cohorts 
   GROUP BY cohort_month 
), 
 
-- Step 5: Count retained (distinct) customers per cohort per month offset 
retention AS ( 
   SELECT 
       cohort_month, 
       month_offset, 
       COUNT(DISTINCT customer_id) AS retained_users 
   FROM cohort_activity 
   GROUP BY cohort_month, month_offset 
) 
 
-- Step 6: Combine cohort size with retained users and calculate retention rate 
SELECT 
   TO_CHAR(r.cohort_month, 'YYYY-MM') AS cohort_month, 
   r.month_offset, 
   cs.cohort_size, 
   r.retained_users, 
   ROUND(100.0 * r.retained_users / cs.cohort_size, 2) AS retention_rate 
FROM retention r 
JOIN cohort_size cs 
   ON r.cohort_month = cs.cohort_month 
ORDER BY r.cohort_month, r.month_offset; 
