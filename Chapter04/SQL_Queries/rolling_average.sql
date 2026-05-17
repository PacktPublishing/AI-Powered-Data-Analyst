WITH daily_revenue AS ( 

-- Aggregate revenue by day and region for completed orders 
    SELECT  
        order_date, 
        region, 
        SUM(total_amount) AS daily_revenue 
    FROM orders 
    WHERE status = 'completed'  -- Assuming there's a status column 
    GROUP BY order_date, region 
) 
SELECT  
    order_date, 
    region, 
    daily_revenue, 
     
    -- 7-day rolling average (current day + previous 6 days) 
    -- ROWS BETWEEN 6 PRECEDING AND CURRENT ROW includes: 
    -- - Current row (day) 
    -- - 6 rows before current (previous 6 days) 
    -- Total of 7 days in the window 
    AVG(daily_revenue) OVER ( 
        PARTITION BY region  
        ORDER BY order_date  
        ROWS BETWEEN 6 PRECEDING AND CURRENT ROW 
    ) AS rolling_7_day_avg, 
     
    -- Cumulative revenue from start of current month 
    -- ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW includes: 
    -- - All rows from the start of the partition (first day of month) 
    -- - Up through current row 
    -- PARTITION BY region, month ensures it resets each month 
    SUM(daily_revenue) OVER ( 
        PARTITION BY region, DATE_TRUNC('month', order_date) 
        ORDER BY order_date  
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW 
    ) AS cumulative_month_revenue, 
     
    -- Day-over-day change (absolute amount) 
    -- LAG accesses previous row's daily_revenue without a frame clause 
    -- LAG with 1 offset means the immediately preceding row 
    daily_revenue - LAG(daily_revenue, 1) OVER ( 
        PARTITION BY region  
        ORDER BY order_date 
    ) AS dod_change_absolute 
     
FROM daily_revenue 
ORDER BY region, order_date ASC; 
