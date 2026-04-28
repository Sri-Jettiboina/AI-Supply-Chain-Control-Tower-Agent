import pandas as pd
from .db import load_csv


def get_kpi_summary(df: pd.DataFrame | None = None) -> dict:
    """Return core supply chain KPIs from the CSV dataset."""
    if df is None:
        df = load_csv()

    total_spend = float(df["po_value"].sum())
    total_orders = int(df["po_id"].nunique())
    late_rate = round((df["delivery_status"].eq("Late").mean()) * 100, 2)
    defect_rate = round((df["defective_units"].sum() / max(df["quantity_received"].sum(), 1)) * 100, 2)
    avg_lead_time = round(df["lead_time_days"].mean(), 2)
    stockout_risk_count = int((df["inventory_level"] < df["reorder_point"]).sum())

    return {
        "total_spend": round(total_spend, 2),
        "total_orders": total_orders,
        "late_delivery_rate_pct": late_rate,
        "defect_rate_pct": defect_rate,
        "avg_lead_time_days": avg_lead_time,
        "stockout_risk_records": stockout_risk_count,
    }


def supplier_risk_table(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Calculate supplier KPI table and risk level."""
    if df is None:
        df = load_csv()

    grouped = df.groupby(["supplier_id", "supplier_name", "country", "category"], as_index=False).agg(
        total_orders=("po_id", "nunique"),
        late_orders=("delivery_status", lambda s: (s == "Late").sum()),
        total_spend=("po_value", "sum"),
        avg_lead_time=("lead_time_days", "mean"),
        defective_units=("defective_units", "sum"),
        quantity_received=("quantity_received", "sum"),
    )

    grouped["late_delivery_rate"] = (grouped["late_orders"] / grouped["total_orders"] * 100).round(2)
    grouped["defect_rate"] = (grouped["defective_units"] / grouped["quantity_received"].replace(0, 1) * 100).round(2)
    grouped["avg_lead_time"] = grouped["avg_lead_time"].round(2)

    grouped["risk_score"] = (
        grouped["late_delivery_rate"] * 0.40 +
        grouped["defect_rate"] * 8.00 +
        grouped["avg_lead_time"] * 0.80 +
        grouped["total_spend"].apply(lambda x: 15 if x > 200000 else 5)
    ).round(2)

    def classify(score: float) -> str:
        if score >= 70:
            return "Critical Risk"
        if score >= 50:
            return "High Risk"
        if score >= 30:
            return "Medium Risk"
        return "Low Risk"

    grouped["calculated_risk_level"] = grouped["risk_score"].apply(classify)
    return grouped.sort_values("risk_score", ascending=False)


def stockout_risk_table(df: pd.DataFrame | None = None) -> pd.DataFrame:
    """Find products where inventory is below reorder point or forecasted demand."""
    if df is None:
        df = load_csv()

    product = df.sort_values("po_date").groupby(
        ["product_id", "product_name", "category", "region"],
        as_index=False
    ).tail(1)

    product = product[[
        "product_id", "product_name", "category", "region",
        "inventory_level", "forecasted_demand", "reorder_point"
    ]].copy()

    def classify(row):
        if row["inventory_level"] < row["reorder_point"]:
            return "High Stockout Risk"
        if row["inventory_level"] < row["forecasted_demand"]:
            return "Medium Stockout Risk"
        return "Low Risk"

    product["stockout_risk"] = product.apply(classify, axis=1)
    return product.sort_values(["stockout_risk", "forecasted_demand"], ascending=[True, False])


def monthly_spend(df: pd.DataFrame | None = None) -> pd.DataFrame:
    if df is None:
        df = load_csv()
    df = df.copy()
    df["month"] = pd.to_datetime(df["po_date"]).dt.to_period("M").astype(str)
    return df.groupby("month", as_index=False).agg(total_spend=("po_value", "sum")).sort_values("month")
