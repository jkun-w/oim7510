import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(r"""
    # Babson Bean Café — Generating the Data

    This notebook makes up a café's worth of loyalty members, menu items, drink
    options, orders and payments, shaped like the tables in `README.md`, and writes
    each one to a CSV file in `projects/db/data/`. `build.py` reads those CSV files
    to make the database.
    """)
    return


@app.cell
def _():
    import csv
    import os
    import random
    from datetime import date, datetime, timedelta

    from faker import Faker

    return Faker, csv, date, datetime, os, random, timedelta


@app.cell
def _(Faker, random):
    # A fixed seed means re-running this notebook makes the exact same data every time.
    random.seed(42)
    fake = Faker()
    Faker.seed(42)
    return (fake,)


@app.cell
def _(date):
    # The data behaves as if "today" is this date, so "last month" and "the last 60
    # days" mean the same thing every time this notebook, or build.py, is run.
    TODAY = date(2026, 11, 1)
    return (TODAY,)


@app.cell
def _(os):
    # __file__ is this notebook's own path, so the data folder is found no matter
    # which folder the terminal was opened in.
    DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
    os.makedirs(DATA_DIR, exist_ok=True)
    return (DATA_DIR,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Loyalty members
    """)
    return


@app.cell
def _(DATA_DIR, TODAY, csv, fake, os, random, timedelta):
    MEMBER_COUNT = 50

    members = []
    for _member_id in range(1, MEMBER_COUNT + 1):
        first_name = fake.first_name()
        mobile_number = fake.numerify("617-###-####")
        if random.random() < 0.8:
            email = fake.unique.email()
        else:
            email = ""
        days_since_joining = random.randint(30, 720)
        join_date = TODAY - timedelta(days=days_since_joining)
        points_balance = random.randint(0, 500)
        members.append(
            {
                "member_id": _member_id,
                "first_name": first_name,
                "mobile_number": mobile_number,
                "email": email,
                "join_date": join_date.isoformat(),
                "points_balance": points_balance,
            }
        )

    with open(os.path.join(DATA_DIR, "members.csv"), "w", newline="", encoding="utf-8") as _f:
        _writer = csv.DictWriter(_f, fieldnames=list(members[0].keys()))
        _writer.writeheader()
        for _row in members:
            _writer.writerow(_row)

    len(members)
    return (members,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Menu
    """)
    return


