COMMENT ON TABLE orders IS  
   'Cleaned, deduplicated order events, one row per order.'; 
 
COMMENT ON COLUMN orders.order_status IS  
   'One of: pending, fulfilled, cancelled, refunded.'; 
