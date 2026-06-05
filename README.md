# ☕ Local Café Performance Analysis

> **Tools:** Python · SQLite · SQL · Google Sheets-compatible CSV · matplotlib

A data analysis project that examines 2,000+ café point-of-sale transactions to surface insights on peak trading hours, top-selling products, category revenue share, and — the headline finding — a **~27% higher average spend per weekend visit** compared to weekdays.

---

##  Project Overview

| Item | Detail |
|---|---|
| Dataset | 2,200 transactions · 4,191 line items · 20 products |
| Period | 1 Jan 2024 – 31 Dec 2024 |
| Total Revenue | $18,802 |
| Avg Transaction | $8.55 (weekday $7.96 · weekend $10.08) |

The analysis answers three business questions:
1. **When** is the café busiest — and which hours are under-served?
2. **What** sells best by units and by revenue contribution?
3. **Why** does weekend revenue per visit outperform weekdays, and how can that gap be widened?

---

##  Repository Structure

```
cafe-analysis/
├── data/
│   ├── transactions.csv       # 2,200 transaction records
│   ├── order_items.csv        # 4,191 individual line items
│   └── products.csv           # 20-item product catalogue
│
├── sql/
│   ├── 01_schema.sql          # Table definitions + indexes
│   └── 02_analysis_queries.sql # 11 analysis queries (standalone)
│
├── scripts/
│   ├── generate_data.py       # Generates realistic synthetic data
│   ├── analyze.py             # Runs all SQL queries + saves charts
│   └── build_report.js        # Generates the Word (.docx) report
│
├── reports/
│   ├── peak_hours_traffic.png
│   ├── peak_hours_revenue.png
│   ├── category_revenue.png
│   ├── weekday_vs_weekend.png
│   ├── revenue_by_day.png
│   └── weekly_revenue_trend.png
│
└── README.md
```

---

##  Quick Start

### 1. Clone & Install

```bash
git clone https://github.com/YOUR_USERNAME/cafe-analysis.git
cd cafe-analysis

# Python dependencies
pip install matplotlib

# Node dependency (only needed to rebuild the Word report)
npm install -g docx
```

### 2. Generate the Data

```bash
python scripts/generate_data.py
```

Creates `data/transactions.csv`, `data/order_items.csv`, and `data/products.csv`.

### 3. Run the Full Analysis

```bash
python scripts/analyze.py
```

- Loads CSV data into an in-memory SQLite database
- Runs 11 SQL queries and prints results to the terminal
- Saves 6 charts to `reports/`

### 4. (Optional) Rebuild the Word Report

```bash
node scripts/build_report.js
```

Regenerates `reports/Cafe_Performance_Analysis_Report.docx`.

---

##  SQL Queries Included

| # | Query | Purpose |
|---|---|---|
| 1 | Overview Stats | Total revenue, avg transaction, date range |
| 2 | Peak Hours | Traffic and revenue by hour of day |
| 3 | Top 10 Products | Best sellers by units and revenue |
| 4 | Category Performance | Revenue share by product category |
| 5 | Weekday vs Weekend | Core revenue comparison |
| 6 | Day of Week | Granular daily breakdown |
| 7 | Weekly Trend | 52-week revenue trend line |
| 8 | Payment Methods | Card / Cash / Mobile Pay split |
| 9 | Basket Size | Distribution of items per transaction |
| 10 | Weekend Top Products | What drives weekend revenue |
| 11 | Monthly Summary | Month-by-month revenue |

All queries are in `sql/02_analysis_queries.sql` and can be run independently in **DB Browser for SQLite**, **DBeaver**, or any SQL client.

---

##  Key Findings

###  Peak Hours
The **8–10 AM morning rush** generates **34% of all daily transactions**. A secondary lunchtime peak occurs at 12–13 PM (~22% of traffic). After 15:00, footfall drops steeply.

###  Top Products
| Rank | Product | Units | Revenue |
|---|---|---|---|
| 1 | Latte | 408 | $1,836 |
| 2 | Espresso | 326 | $815 |
| 3 | Americano | 312 | $936 |
| 4 | Croissant | 306 | $918 |
| 5 | Avocado Toast | 225 | $1,912 |

**Avocado Toast** ranks 8th by units but 2nd by revenue — the highest revenue-per-unit of any item.

###  Weekend Revenue Opportunity
| Day Type | Transactions | Total Revenue | Avg Spend |
|---|---|---|---|
| Weekday | 1,589 | $12,642 | $7.96 |
| **Weekend** | **611** | **$6,160** | **$10.08** |

Weekend visitors spend **~27% more per transaction** and buy **2.25 items vs 1.77 on weekdays**. Focused weekend programming (brunch menus, combos, extended hours) could materially increase annual revenue.

###  Payment Mix
- Card: 59% of transactions
- Cash: 25%
- Mobile Pay: 16% (growing)

---

##  Recommendations

1. **Staff up for 07:45 AM** — the 8–10 window drives a third of daily revenue
2. **Introduce a Morning Combo** (coffee + pastry) to increase basket size
3. **Build a weekend brunch menu** — customers already spend more; give them more to buy
4. **Expand the Food category** — only 5 SKUs but 36% of total revenue
5. **Invest in contactless payment** — 75% of customers pay digitally

---

##  Tech Stack

| Tool | Use |
|---|---|
| **Python 3** | Data generation, SQLite integration, chart output |
| **SQLite (in-memory)** | Relational query engine — no server required |
| **SQL** | All analytical queries |
| **matplotlib** | Charts and visualisations |
| **Node.js + docx** | Word report generation |
| **CSV / Google Sheets** | Data storage format (Sheets-compatible) |

---

## 📄 License

MIT — free to use, adapt, and include in your own portfolio.
