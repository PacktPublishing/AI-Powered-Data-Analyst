WITH monthly_active AS ( 
    -- Calculate active users per month and channel 
    SELECT  
        DATE_TRUNC('month', le.event_date) AS month, 
        c.acquisition_channel, 
        COUNT(DISTINCT le.customer_id) AS monthly_active_users 
    FROM login_events le 
    INNER JOIN customers c ON le.customer_id = c.customer_id 
    WHERE le.event_date BETWEEN '2026-01-01' AND '2026-03-31'  -- Q1 2026 
    GROUP BY DATE_TRUNC('month', le.event_date), c.acquisition_channel 
), 
with_previous AS ( 
    -- Use LAG to get previous month's users for each channel 
    SELECT  
        month, 
        acquisition_channel, 
        monthly_active_users, 
        LAG(monthly_active_users) OVER ( 
            PARTITION BY acquisition_channel  
            ORDER BY month 
        ) AS previous_month_users 
    FROM monthly_active 
) 
SELECT  
    TO_CHAR(month, 'YYYY-MM') AS month, 
    acquisition_channel, 
    monthly_active_users, 
    COALESCE(previous_month_users, 0) AS previous_month_users, 
    -- Calculate MoM change percentage 
    CASE  
        WHEN previous_month_users IS NULL OR previous_month_users = 0 THEN NULL 
        ELSE ROUND( 
            ((monthly_active_users - previous_month_users)::NUMERIC / previous_month_users) * 100,  
            1 
        ) 
    END AS month_over_month_change 
FROM with_previous 
ORDER BY acquisition_channel, month; 
