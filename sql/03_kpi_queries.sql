-- Supplier KPI queries for the AI Supply Chain Control Tower Agent

-- 1. Supplier late delivery rate
SELECT 
    s.supplier_name,
    s.country,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN p.delivery_status = 'Late' THEN 1 ELSE 0 END) AS late_orders,
    ROUND(100.0 * SUM(CASE WHEN p.delivery_status = 'Late' THEN 1 ELSE 0 END) / COUNT(*), 2) AS late_delivery_rate
FROM purchase_orders p
JOIN suppliers s ON p.supplier_id = s.supplier_id
GROUP BY s.supplier_name, s.country
ORDER BY late_delivery_rate DESC;

-- 2. Supplier defect rate
SELECT 
    s.supplier_name,
    SUM(p.defective_units) AS total_defective_units,
    SUM(p.quantity_received) AS total_received_units,
    ROUND(100.0 * SUM(p.defective_units) / NULLIF(SUM(p.quantity_received), 0), 2) AS defect_rate
FROM purchase_orders p
JOIN suppliers s ON p.supplier_id = s.supplier_id
GROUP BY s.supplier_name
ORDER BY defect_rate DESC;

-- 3. Monthly procurement spend
SELECT 
    DATE_TRUNC('month', po_date)::date AS month,
    ROUND(SUM(po_value), 2) AS total_spend
FROM purchase_orders
GROUP BY DATE_TRUNC('month', po_date)
ORDER BY month;

-- 4. Top high-spend suppliers
SELECT 
    s.supplier_name,
    s.country,
    s.category,
    ROUND(SUM(p.po_value), 2) AS total_spend,
    COUNT(*) AS order_count
FROM purchase_orders p
JOIN suppliers s ON p.supplier_id = s.supplier_id
GROUP BY s.supplier_name, s.country, s.category
ORDER BY total_spend DESC
LIMIT 10;

-- 5. Inventory stockout risk
SELECT 
    pr.product_name,
    pr.category,
    pr.region,
    i.inventory_level,
    i.forecasted_demand,
    i.reorder_point,
    CASE 
        WHEN i.inventory_level < i.reorder_point THEN 'High Stockout Risk'
        WHEN i.inventory_level < i.forecasted_demand THEN 'Medium Stockout Risk'
        ELSE 'Low Risk'
    END AS stockout_risk
FROM inventory i
JOIN products pr ON i.product_id = pr.product_id
ORDER BY 
    CASE 
        WHEN i.inventory_level < i.reorder_point THEN 1
        WHEN i.inventory_level < i.forecasted_demand THEN 2
        ELSE 3
    END;

-- 6. Supplier risk score
WITH supplier_kpis AS (
    SELECT
        s.supplier_id,
        s.supplier_name,
        COUNT(*) AS total_orders,
        ROUND(100.0 * SUM(CASE WHEN p.delivery_status = 'Late' THEN 1 ELSE 0 END) / COUNT(*), 2) AS late_delivery_rate,
        ROUND(100.0 * SUM(p.defective_units) / NULLIF(SUM(p.quantity_received), 0), 2) AS defect_rate,
        ROUND(AVG(p.lead_time_days), 2) AS avg_lead_time,
        ROUND(SUM(p.po_value), 2) AS total_spend
    FROM purchase_orders p
    JOIN suppliers s ON p.supplier_id = s.supplier_id
    GROUP BY s.supplier_id, s.supplier_name
)
SELECT *,
    ROUND(
        (late_delivery_rate * 0.40) +
        (defect_rate * 8.00) +
        (avg_lead_time * 0.80) +
        (CASE WHEN total_spend > 200000 THEN 15 ELSE 5 END), 2
    ) AS risk_score,
    CASE
        WHEN ((late_delivery_rate * 0.40) + (defect_rate * 8.00) + (avg_lead_time * 0.80) + (CASE WHEN total_spend > 200000 THEN 15 ELSE 5 END)) >= 70 THEN 'Critical Risk'
        WHEN ((late_delivery_rate * 0.40) + (defect_rate * 8.00) + (avg_lead_time * 0.80) + (CASE WHEN total_spend > 200000 THEN 15 ELSE 5 END)) >= 50 THEN 'High Risk'
        WHEN ((late_delivery_rate * 0.40) + (defect_rate * 8.00) + (avg_lead_time * 0.80) + (CASE WHEN total_spend > 200000 THEN 15 ELSE 5 END)) >= 30 THEN 'Medium Risk'
        ELSE 'Low Risk'
    END AS calculated_risk_level
FROM supplier_kpis
ORDER BY risk_score DESC;
