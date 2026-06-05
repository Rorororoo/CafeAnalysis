"""
analyze.py
----------
Loads CSV data into an in-memory SQLite database, runs all analysis queries,
prints results to the console, and saves charts to reports/.

Usage:
    python scripts/analyze.py
"""

import sqlite3
import csv
import os
import sys

# ── Optional matplotlib ────────────────────────────────────────────────────────
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.ticker as mticker
    PLOTS = True
except ImportError:
    PLOTS = False
    print("[INFO] matplotlib not installed – skipping charts (pip install matplotlib)")

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR  = os.path.join(BASE_DIR, "data")
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

# ── Load CSVs into SQLite ──────────────────────────────────────────────────────

def load_csv(conn: sqlite3.Connection, table: str, path: str):
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    if not rows:
        return
    cols = list(rows[0].keys())
    placeholders = ", ".join("?" for _ in cols)
    col_names    = ", ".join(cols)
    conn.executemany(
        f"INSERT OR IGNORE INTO {table} ({col_names}) VALUES ({placeholders})",
        [tuple(r[c] for c in cols) for r in rows],
    )
    conn.commit()
    print(f"  Loaded {len(rows):,} rows into '{table}'")


def build_db() -> sqlite3.Connection:
    schema = open(os.path.join(BASE_DIR, "sql", "01_schema.sql")).read()
    conn = sqlite3.connect(":memory:")
    conn.executescript(schema)
    load_csv(conn, "products",     os.path.join(DATA_DIR, "products.csv"))
    load_csv(conn, "transactions", os.path.join(DATA_DIR, "transactions.csv"))
    load_csv(conn, "order_items",  os.path.join(DATA_DIR, "order_items.csv"))
    return conn


# ── Pretty-print query results ─────────────────────────────────────────────────

def run(conn, sql: str, title: str = ""):
    cur = conn.execute(sql)
    rows = cur.fetchall()
    cols = [d[0] for d in cur.description]
    if title:
        print(f"\n{'='*60}")
        print(f"  {title}")
        print(f"{'='*60}")
    widths = [max(len(str(c)), max((len(str(r[i])) for r in rows), default=0))
              for i, c in enumerate(cols)]
    header = "  ".join(str(c).ljust(w) for c, w in zip(cols, widths))
    print(header)
    print("  ".join("-" * w for w in widths))
    for row in rows:
        print("  ".join(str(v).ljust(w) for v, w in zip(row, widths)))
    return rows, cols


# ── Chart helpers ──────────────────────────────────────────────────────────────

PALETTE = ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3",
           "#937860", "#DA8BC3", "#8C8C8C", "#CCB974", "#64B5CD"]

def bar_chart(labels, values, title, xlabel, ylabel, fname, color="#4C72B0", rotate=False):
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(labels, values, color=color, edgecolor="white", linewidth=0.6)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    for bar in bars:
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.01,
                f"{bar.get_height():,.0f}", ha="center", va="bottom", fontsize=8)
    if rotate:
        plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    path = os.path.join(REPORT_DIR, fname)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  → saved {path}")


