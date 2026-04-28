import pandas as pd
from sqlalchemy import text
from .db import get_engine
from .config import DATA_PATH


def main():
    df = pd.read_csv(DATA_PATH)
    engine = get_engine()

    with engine.begin() as conn:
        schema_sql = open("sql/01_create_tables.sql", encoding="utf-8").read()
        conn.execute(text(schema_sql))

        suppliers = df[["supplier_id", "supplier_name", "country", "category", "base_risk_level"]].drop_duplicates("supplier_id")
        products = df[["product_id", "product_name", "category", "region"]].drop_duplicates("product_id")
        inventory = df.sort_values("po_date").drop_duplicates("product_id", keep="last")[[
            "product_id", "inventory_level", "forecasted_demand", "reorder_point"
        ]]
        purchase_orders = df[[
            "po_id", "supplier_id", "product_id", "po_date", "expected_delivery_date", "actual_delivery_date",
            "quantity_ordered", "quantity_received", "po_value", "defective_units", "lead_time_days", "delivery_status"
        ]]

        suppliers.to_sql("suppliers", conn, if_exists="append", index=False)
        products.to_sql("products", conn, if_exists="append", index=False)
        inventory.to_sql("inventory", conn, if_exists="append", index=False)
        purchase_orders.to_sql("purchase_orders", conn, if_exists="append", index=False)

    print("Loaded data into PostgreSQL successfully.")


if __name__ == "__main__":
    main()