@app.cell
def _(DATA_DIR, csv, os):
    # name, category, price, cost
    PRODUCT_CATALOG = [
        ("Drip Coffee", "coffee", 2.75, 0.60),
        ("Americano", "coffee", 3.25, 0.65),
        ("Latte", "coffee", 4.50, 1.10),
        ("Cappuccino", "coffee", 4.50, 1.10),
        ("Cold Brew", "coffee", 4.00, 0.90),
        ("Espresso", "coffee", 2.50, 0.55),
        ("Mocha", "coffee", 4.75, 1.20),
        ("Flat White", "coffee", 4.50, 1.05),
        ("Green Tea", "tea", 3.00, 0.50),
        ("Black Tea", "tea", 3.00, 0.50),
        ("Chai Latte", "tea", 4.25, 1.00),
        ("Matcha Latte", "tea", 4.75, 1.30),
        ("Herbal Tea", "tea", 3.00, 0.50),
        ("Iced Tea", "tea", 3.25, 0.55),
        ("Bagel", "food", 2.50, 0.80),
        ("Blueberry Muffin", "food", 3.25, 1.00),
        ("Croissant", "food", 3.50, 1.05),
        ("Avocado Toast", "food", 6.50, 2.20),
        ("Breakfast Sandwich", "food", 5.75, 2.00),
        ("Chocolate Chip Cookie", "food", 2.25, 0.60),
        ("Banana Bread", "food", 3.00, 0.90),
        ("Granola Bar", "food", 2.00, 0.70),
        ("Bottled Water", "other", 2.00, 0.40),
        ("Orange Juice", "other", 3.25, 1.00),
        ("Babson Bean Mug", "other", 12.00, 5.00),
        ("Babson Bean Tote Bag", "other", 10.00, 4.00),
    ]

    # these two items are off the menu today, but they were sold in the past
    UNAVAILABLE_PRODUCTS = {"Herbal Tea", "Granola Bar"}

    products = []
    for product_index in range(len(PRODUCT_CATALOG)):
        _name, _category, _price, _cost = PRODUCT_CATALOG[product_index]
        products.append(
            {
                "product_id": product_index + 1,
                "name": _name,
                "category": _category,
                "price": _price,
                "cost": _cost,
                "is_available": _name not in UNAVAILABLE_PRODUCTS,
            }
        )

    with open(os.path.join(DATA_DIR, "products.csv"), "w", newline="", encoding="utf-8") as _f:
        _writer = csv.DictWriter(_f, fieldnames=list(products[0].keys()))
        _writer.writeheader()
        for _row in products:
            _writer.writerow(_row)

    len(products)
    return (products,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Options a drink can carry
    """)
    return


@app.cell
def _(DATA_DIR, csv, os):
    # name, price, cost
    OPTION_CATALOG = [
        ("Extra Shot", 0.75, 0.20),
        ("Oat Milk", 0.65, 0.30),
        ("Almond Milk", 0.65, 0.28),
        ("Soy Milk", 0.60, 0.25),
        ("Vanilla Syrup", 0.50, 0.10),
        ("Caramel Syrup", 0.50, 0.10),
        ("Whipped Cream", 0.50, 0.15),
        ("Decaf", 0.00, 0.00),
    ]

    options = []
    for option_index in range(len(OPTION_CATALOG)):
        _name, _price, _cost = OPTION_CATALOG[option_index]
        options.append(
            {
                "option_id": option_index + 1,
                "name": _name,
                "price": _price,
                "cost": _cost,
            }
        )

    with open(os.path.join(DATA_DIR, "options.csv"), "w", newline="", encoding="utf-8") as _f:
        _writer = csv.DictWriter(_f, fieldnames=list(options[0].keys()))
        _writer.writeheader()
        for _row in options:
            _writer.writerow(_row)

    len(options)
    return (options,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Orders, their lines and options, and their payments

    A handful of members (the first 8) are left out of every order below, so there
    are loyalty members who joined and never ordered. Exactly two orders also get a
    payment that no longer matches their total — broken on purpose, so the
    payments-vs-total check has something real to find. The data covers the 12
    months up to `TODAY`, the `as_of` date Part B uses.
    """)
    return


@app.cell
def _():
    # exact order_ids whose payment is deliberately wrong, named here so Part B
    # knows which two rows to expect its check to find
    MISMATCHED_ORDER_IDS = [50, 900]
    return (MISMATCHED_ORDER_IDS,)


