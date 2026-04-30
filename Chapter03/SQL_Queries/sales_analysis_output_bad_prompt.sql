SELECT 
   DATE_TRUNC('month', o.order_date) AS month, 
   p.category, 
   COUNT(DISTINCT o.order_id) AS total_orders, 
   SUM(oi.quantity) AS units_sold, 
   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total_revenue, 
   ROUND(AVG(oi.quantity * oi.unit_price), 2) AS avg_order_value, 
   ROUND(SUM(oi.quantity * oi.unit_price - (oi.quantity * p.cost)), 2) AS total_profit, 
   ROUND((SUM(oi.quantity * oi.unit_price - (oi.quantity * p.cost)) / NULLIF(SUM(oi.quantity * oi.unit_price), 0)) * 100, 2) AS profit_margin_pct 
FROM orders o 
JOIN order_items oi ON o.order_id = oi.order_id 
JOIN products p ON oi.product_id = p.product_id 
WHERE o.order_date >= DATE_TRUNC('year', CURRENT_DATE) - INTERVAL '1 year' 
AND o.status NOT IN ('cancelled', 'refunded') 
GROUP BY DATE_TRUNC('month', o.order_date), p.category 
ORDER BY month DESC, total_revenue DESC; 
