import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _(mo):
    mo.md(
        r"""
        # Babson Bean Café — Building the Database

        This notebook creates `database.duckdb`, declares every table with its primary
        key, its foreign keys and the rules a `CHECK` constraint can hold, loads the CSV
        files from `projects/db/data/`, and then checks the one rule that spans tables:
        that an order's payments add up to its total.
        """
    )
    return


@app.cell
def _():
    import os

    import duckdb

    return duckdb, os


@app.cell
def _(os):
    # __file__ is this notebook's own path, so these folders are found no matter
    # which folder the terminal was opened in.
    DB_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(DB_DIR, "data")
    DB_PATH = os.path.join(DB_DIR, "database.duckdb")
    return DATA_DIR, DB_PATH


@app.cell
def _(DB_PATH, duckdb, os):
    # Rebuilding from scratch each time means build.py can be re-run safely.
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    con = duckdb.connect(DB_PATH)
    return (con,)


@app.cell
def _(mo):
    mo.md(r"""## Tables""")
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE TABLE members (
            member_id INTEGER PRIMARY KEY,
            first_name VARCHAR NOT NULL,
            mobile_number VARCHAR NOT NULL,
            email VARCHAR,
            join_date DATE NOT NULL,
            points_balance INTEGER NOT NULL CHECK (points_balance >= 0)
        );
        """
    )

    con.execute(
        """
        CREATE TABLE products (
            product_id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            category VARCHAR NOT NULL CHECK (category IN ('coffee', 'tea', 'food', 'other')),
            price DECIMAL(6, 2) NOT NULL,
            cost DECIMAL(6, 2) NOT NULL,
            is_available BOOLEAN NOT NULL,
            CHECK (price >= cost)
        );
        """
    )

    con.execute(
        """
        CREATE TABLE options (
            option_id INTEGER PRIMARY KEY,
            name VARCHAR NOT NULL,
            price DECIMAL(6, 2) NOT NULL CHECK (price >= 0),
            cost DECIMAL(6, 2) NOT NULL CHECK (cost >= 0)
        );
        """
    )

    con.execute(
        """
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            order_datetime TIMESTAMP NOT NULL,
            member_id INTEGER REFERENCES members (member_id),
            channel VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
        );
        """
    )

    con.execute(
        """
        CREATE TABLE order_lines (
            order_line_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders (order_id),
            product_id INTEGER NOT NULL REFERENCES products (product_id),
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            price_charged DECIMAL(6, 2) NOT NULL CHECK (price_charged >= 0)
        );
        """
    )

    con.execute(
        """
        CREATE TABLE order_line_options (
            order_line_id INTEGER NOT NULL REFERENCES order_lines (order_line_id),
            option_id INTEGER NOT NULL REFERENCES options (option_id),
            price_charged DECIMAL(6, 2) NOT NULL CHECK (price_charged >= 0),
            PRIMARY KEY (order_line_id, option_id)
        );
        """
    )

    con.execute(
        """
        CREATE TABLE payments (
            payment_id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders (order_id),
            method VARCHAR NOT NULL CHECK (method IN ('cash', 'card', 'app', 'points')),
            amount DECIMAL(8, 2) NOT NULL CHECK (amount > 0)
        );
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## Loading the CSV files""")
    return


@app.cell
def _(DATA_DIR, con, os):
    # Parents load before children, so every foreign key finds the row it points to.
    load_order = [
        "members",
        "products",
        "options",
        "orders",
        "order_lines",
        "order_line_options",
        "payments",
    ]

    for table_name in load_order:
        csv_path = os.path.join(DATA_DIR, f"{table_name}.csv")
        # nullstr='' turns an empty CSV field (no email, no member) into a real NULL.
        con.execute(
            f"INSERT INTO {table_name} SELECT * FROM read_csv('{csv_path}', header = true, nullstr = '')"
        )

    return (load_order,)


@app.cell
def _(mo):
    mo.md(r"""## Checking the row counts""")
    return


@app.cell
def _(con, load_order, mo):
    count_lines = []
    for _table_name in load_order:
        _count = con.execute(f"SELECT count(*) FROM {_table_name}").fetchone()[0]
        count_lines.append(f"- `{_table_name}`: {_count} rows")

    mo.md("\n".join(count_lines))
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Checking the one rule a `CHECK` can't hold

        A `CHECK` constraint can only look at one row of one table, so it can't require
        that an order's payments add up to its lines and their options. That rule is
        checked here instead, with a query that compares the two totals for every order.
        """
    )
    return


@app.cell
def _(con):
    con.execute(
        """
        CREATE VIEW order_totals AS
        SELECT
            o.order_id,
            -- what the order should cost: every line, plus every option, charged once per unit
            coalesce(lines.lines_total, 0) + coalesce(line_options.options_total, 0) AS charged_total,
            coalesce(paid.paid_total, 0) AS paid_total
        FROM orders o
        LEFT JOIN (
            SELECT order_id, sum(quantity * price_charged) AS lines_total
            FROM order_lines
            GROUP BY order_id
        ) lines ON lines.order_id = o.order_id
        LEFT JOIN (
            SELECT ol.order_id, sum(ol.quantity * olo.price_charged) AS options_total
            FROM order_line_options olo
            JOIN order_lines ol ON ol.order_line_id = olo.order_line_id
            GROUP BY ol.order_id
        ) line_options ON line_options.order_id = o.order_id
        LEFT JOIN (
            SELECT order_id, sum(amount) AS paid_total
            FROM payments
            GROUP BY order_id
        ) paid ON paid.order_id = o.order_id;
        """
    )
    return


@app.cell
def _(con):
    # a penny of rounding is fine; anything more means the payments do not match the order
    mismatched_orders = con.execute(
        """
        SELECT order_id, charged_total, paid_total, round(paid_total - charged_total, 2) AS difference
        FROM order_totals
        WHERE abs(paid_total - charged_total) > 0.01
        ORDER BY order_id
        """
    ).fetchall()
    mismatched_orders
    return (mismatched_orders,)


@app.cell
def _(mismatched_orders, mo):
    mo.md(
        f"""
        **{len(mismatched_orders)} orders** have payments that do not add up to their
        total. (12 orders were deliberately thrown off when the data was made, so this
        check has something real to catch.)
        """
    )
    return


@app.cell
def _(con):
    con.close()
    return


if __name__ == "__main__":
    app.run()
