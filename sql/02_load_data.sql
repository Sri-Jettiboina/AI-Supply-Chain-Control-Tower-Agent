-- Load data into PostgreSQL.
-- Recommended: run src/load_to_postgres.py because it deduplicates suppliers/products/inventory.

DROP TABLE IF EXISTS staging_supply_chain;
CREATE TABLE staging_supply_chain (
    po_id VARCHAR(20),
    supplier_id VARCHAR(20),
    supplier_name VARCHAR(100),
    product_id VARCHAR(20),
    product_name VARCHAR(100),
    category VARCHAR(60),
    region VARCHAR(60),
    country VARCHAR(60),
    po_date DATE,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    quantity_ordered INT,
    quantity_received INT,
    inventory_level INT,
    forecasted_demand INT,
    reorder_point INT,
    po_value NUMERIC(14,2),
    defective_units INT,
    lead_time_days INT,
    delivery_status VARCHAR(30),
    base_risk_level VARCHAR(20)
);

-- Update this file path before running in psql:
-- COPY staging_supply_chain FROM '/absolute/path/to/data/cleaned_supply_chain_data.csv' DELIMITER ',' CSV HEADER;

INSERT INTO suppliers (supplier_id, supplier_name, country, category, base_risk_level)
SELECT DISTINCT supplier_id, supplier_name, country, category, base_risk_level
FROM staging_supply_chain
ON CONFLICT (supplier_id) DO NOTHING;

INSERT INTO products (product_id, product_name, category, region)
SELECT DISTINCT product_id, product_name, category, region
FROM staging_supply_chain
ON CONFLICT (product_id) DO NOTHING;

INSERT INTO inventory (product_id, inventory_level, forecasted_demand, reorder_point)
SELECT DISTINCT ON (product_id) product_id, inventory_level, forecasted_demand, reorder_point
FROM staging_supply_chain
ORDER BY product_id, po_date DESC
ON CONFLICT (product_id) DO UPDATE SET
    inventory_level = EXCLUDED.inventory_level,
    forecasted_demand = EXCLUDED.forecasted_demand,
    reorder_point = EXCLUDED.reorder_point,
    last_updated = CURRENT_DATE;

INSERT INTO purchase_orders (
    po_id, supplier_id, product_id, po_date, expected_delivery_date, actual_delivery_date,
    quantity_ordered, quantity_received, po_value, defective_units, lead_time_days, delivery_status
)
SELECT po_id, supplier_id, product_id, po_date, expected_delivery_date, actual_delivery_date,
       quantity_ordered, quantity_received, po_value, defective_units, lead_time_days, delivery_status
FROM staging_supply_chain
ON CONFLICT (po_id) DO NOTHING;
