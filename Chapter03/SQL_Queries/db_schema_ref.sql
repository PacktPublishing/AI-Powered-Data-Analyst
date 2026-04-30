CREATE TABLE customers ( 
    customer_id     SERIAL PRIMARY KEY, 
    email           VARCHAR(255) NOT NULL UNIQUE, 
    signup_date     DATE NOT NULL, 
    country         VARCHAR(2), 
    tier            VARCHAR(10) CHECK (tier IN ('free', 'basic', 'pro', 'enterprise')) 
); 
CREATE TABLE orders ( 
    order_id        SERIAL PRIMARY KEY, 
    customer_id     INTEGER REFERENCES customers(customer_id), 
    order_date      TIMESTAMP NOT NULL, 
    subtotal        NUMERIC(10,2) NOT NULL, 
    discount        NUMERIC(10,2) DEFAULT 0, 
    status          VARCHAR(20) DEFAULT 'pending' 
); 
CREATE TABLE order_items ( 
    item_id         SERIAL PRIMARY KEY, 
    order_id        INTEGER REFERENCES orders(order_id), 
    product_id      INTEGER, 
    quantity        INTEGER NOT NULL, 
    unit_price      NUMERIC(10,2) NOT NULL 
