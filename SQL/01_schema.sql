-- =============================================================
--  Local Café Performance Analysis
--  File: sql/01_schema.sql
--  Creates the three core tables used throughout the analysis.
-- =============================================================

CREATE TABLE IF NOT EXISTS products (
    product_id   INTEGER PRIMARY KEY,
    name         TEXT    NOT NULL,
    category     TEXT    NOT NULL,
    price        REAL    NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id  INTEGER PRIMARY KEY,
    timestamp       TEXT    NOT NULL,          -- 'YYYY-MM-DD HH:MM:SS'
    day_of_week     TEXT    NOT NULL,
    is_weekend      INTEGER NOT NULL DEFAULT 0, -- 0 = weekday, 1 = weekend
    hour            INTEGER NOT NULL,
    total_amount    REAL    NOT NULL,
    num_items       INTEGER NOT NULL,
    payment_method  TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id         INTEGER PRIMARY KEY,
    transaction_id  INTEGER NOT NULL REFERENCES transactions(transaction_id),
    product_id      INTEGER NOT NULL REFERENCES products(product_id),
    product_name    TEXT    NOT NULL,
    category        TEXT    NOT NULL,
    price           REAL    NOT NULL
);

-- Indexes for common filter patterns
CREATE INDEX IF NOT EXISTS idx_tx_timestamp   ON transactions(timestamp);
CREATE INDEX IF NOT EXISTS idx_tx_is_weekend  ON transactions(is_weekend);
CREATE INDEX IF NOT EXISTS idx_tx_hour        ON transactions(hour);
CREATE INDEX IF NOT EXISTS idx_oi_product     ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_oi_category    ON order_items(category);
