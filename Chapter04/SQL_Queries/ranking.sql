WITH rep_revenue AS ( 
    -- Calculate total revenue per sales rep for Q2 2025 
    SELECT  
        sr.rep_id, 
        sr.rep_name, 
        sr.region, 
        COALESCE(SUM(o.total_amount), 0) AS total_revenue 
    FROM sales_reps sr 
    LEFT JOIN orders o  
        ON sr.rep_id = o.rep_id 
        AND o.order_date >= '2025-04-01' 
        AND o.order_date < '2025-07-01' 
        AND o.status = 'completed'  -- Only count completed orders 
    GROUP BY sr.rep_id, sr.rep_name, sr.region 
), 
region_totals AS ( 
    -- Calculate total revenue per region for percentage calculation 
    SELECT  
        region, 
        SUM(total_revenue) AS region_total 
    FROM rep_revenue 
    GROUP BY region 
), 
ranked_reps AS ( 
    -- Calculate DENSE_RANK and percentage of region total 
    SELECT  
        rr.rep_id, 
        rr.rep_name, 
        rr.region, 
        rr.total_revenue, 
        rt.region_total, 
        DENSE_RANK() OVER ( 
            PARTITION BY rr.region  
            ORDER BY rr.total_revenue DESC 
        ) AS region_rank, 
        -- Revenue as percentage of region's total 
        CASE  
            WHEN rt.region_total = 0 THEN 0 
            ELSE ROUND((rr.total_revenue / rt.region_total) * 100, 2) 
        END AS revenue_pct_of_region, 
        -- Calculate quartile position 
        NTILE(4) OVER ( 
            PARTITION BY rr.region  
            ORDER BY rr.total_revenue DESC 
        ) AS quartile 
    FROM rep_revenue rr 
    JOIN region_totals rt ON rr.region = rt.region 
) 
-- Final output with performance tier 
SELECT  
    rep_id, 
    rep_name, 
    region, 
    total_revenue, 
    region_rank, 
    revenue_pct_of_region, 
    CASE  
        WHEN quartile = 1 THEN 'Top Performer' 
        ELSE 'Standard' 
    END AS performance_tier 
FROM ranked_reps 
ORDER BY region, region_rank; 
