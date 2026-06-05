"""
generate_data.py
----------------
Generates 2,000+ realistic café transaction records and saves them
to data/transactions.csv and data/products.csv.
"""

import csv
import random
from datetime import datetime, timedelta

random.seed(42)

# ── Products catalogue ─────────────────────────────────────────────────────────
PRODUCTS = [
    {"product_id": 1,  "name": "Espresso",          "category": "Coffee",     "price": 2.50},
    {"product_id": 2,  "name": "Americano",          "category": "Coffee",     "price": 3.00},
    {"product_id": 3,  "name": "Cappuccino",         "category": "Coffee",     "price": 4.00},
    {"product_id": 4,  "name": "Latte",              "category": "Coffee",     "price": 4.50},
    {"product_id": 5,  "name": "Flat White",         "category": "Coffee",     "price": 4.00},
    {"product_id": 6,  "name": "Mocha",              "category": "Coffee",     "price": 4.75},
    {"product_id": 7,  "name": "Cold Brew",          "category": "Coffee",     "price": 4.50},
    {"product_id": 8,  "name": "Green Tea",          "category": "Tea",        "price": 2.75},
    {"product_id": 9,  "name": "Chai Latte",         "category": "Tea",        "price": 4.00},
    {"product_id": 10, "name": "Herbal Infusion",    "category": "Tea",        "price": 2.75},
    {"product_id": 11, "name": "Fresh OJ",           "category": "Cold Drink", "price": 3.50},
    {"product_id": 12, "name": "Smoothie",           "category": "Cold Drink", "price": 5.00},
    {"product_id": 13, "name": "Croissant",          "category": "Pastry",     "price": 3.00},
    {"product_id": 14, "name": "Blueberry Muffin",   "category": "Pastry",     "price": 3.25},
    {"product_id": 15, "name": "Banana Bread",       "category": "Pastry",     "price": 3.50},
    {"product_id": 16, "name": "Avocado Toast",      "category": "Food",       "price": 8.50},
    {"product_id": 17, "name": "Bagel & Cream Cheese","category": "Food",      "price": 5.50},
    {"product_id": 18, "name": "Granola Bowl",       "category": "Food",       "price": 7.00},
    {"product_id": 19, "name": "Club Sandwich",      "category": "Food",       "price": 9.00},
    {"product_id": 20, "name": "Caesar Salad",       "category": "Food",       "price": 8.00},
]

# ── Weighted popularity (higher weight = more popular) ─────────────────────────
WEIGHTS = [15, 12, 14, 18, 10, 8, 9, 6, 7, 4, 5, 5, 12, 10, 8, 9, 8, 6, 7, 6]

# ── Hour-of-day traffic distribution ──────────────────────────────────────────
# Key: hour (0-23), Value: relative weight
HOUR_WEIGHTS = {
    6: 2, 7: 8, 8: 18, 9: 20, 10: 14, 11: 12, 12: 16,
    13: 14, 14: 10, 15: 9, 16: 8, 17: 6, 18: 4, 19: 2, 20: 1,
}
HOURS = list(HOUR_WEIGHTS.keys())
HOUR_W = list(HOUR_WEIGHTS.values())

# Weekend hours skew slightly later
WEEKEND_HOUR_WEIGHTS = {
    8: 4, 9: 10, 10: 18, 11: 20, 12: 18, 13: 16, 14: 14,
    15: 12, 16: 10, 17: 8, 18: 6, 19: 4, 20: 2,
}
W_HOURS = list(WEEKEND_HOUR_WEIGHTS.keys())
W_HOUR_W = list(WEEKEND_HOUR_WEIGHTS.values())

PAYMENT_METHODS = ["Card", "Cash", "Mobile Pay"]
PAYMENT_WEIGHTS = [60, 25, 15]

START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 12, 31)


def random_timestamp(is_weekend: bool) -> datetime:
    delta = (END_DATE - START_DATE).days
    day = START_DATE + timedelta(days=random.randint(0, delta))
    if is_weekend:
        hour   = random.choices(W_HOURS, weights=W_HOUR_W)[0]
    else:
        hour   = random.choices(HOURS,   weights=HOUR_W)[0]
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return day.replace(hour=hour, minute=minute, second=second)


def generate_transactions(n: int = 2200):
    transactions = []
    items_rows   = []
    transaction_id = 1
    item_id        = 1

    for _ in range(n):
        ts         = START_DATE + timedelta(days=random.randint(0, (END_DATE - START_DATE).days))
        is_weekend = ts.weekday() >= 5
        ts         = random_timestamp(is_weekend)

        # Weekend bump: ~40 % more revenue per transaction on average
        num_items  = random.choices([1, 2, 3, 4], weights=[50, 30, 15, 5])[0]
        if is_weekend:
            num_items = random.choices([1, 2, 3, 4, 5], weights=[35, 30, 20, 10, 5])[0]

        chosen = random.choices(PRODUCTS, weights=WEIGHTS, k=num_items)
        total  = round(sum(p["price"] for p in chosen), 2)
        method = random.choices(PAYMENT_METHODS, weights=PAYMENT_WEIGHTS)[0]

        transactions.append({
            "transaction_id": transaction_id,
            "timestamp":      ts.strftime("%Y-%m-%d %H:%M:%S"),
            "day_of_week":    ts.strftime("%A"),
            "is_weekend":     int(is_weekend),
            "hour":           ts.hour,
            "total_amount":   total,
            "num_items":      num_items,
            "payment_method": method,
        })

        for p in chosen:
            items_rows.append({
                "item_id":        item_id,
                "transaction_id": transaction_id,
                "product_id":     p["product_id"],
                "product_name":   p["name"],
                "category":       p["category"],
                "price":          p["price"],
            })
            item_id += 1

        transaction_id += 1

    return transactions, items_rows


def write_csv(path: str, rows: list, fieldnames: list):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  Wrote {len(rows):,} rows → {path}")


if __name__ == "__main__":
    print("Generating café transaction data …")
    transactions, items = generate_transactions(2200)

    write_csv(
        "data/transactions.csv", transactions,
        ["transaction_id","timestamp","day_of_week","is_weekend",
         "hour","total_amount","num_items","payment_method"],
    )
    write_csv(
        "data/order_items.csv", items,
        ["item_id","transaction_id","product_id","product_name","category","price"],
    )

    products_rows = PRODUCTS
    write_csv(
        "data/products.csv", products_rows,
        ["product_id","name","category","price"],
    )

    print(f"\nDone! {len(transactions):,} transactions, {len(items):,} line items.")