def line_chart(labels, values, title, xlabel, ylabel, fname):
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(range(len(labels)), values, color="#4C72B0", linewidth=2, marker="o", markersize=3)
    ax.fill_between(range(len(labels)), values, alpha=0.15, color="#4C72B0")
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel(xlabel, fontsize=11)
    ax.set_ylabel(ylabel, fontsize=11)
    step = max(1, len(labels) // 12)
    ax.set_xticks(range(0, len(labels), step))
    ax.set_xticklabels([labels[i] for i in range(0, len(labels), step)], rotation=30, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
    plt.tight_layout()
    path = os.path.join(REPORT_DIR, fname)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  → saved {path}")


def grouped_bar(groups, series_labels, data_matrix, title, ylabel, fname):
    """data_matrix: list of value-lists, one per series."""
    x    = range(len(groups))
    w    = 0.35
    fig, ax = plt.subplots(figsize=(8, 5))
    for i, (label, vals) in enumerate(zip(series_labels, data_matrix)):
        offset = [xi + i * w - w / 2 for xi in x]
        ax.bar(offset, vals, w, label=label, color=PALETTE[i], edgecolor="white")
    ax.set_xticks([xi + w / 4 for xi in x])
    ax.set_xticklabels(groups)
    ax.set_title(title, fontsize=14, fontweight="bold", pad=12)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.legend()
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    plt.tight_layout()
    path = os.path.join(REPORT_DIR, fname)
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"  → saved {path}")


# ── Main analysis ──────────────────────────────────────────────────────────────

def main():
    print("\n📊  Building in-memory database …")
    conn = build_db()

    # 1. Overview
    run(conn, """
        SELECT COUNT(*) total_transactions,
               ROUND(SUM(total_amount),2) total_revenue,
               ROUND(AVG(total_amount),2) avg_transaction_value,
               MIN(DATE(timestamp)) first_date,
               MAX(DATE(timestamp)) last_date
        FROM transactions
    """, "1. DATASET OVERVIEW")

    # 2. Peak hours
    rows, _ = run(conn, """
        SELECT hour,
               COUNT(*) num_transactions,
               ROUND(SUM(total_amount),2) total_revenue
        FROM transactions
        GROUP BY hour ORDER BY hour
    """, "2. PEAK HOURS (by traffic)")

    if PLOTS and rows:
        hours  = [str(r[0]) + ":00" for r in rows]
        txns   = [r[1] for r in rows]
        rev    = [r[2] for r in rows]
        bar_chart(hours, txns,  "Transactions by Hour of Day", "Hour", "# Transactions",
                  "peak_hours_traffic.png", rotate=True)
        bar_chart(hours, rev,   "Revenue by Hour of Day", "Hour", "Revenue ($)",
                  "peak_hours_revenue.png", color="#DD8452", rotate=True)

    # 3. Top products
    run(conn, """
        SELECT oi.product_name, oi.category, COUNT(*) units_sold,
               ROUND(SUM(oi.price),2) total_revenue
        FROM order_items oi
        GROUP BY oi.product_id
        ORDER BY units_sold DESC LIMIT 10
    """, "3. TOP 10 PRODUCTS")

    # 4. Category performance
    rows, _ = run(conn, """
        SELECT category, COUNT(*) units_sold,
               ROUND(SUM(price),2) category_revenue
        FROM order_items
        GROUP BY category ORDER BY category_revenue DESC
    """, "4. CATEGORY PERFORMANCE")

    if PLOTS and rows:
        cats  = [r[0] for r in rows]
        revs  = [r[2] for r in rows]
        bar_chart(cats, revs, "Revenue by Category", "Category", "Revenue ($)",
                  "category_revenue.png", color="#55A868")

    # 5. Weekday vs Weekend
    rows, _ = run(conn, """
        SELECT CASE WHEN is_weekend=1 THEN 'Weekend' ELSE 'Weekday' END day_type,
               COUNT(*) num_transactions,
               ROUND(SUM(total_amount),2) total_revenue,
               ROUND(AVG(total_amount),2) avg_tx_value,
               ROUND(AVG(num_items),2)    avg_items
        FROM transactions GROUP BY is_weekend
    """, "5. WEEKDAY vs WEEKEND")

    if PLOTS and rows:
        types  = [r[0] for r in rows]
        tx_cnt = [r[1] for r in rows]
        rev    = [r[2] for r in rows]
        grouped_bar(
            types,
            ["Transactions", "Revenue ($)"],
            [tx_cnt, rev],
            "Weekday vs Weekend: Transactions & Revenue",
            "Count / Revenue ($)",
            "weekday_vs_weekend.png",
        )

    # 6. Day of week
    rows, _ = run(conn, """
        SELECT day_of_week,
               COUNT(*) num_transactions,
               ROUND(SUM(total_amount),2) total_revenue,
               ROUND(AVG(total_amount),2) avg_tx_value
        FROM transactions
        GROUP BY day_of_week
        ORDER BY CASE day_of_week
            WHEN 'Monday' THEN 1 WHEN 'Tuesday' THEN 2 WHEN 'Wednesday' THEN 3
            WHEN 'Thursday' THEN 4 WHEN 'Friday' THEN 5
            WHEN 'Saturday' THEN 6 WHEN 'Sunday' THEN 7 END
    """, "6. REVENUE BY DAY OF WEEK")

    if PLOTS and rows:
        days = [r[0][:3] for r in rows]
        rev  = [r[2] for r in rows]
        colors = ["#C44E52" if d in ("Sat","Sun") else "#4C72B0" for d in days]
        fig, ax = plt.subplots(figsize=(9, 5))
        bars = ax.bar(days, rev, color=colors, edgecolor="white")
        ax.set_title("Revenue by Day of Week  (red = weekend)", fontsize=14,
                     fontweight="bold", pad=12)
        ax.set_xlabel("Day"); ax.set_ylabel("Revenue ($)")
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
        for bar in bars:
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()*1.01,
                    f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=8)
        plt.tight_layout()
        plt.savefig(os.path.join(REPORT_DIR, "revenue_by_day.png"), dpi=150)
        plt.close()
        print(f"  → saved reports/revenue_by_day.png")

    # 7. Weekly trend
    rows, _ = run(conn, """
        SELECT STRFTIME('%Y-W%W', timestamp) year_week,
               ROUND(SUM(total_amount),2) weekly_revenue
        FROM transactions
        GROUP BY year_week ORDER BY year_week
    """, "7. WEEKLY REVENUE TREND")

    if PLOTS and rows:
        weeks = [r[0] for r in rows]
        wrev  = [r[1] for r in rows]
        line_chart(weeks, wrev, "Weekly Revenue Trend (2024)",
                   "Week", "Revenue ($)", "weekly_revenue_trend.png")

    # 8. Payment methods
    run(conn, """
        SELECT payment_method, COUNT(*) num_transactions,
               ROUND(100.0*COUNT()/(SELECT COUNT() FROM transactions),1) pct,
               ROUND(AVG(total_amount),2) avg_tx_value
        FROM transactions GROUP BY payment_method ORDER BY num_transactions DESC
    """, "8. PAYMENT METHOD MIX")

    # 9. Basket size
    run(conn, """
        SELECT num_items, COUNT(*) num_transactions,
               ROUND(100.0*COUNT()/(SELECT COUNT() FROM transactions),1) pct,
               ROUND(AVG(total_amount),2) avg_spend
        FROM transactions GROUP BY num_items ORDER BY num_items
    """, "9. BASKET SIZE DISTRIBUTION")

    print("\n✅  Analysis complete.  Charts saved to reports/\n")
    conn.close()


if __name__ == "__main__":
    main()
