SELECT 
    p.category, 
    COUNT(DISTINCT o.order_id) AS total_orders, 
    SUM(oi.quantity) AS units_sold, 
    SUM(oi.quantity * oi.unit_price) AS gross_revenue, 
    SUM(oi.quantity * p.cost_price) AS total_cost, 
    ROUND( 
        (SUM(oi.quantity * oi.unit_price) - SUM(oi.quantity * p.cost_price))  
        / NULLIF(SUM(oi.quantity * oi.unit_price), 0) * 100,  
        2 
    ) AS margin_pct 
FROM orders o 
JOIN order_items oi ON o.order_id = oi.order_id 
JOIN products p ON oi.product_id = p.product_id 
WHERE o.status = 'completed' 
    AND o.order_date >= '2023-10-01' 
    AND o.order_date < '2024-01-01' 
GROUP BY p.category 
ORDER BY gross_revenue DESC; 
