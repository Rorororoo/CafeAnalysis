-- =============================================================
--  Local Café Performance Analysis
--  File: sql/02_analysis_queries.sql
--
--  Run each block independently in DB Browser for SQLite,
--  DBeaver, or via the Python analysis script.
-- =============================================================


-- ── 1. OVERVIEW STATS ──────────────────────────────────────────────────────────
-- Quick snapshot of the entire dataset.

SELECT
    COUNT(*)                              AS total_transactions,
    ROUND(SUM(total_amount), 2)           AS total_revenue,
    ROUND(AVG(total_amount), 2)           AS avg_transaction_value,
    ROUND(AVG(num_items),    2)           AS avg_items_per_transaction,
    MIN(DATE(timestamp))                  AS first_date,
    MAX(DATE(timestamp))                  AS last_date
FROM transactions;


-- ── 2. PEAK HOURS ──────────────────────────────────────────────────────────────
-- Identify which hours generate the most footfall and revenue.

SELECT
    hour,
    COUNT(*)                              AS num_transactions,
    ROUND(SUM(total_amount), 2)           AS total_revenue,
    ROUND(AVG(total_amount), 2)           AS avg_revenue_per_tx,
    ROUND(100.0 * COUNT(*) /
          (SELECT COUNT(*) FROM transactions), 1) AS pct_of_traffic
FROM transactions
GROUP BY hour
ORDER BY num_transactions DESC;


-- ── 3. TOP SELLING PRODUCTS ────────────────────────────────────────────────────
-- Most ordered items by units sold and total revenue contribution.

SELECT
    oi.product_name,
    oi.category,
    p.price                               AS unit_price,
    COUNT(*)                              AS units_sold,
    ROUND(SUM(oi.price), 2)              AS total_revenue,
    ROUND(100.0 * COUNT(*) /
          (SELECT COUNT(*) FROM order_items), 1) AS pct_of_orders
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY oi.product_id
ORDER BY units_sold DESC
LIMIT 10;


-- ── 4. CATEGORY PERFORMANCE ────────────────────────────────────────────────────
-- Revenue and unit share broken down by product category.

SELECT
    category,
    COUNT(*)                              AS units_sold,
    ROUND(SUM(price), 2)                 AS category_revenue,
    ROUND(AVG(price), 2)                 AS avg_item_price,
    ROUND(100.0 * SUM(price) /
          (SELECT SUM(price) FROM order_items), 1) AS revenue_share_pct
FROM order_items
GROUP BY category
ORDER BY category_revenue DESC;


-- ── 5. WEEKDAY vs WEEKEND REVENUE ──────────────────────────────────────────────
-- Core finding: weekend revenue premium.

SELECT
    CASE WHEN is_weekend = 1 THEN 'Weekend' ELSE 'Weekday' END AS day_type,
    COUNT(*)                              AS num_transactions,
    ROUND(SUM(total_amount), 2)           AS total_revenue,
    ROUND(AVG(total_amount), 2)           AS avg_transaction_value,
    ROUND(AVG(num_items),    2)           AS avg_items_per_tx
FROM transactions
GROUP BY is_weekend;


-- ── 6. REVENUE BY DAY OF WEEK ──────────────────────────────────────────────────
-- Granular day-level breakdown to confirm weekend pattern.

SELECT
    day_of_week,
    COUNT(*)                              AS num_transactions,
    ROUND(SUM(total_amount), 2)           AS total_revenue,
    ROUND(AVG(total_amount), 2)           AS avg_transaction_value
FROM transactions
GROUP BY day_of_week
ORDER BY
    CASE day_of_week
        WHEN 'Monday'    THEN 1 WHEN 'Tuesday'   THEN 2
        WHEN 'Wednesday' THEN 3 WHEN 'Thursday'  THEN 4
        WHEN 'Friday'    THEN 5 WHEN 'Saturday'  THEN 6
        WHEN 'Sunday'    THEN 7
    END;


-- ── 7. WEEKLY REVENUE TREND ────────────────────────────────────────────────────
-- Aggregate revenue by ISO week number to spot seasonal or growth trends.

SELECT
    STRFTIME('%Y-W%W', timestamp)         AS year_week,
    COUNT(*)                              AS num_transactions,
    ROUND(SUM(total_amount), 2)           AS weekly_revenue,
    ROUND(AVG(total_amount), 2)           AS avg_tx_value
FROM transactions
GROUP BY year_week
ORDER BY year_week;


-- ── 8. PAYMENT METHOD MIX ──────────────────────────────────────────────────────
-- Understand how customers pay (informs POS / contactless investment decisions).

SELECT
    payment_method,
    COUNT(*)                              AS num_transactions,
    ROUND(100.0 * COUNT(*) /
          (SELECT COUNT(*) FROM transactions), 1) AS pct_of_transactions,
    ROUND(AVG(total_amount), 2)           AS avg_transaction_value
FROM transactions
GROUP BY payment_method
ORDER BY num_transactions DESC;


-- ── 9. ORDERING PATTERN: ITEMS PER TRANSACTION ─────────────────────────────────
-- Shows whether upsell / combo deals could increase basket size.

SELECT
    num_items,
    COUNT(*)                              AS num_transactions,
    ROUND(100.0 * COUNT(*) /
          (SELECT COUNT(*) FROM transactions), 1) AS pct_of_transactions,
    ROUND(AVG(total_amount), 2)           AS avg_spend
FROM transactions
GROUP BY num_items
ORDER BY num_items;


-- ── 10. TOP PRODUCTS ON WEEKENDS ───────────────────────────────────────────────
-- Which products drive the weekend revenue premium?

SELECT
    oi.product_name,
    oi.category,
    COUNT(*)                              AS weekend_units_sold,
    ROUND(SUM(oi.price), 2)             AS weekend_revenue
FROM order_items oi
JOIN transactions t ON oi.transaction_id = t.transaction_id
WHERE t.is_weekend = 1
GROUP BY oi.product_id
ORDER BY weekend_units_sold DESC
LIMIT 10;


-- ── 11. MONTHLY REVENUE SUMMARY ────────────────────────────────────────────────
-- Year-over-month revenue to identify seasonal highs / lows.

SELECT
    STRFTIME('%Y-%m', timestamp)          AS month,
    COUNT(*)                              AS num_transactions,
    ROUND(SUM(total_amount), 2)           AS monthly_revenue,
    ROUND(AVG(total_amount), 2)           AS avg_tx_value
FROM transactions
GROUP BY month
ORDER BY month;
