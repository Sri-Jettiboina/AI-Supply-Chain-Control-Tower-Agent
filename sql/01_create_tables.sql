-- AI Supply Chain Control Tower Agent
-- PostgreSQL schema

DROP TABLE IF EXISTS purchase_orders CASCADE;
DROP TABLE IF EXISTS inventory CASCADE;
DROP TABLE IF EXISTS suppliers CASCADE;
DROP TABLE IF EXISTS products CASCADE;

CREATE TABLE suppliers (
    supplier_id VARCHAR(20) PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    country VARCHAR(60),
    category VARCHAR(60),
    base_risk_level VARCHAR(20)
);

CREATE TABLE products (
    product_id VARCHAR(20) PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(60),
    region VARCHAR(60)
);

CREATE TABLE inventory (
    product_id VARCHAR(20) PRIMARY KEY REFERENCES products(product_id),
    inventory_level INT,
    forecasted_demand INT,
    reorder_point INT,
    last_updated DATE DEFAULT CURRENT_DATE
);

CREATE TABLE purchase_orders (
    po_id VARCHAR(20) PRIMARY KEY,
    supplier_id VARCHAR(20) REFERENCES suppliers(supplier_id),
    product_id VARCHAR(20) REFERENCES products(product_id),
    po_date DATE,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    quantity_ordered INT,
    quantity_received INT,
    po_value NUMERIC(14,2),
    defective_units INT,
    lead_time_days INT,
    delivery_status VARCHAR(30)
);

CREATE INDEX idx_purchase_orders_supplier ON purchase_orders(supplier_id);
CREATE INDEX idx_purchase_orders_product ON purchase_orders(product_id);
CREATE INDEX idx_purchase_orders_po_date ON purchase_orders(po_date);