@app.cell
def _(MISMATCHED_ORDER_IDS, TODAY, datetime, members, options, products, random, timedelta):
    ORDER_COUNT = 1200

    never_ordering_member_ids = set()
    for member in members[:8]:
        never_ordering_member_ids.add(member["member_id"])

    orderable_member_ids = []
    for member in members:
        if member["member_id"] not in never_ordering_member_ids:
            orderable_member_ids.append(member["member_id"])

    # kept out of the most recent 60 days, so question 7 has a real answer
    stale_product_names = {"Herbal Tea", "Granola Bar", "Babson Bean Tote Bag"}

    # a café is busiest in the morning rush and again around lunch, not flat all day
    HOURS = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]
    HOUR_WEIGHTS = [6, 10, 8, 4, 3, 7, 5, 2, 2, 3, 4, 3, 2]

    orders = []
    order_lines = []
    order_line_options = []
    payments = []

    next_order_line_id = 1
    next_payment_id = 1

    for order_id in range(1, ORDER_COUNT + 1):
        days_ago = random.randint(0, 365)
        order_dt = datetime.combine(TODAY, datetime.min.time()) - timedelta(days=days_ago)
        order_hour = random.choices(HOURS, weights=HOUR_WEIGHTS)[0]
        order_dt = order_dt.replace(hour=order_hour, minute=random.randint(0, 59))
        is_recent = days_ago <= 60

        if random.random() < 0.45:
            _member_id = random.choice(orderable_member_ids)
        else:
            _member_id = ""

        if random.random() < 0.6:
            channel = "counter"
        else:
            channel = "app"

        orders.append(
            {
                "order_id": order_id,
                "order_datetime": order_dt.isoformat(sep=" "),
                "member_id": _member_id,
                "channel": channel,
            }
        )

        line_count = random.randint(1, 4)
        order_total = 0.0

        for _line_number in range(line_count):
            while True:
                product = random.choice(products)
                if is_recent and product["name"] in stale_product_names:
                    continue
                break

            quantity = random.randint(1, 3)
            price_charged = product["price"]
            if random.random() < 0.15:
                # an older, lower menu price: the product's price has since gone up
                price_charged = round(price_charged * 0.9, 2)

            order_lines.append(
                {
                    "order_line_id": next_order_line_id,
                    "order_id": order_id,
                    "product_id": product["product_id"],
                    "quantity": quantity,
                    "price_charged": price_charged,
                }
            )
            order_total = order_total + quantity * price_charged

            if product["category"] == "coffee" or product["category"] == "tea":
                for option in options:
                    if random.random() < 0.25:
                        order_line_options.append(
                            {
                                "order_line_id": next_order_line_id,
                                "option_id": option["option_id"],
                                "price_charged": option["price"],
                            }
                        )
                        order_total = order_total + quantity * option["price"]

            next_order_line_id = next_order_line_id + 1

        order_total = round(order_total, 2)

        can_use_points = _member_id != ""
        if can_use_points and random.random() < 0.3:
            points_share = round(random.uniform(0.2, 0.6), 2)
            points_amount = round(order_total * points_share, 2)
            remaining_amount = round(order_total - points_amount, 2)
            second_method = random.choice(["cash", "card", "app"])
            payments.append(
                {"payment_id": next_payment_id, "order_id": order_id, "method": "points", "amount": points_amount}
            )
            next_payment_id = next_payment_id + 1
            payments.append(
                {"payment_id": next_payment_id, "order_id": order_id, "method": second_method, "amount": remaining_amount}
            )
            next_payment_id = next_payment_id + 1
        else:
            method = random.choice(["cash", "card", "card", "app"])
            payments.append({"payment_id": next_payment_id, "order_id": order_id, "method": method, "amount": order_total})
            next_payment_id = next_payment_id + 1

    # on exactly these two orders, nudge one payment so it no longer matches the total
    still_to_adjust = set(MISMATCHED_ORDER_IDS)
    for payment in payments:
        if payment["order_id"] in still_to_adjust:
            payment["amount"] = round(payment["amount"] + random.uniform(1.0, 5.0), 2)
            still_to_adjust.remove(payment["order_id"])
    return order_line_options, order_lines, orders, payments


@app.cell
def _(DATA_DIR, csv, order_line_options, order_lines, orders, os, payments):
    with open(os.path.join(DATA_DIR, "orders.csv"), "w", newline="", encoding="utf-8") as _f:
        _writer = csv.DictWriter(_f, fieldnames=list(orders[0].keys()))
        _writer.writeheader()
        for _row in orders:
            _writer.writerow(_row)

    with open(os.path.join(DATA_DIR, "order_lines.csv"), "w", newline="", encoding="utf-8") as _f:
        _writer = csv.DictWriter(_f, fieldnames=list(order_lines[0].keys()))
        _writer.writeheader()
        for _row in order_lines:
            _writer.writerow(_row)

    with open(os.path.join(DATA_DIR, "order_line_options.csv"), "w", newline="", encoding="utf-8") as _f:
        _writer = csv.DictWriter(_f, fieldnames=list(order_line_options[0].keys()))
        _writer.writeheader()
        for _row in order_line_options:
            _writer.writerow(_row)

    with open(os.path.join(DATA_DIR, "payments.csv"), "w", newline="", encoding="utf-8") as _f:
        _writer = csv.DictWriter(_f, fieldnames=list(payments[0].keys()))
        _writer.writeheader()
        for _row in payments:
            _writer.writerow(_row)
    return


@app.cell
def _(
    MISMATCHED_ORDER_IDS,
    members,
    mo,
    options,
    order_line_options,
    order_lines,
    orders,
    payments,
    products,
):
    mo.md(f"""
    ## Row counts written to `projects/db/data/`

    - `members.csv`: {len(members)} rows
    - `products.csv`: {len(products)} rows
    - `options.csv`: {len(options)} rows
    - `orders.csv`: {len(orders)} rows
    - `order_lines.csv`: {len(order_lines)} rows
    - `order_line_options.csv`: {len(order_line_options)} rows
    - `payments.csv`: {len(payments)} rows

    Orders {MISMATCHED_ORDER_IDS[0]} and {MISMATCHED_ORDER_IDS[1]} are the two rows
    where a payment was deliberately broken so it no longer matches the order's total.
    """)
    return


if __name__ == "__main__":
    app.run()
