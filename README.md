# AI Supply Chain Control Tower Agent using GPT-5.5, PostgreSQL, Python, and Streamlit

## Project Overview

This project is a GenAI-powered supply chain analytics assistant that helps business users ask natural-language questions about supplier risk, procurement spend, delivery delays, inventory exposure, and stockout risk.

The project combines **GPT-5.5**, **Python**, **PostgreSQL**, **SQL**, **Streamlit**, and **Power BI-ready datasets** to simulate a modern supply chain control tower.

## Business Problem

Supply chain teams often depend on disconnected ERP extracts, Excel files, supplier scorecards, and dashboards. This creates delays in identifying high-risk suppliers, late shipments, stockout exposure, and procurement cost-saving opportunities.

This project solves that problem by creating an AI assistant that can answer questions like:

- Which suppliers are high risk this month?
- Which products may face stockout?
- Why did delivery performance drop?
- What are the top procurement spend drivers?
- Draft an email to a supplier about repeated late deliveries.

## Key Features

- AI-powered natural-language supply chain Q&A
- Supplier risk scoring using late delivery, defect rate, lead time, and spend concentration
- Inventory stockout risk classification
- Procurement spend analysis
- Executive KPI summary generation
- Supplier communication draft generation
- PostgreSQL database schema and SQL KPI queries
- Streamlit chatbot interface
- Power BI-ready CSV dataset

## Tools and Technologies

| Area | Tools |
|---|---|
| AI Agent | GPT-5.5 / OpenAI API |
| Programming | Python, Pandas |
| Database | PostgreSQL |
| SQL Analysis | Supplier KPIs, procurement spend, inventory risk |
| Web App | Streamlit |
| Dashboarding | Power BI-ready data |
| Version Control | GitHub |

## Project Structure

```text
AI-Supply-Chain-Control-Tower-Agent/
│
├── app/
│   └── streamlit_app.py
│
├── data/
│   ├── raw_supply_chain_data.csv
│   └── cleaned_supply_chain_data.csv
│
├── docs/
│   └── PROJECT_SUMMARY.md
│
├── prompts/
│   └── agent_prompts.md
│
├── sql/
│   ├── 01_create_tables.sql
│   ├── 02_load_data.sql
│   └── 03_kpi_queries.sql
│
├── src/
│   ├── ai_agent.py
│   ├── config.py
│   ├── db.py
│   ├── kpi_engine.py
│   └── load_to_postgres.py
│
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Dataset

The sample dataset includes **250 synthetic purchase order records** with supplier, inventory, delivery, quality, and procurement spend fields.

### Main Columns

- PO_ID
- Supplier_ID
- Supplier_Name
- Product_ID
- Product_Name
- Category
- Region
- Country
- PO_Date
- Expected_Delivery_Date
- Actual_Delivery_Date
- Quantity_Ordered
- Quantity_Received
- Inventory_Level
- Forecasted_Demand
- Reorder_Point
- PO_Value
- Defective_Units
- Lead_Time_Days
- Delivery_Status

## PostgreSQL Data Model

The PostgreSQL schema includes four main tables:

- suppliers
- products
- inventory
- purchase_orders

## Example SQL Analysis

The SQL folder includes queries for:

- Supplier late delivery rate
- Supplier defect rate
- Monthly procurement spend
- Top high-spend suppliers
- Inventory stockout risk
- Supplier risk score classification

## How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/your-username/AI-Supply-Chain-Control-Tower-Agent.git
cd AI-Supply-Chain-Control-Tower-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate
```

For Mac/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create environment file

Copy `.env.example` and rename it to `.env`.

```text
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-5.5
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/supply_chain_ai
```

Do not upload your real `.env` file to GitHub.

### 5. Run Streamlit app

```bash
streamlit run app/streamlit_app.py
```

The project also works without an API key using the built-in offline KPI engine.

## PostgreSQL Setup

Create a local PostgreSQL database:

```sql
CREATE DATABASE supply_chain_ai;
```

Run the schema file:

```bash
psql -U postgres -d supply_chain_ai -f sql/01_create_tables.sql
```

Then load the dataset using:

```bash
python -m src.load_to_postgres
```

## Example AI Questions

```text
Which suppliers are high risk and why?
Which products have stockout risk?
Give me an executive summary of supply chain performance.
Draft an email to a supplier with repeated late deliveries.
What procurement cost-saving opportunities should leadership review?
```

## Business Impact

This project demonstrates how GenAI can improve supply chain visibility by converting supplier, procurement, inventory, and delivery data into business-ready recommendations.

Potential benefits:

- Faster supplier risk identification
- Better stockout visibility
- Improved procurement spend monitoring
- Stronger executive reporting
- Faster business communication
- More proactive supply chain decision-making

## Resume Bullet Points

```text
Developed an AI-powered Supply Chain Control Tower Agent using Python, PostgreSQL, SQL, Streamlit, Power BI-ready datasets, and GPT-5.5 to analyze supplier risk, procurement spend, late deliveries, inventory exposure, and stockout risk through natural-language business queries.
```

```text
Designed PostgreSQL tables and SQL KPI queries to calculate late delivery rate, defect rate, procurement spend, supplier risk score, and inventory stockout exposure; integrated outputs into a GenAI-enabled Streamlit assistant for executive decision support.
```

## LinkedIn Project Title

```text
AI Supply Chain Control Tower Agent | GPT-5.5 + PostgreSQL + Python + Streamlit
```
