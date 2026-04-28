from __future__ import annotations

import json
from typing import Any
from .config import OPENAI_API_KEY, OPENAI_MODEL
from .kpi_engine import get_kpi_summary, supplier_risk_table, stockout_risk_table

SYSTEM_PROMPT = """
You are an AI Supply Chain Control Tower Agent.
Answer like a supply chain analytics manager: concise, business-friendly, KPI-driven, and action-oriented.
Use the provided data context only. If the user asks for something not covered by the data, say what additional data is needed.
""".strip()


def build_context() -> dict[str, Any]:
    """Build a compact context package for the model."""
    supplier_risk = supplier_risk_table().head(8)
    stockout_risk = stockout_risk_table().head(8)

    return {
        "kpi_summary": get_kpi_summary(),
        "top_supplier_risks": supplier_risk.to_dict(orient="records"),
        "top_stockout_risks": stockout_risk.to_dict(orient="records"),
    }


def offline_response(question: str) -> str:
    """Fallback when no OpenAI API key is available."""
    context = build_context()
    q = question.lower()

    if "supplier" in q or "risk" in q:
        rows = context["top_supplier_risks"][:5]
        lines = ["### Top Supplier Risks"]
        for r in rows:
            lines.append(
                f"- **{r['supplier_name']}**: {r['calculated_risk_level']} | "
                f"Risk Score {r['risk_score']} | Late Delivery {r['late_delivery_rate']}% | "
                f"Defect Rate {r['defect_rate']}% | Avg Lead Time {r['avg_lead_time']} days"
            )
        lines.append("\n**Recommended action:** Review late-delivery root causes, confirm recovery plans, and identify backup suppliers for high-risk categories.")
        return "\n".join(lines)

    if "stockout" in q or "inventory" in q:
        rows = context["top_stockout_risks"][:5]
        lines = ["### Inventory Exposure Summary"]
        for r in rows:
            lines.append(
                f"- **{r['product_name']}** ({r['region']}): {r['stockout_risk']} | "
                f"Inventory {r['inventory_level']} | Forecasted Demand {r['forecasted_demand']} | Reorder Point {r['reorder_point']}"
            )
        lines.append("\n**Recommended action:** Expedite replenishment, validate demand forecast, and prioritize products below reorder point.")
        return "\n".join(lines)

    if "email" in q or "draft" in q:
        return """### Supplier Email Draft

**Subject:** Follow-up on Repeated Delivery Delays

Hi Supplier Team,

I wanted to follow up regarding repeated late deliveries observed in recent purchase orders. These delays are creating planning risk, inventory exposure, and service-level concerns for our operations team.

Could you please share the root cause, recovery timeline, and corrective action plan for upcoming shipments?

Thank you,  
Supply Chain Operations Team"""

    k = context["kpi_summary"]
    return (
        "### Executive KPI Summary\n"
        f"- **Total Spend:** ${k['total_spend']:,.2f}\n"
        f"- **Total Orders:** {k['total_orders']}\n"
        f"- **Late Delivery Rate:** {k['late_delivery_rate_pct']}%\n"
        f"- **Defect Rate:** {k['defect_rate_pct']}%\n"
        f"- **Average Lead Time:** {k['avg_lead_time_days']} days\n"
        f"- **High Stockout Risk Records:** {k['stockout_risk_records']}\n\n"
        "**Recommended action:** Focus leadership review on suppliers with high late-delivery rates, products below reorder point, and categories with concentrated spend."
    )


def ask_agent(question: str) -> str:
    """Ask GPT-5.5 using the OpenAI Responses API. Falls back to local logic without a key."""
    if not OPENAI_API_KEY:
        return offline_response(question)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=OPENAI_API_KEY)
        context = build_context()

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": f"Data context:\n{json.dumps(context, default=str)}\n\nQuestion: {question}",
                },
            ],
        )
        return response.output_text

    except Exception as exc:
        return (
            "The AI API call failed, so I used the offline KPI engine instead.\n\n"
            f"Technical note: {exc}\n\n"
            + offline_response(question)
        )
