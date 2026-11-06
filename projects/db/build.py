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

        This notebook creates `database.duckdb` from nothing every time it runs: it
        deletes any old copy, declares every table with its keys and rules, loads the
        CSV files `make_data.py` wrote to `projects/db/data/`, and saves one view. Every
        other cell below only reads the database back, through `ask()`.
        """
    )
    return


@app.cell
def _():
    import os

    import duckdb
    import matplotlib.pyplot as plt
    import polars as pl

    return duckdb, os, pl, plt


@app.cell
def _(mo):
    # mo.notebook_dir() is this notebook's own folder, so the database is found no
    # matter which folder the terminal was opened in.
    database = mo.notebook_dir() / "database.duckdb"
    return (database,)


@app.cell
def _(database, duckdb):
    def ask(sql):
        # opens the file read-only, runs one query, hands back a table, and closes
        # the file again — so build.py can rebuild while this notebook is open.
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 1. The Tables

        Seven tables: `members`, `products` and `options` are what the café already
        keeps; `orders`, `order_lines` and `order_line_options` record what was sold
        and to whom; `payments` records how each order was settled. Every primary key,
        foreign key and rule the scenario states is declared below — `CHECK` for a rule
        that lives inside one row, a foreign key for one that connects two tables.
        """
    )
    return


@app.cell
def _(database, duckdb, os):
    DATA_DIR = database.parent / "data"

    # deleting the old file first means build.py always makes the database from
    # nothing, so it can never drift from the CSV files or the CREATE TABLE statements
    if database.exists():
        os.remove(database)

    with duckdb.connect(database) as _con:
        _con.execute(
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

        _con.execute(
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

        _con.execute(
            """
            CREATE TABLE options (
                option_id INTEGER PRIMARY KEY,
                name VARCHAR NOT NULL,
                price DECIMAL(6, 2) NOT NULL CHECK (price >= 0),
                cost DECIMAL(6, 2) NOT NULL CHECK (cost >= 0)
            );
            """
        )

        _con.execute(
            """
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                order_datetime TIMESTAMP NOT NULL,
                member_id INTEGER REFERENCES members (member_id),
                channel VARCHAR NOT NULL CHECK (channel IN ('counter', 'app'))
            );
            """
        )

        _con.execute(
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

        _con.execute(
            """
            CREATE TABLE order_line_options (
                order_line_id INTEGER NOT NULL REFERENCES order_lines (order_line_id),
                option_id INTEGER NOT NULL REFERENCES options (option_id),
                price_charged DECIMAL(6, 2) NOT NULL CHECK (price_charged >= 0),
                PRIMARY KEY (order_line_id, option_id)
            );
            """
        )

        _con.execute(
            """
            CREATE TABLE payments (
                payment_id INTEGER PRIMARY KEY,
                order_id INTEGER NOT NULL REFERENCES orders (order_id),
                method VARCHAR NOT NULL CHECK (method IN ('cash', 'card', 'app', 'points')),
                amount DECIMAL(8, 2) NOT NULL CHECK (amount > 0)
            );
            """
        )

        # parents load before children, so every foreign key finds the row it points to
        load_order = [
            "members",
            "products",
            "options",
            "orders",
            "order_lines",
            "order_line_options",
            "payments",
        ]
        for _table_name in load_order:
            _csv_path = DATA_DIR / f"{_table_name}.csv"
            # nullstr='' turns an empty CSV field (no email, no member) into a real NULL
            _con.execute(
                f"INSERT INTO {_table_name} SELECT * FROM read_csv('{_csv_path}', header = true, nullstr = '')"
            )

        # a question the café would ask every week: what each menu category earns,
        # once the options on its lines are counted in — Part B's question 2 uses this
        _con.execute(
            """
            CREATE VIEW category_revenue AS
            WITH line_options AS (
                SELECT
                    ol.order_line_id,
                    sum(ol.quantity * olo.price_charged) AS options_revenue,
                    sum(ol.quantity * o.cost) AS options_cost
                FROM order_lines ol
                JOIN order_line_options olo ON olo.order_line_id = ol.order_line_id
                JOIN options o ON o.option_id = olo.option_id
                GROUP BY ol.order_line_id
            )
            SELECT
                p.category,
                sum(ol.quantity * ol.price_charged) AS product_revenue,
                sum(ol.quantity * p.cost) AS product_cost,
                sum(coalesce(lo.options_revenue, 0)) AS options_revenue,
                sum(coalesce(lo.options_cost, 0)) AS options_cost,
                sum(ol.quantity * ol.price_charged) + sum(coalesce(lo.options_revenue, 0)) AS total_revenue,
                sum(ol.quantity * p.cost) + sum(coalesce(lo.options_cost, 0)) AS total_cost
            FROM order_lines ol
            JOIN products p ON p.product_id = ol.product_id
            LEFT JOIN line_options lo ON lo.order_line_id = ol.order_line_id
            GROUP BY p.category;
            """
        )

    return (DATA_DIR,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 2. The Data

        `make_data.py` writes 50 members, 26 products, 8 options, and 1,200 orders
        (with their lines, options and payments) covering the 12 months up to
        `TODAY = 2026-11-01`, the `as_of` date Part B uses. It follows every rule in
        the scenario, with one exception, made on purpose: **orders 50 and 900** each
        have a payment nudged a few dollars away from their order's true total, so
        the payments-vs-total check (question 4) has two real rows to find. The query
        below finds them the same way that check will.
        """
    )
    return


@app.cell
def _(ask):
    ask(
        """
        SELECT
            o.order_id,
            coalesce(lines.lines_total, 0) + coalesce(opts.options_total, 0) AS charged_total,
            coalesce(paid.paid_total, 0) AS paid_total
        FROM orders o
        LEFT JOIN (
            SELECT order_id, sum(quantity * price_charged) AS lines_total
            FROM order_lines GROUP BY order_id
        ) lines ON lines.order_id = o.order_id
        LEFT JOIN (
            SELECT ol.order_id, sum(ol.quantity * olo.price_charged) AS options_total
            FROM order_line_options olo
            JOIN order_lines ol ON ol.order_line_id = olo.order_line_id
            GROUP BY ol.order_id
        ) opts ON opts.order_id = o.order_id
        LEFT JOIN (
            SELECT order_id, sum(amount) AS paid_total
            FROM payments GROUP BY order_id
        ) paid ON paid.order_id = o.order_id
        WHERE abs(coalesce(paid.paid_total, 0) - (coalesce(lines.lines_total, 0) + coalesce(opts.options_total, 0))) > 0.01
        ORDER BY order_id
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 3. A Look at the Data

        Reading `orders.csv` straight with polars (not through the database), and
        charting orders by hour of day.
        """
    )
    return


@app.cell
def _(DATA_DIR, pl):
    orders_by_hour = (
        pl.read_csv(DATA_DIR / "orders.csv", try_parse_dates=True)
        .with_columns(pl.col("order_datetime").dt.hour().alias("hour"))
        .group_by("hour")
        .len()
        .sort("hour")
    )
    return (orders_by_hour,)


@app.cell
def _(orders_by_hour, plt):
    fig, ax = plt.subplots()
    ax.bar(orders_by_hour["hour"], orders_by_hour["len"])
    ax.set_xlabel("Hour of day")
    ax.set_ylabel("Number of orders")
    ax.set_title("Orders by hour of day")
    fig
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        A real café would look like this: a tall morning-rush peak around 8 a.m., a
        smaller lunchtime bump around noon, and quieter hours on either side —
        `make_data.py` weights the hour an order happens toward those two peaks
        instead of spreading orders evenly across the day, which is what an earlier
        version of the script did.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""## 4. Row Counts""")
    return


@app.cell
def _(ask, mo):
    table_names = [
        "members",
        "products",
        "options",
        "orders",
        "order_lines",
        "order_line_options",
        "payments",
    ]
    count_lines = []
    for _table in table_names:
        _n = ask(f"SELECT count(*) AS n FROM {_table}").item()
        count_lines.append(f"- `{_table}`: {_n} rows")

    mo.md("\n".join(count_lines))
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 5. A Row It Refuses

        `ask()` only reads, so this insert opens a short write connection of its own,
        inside `try`/`except`, so the rest of the notebook still runs after it fails.
        """
    )
    return


@app.cell
def _(database, duckdb):
    try:
        with duckdb.connect(database) as _con:
            # a quantity of -1 breaks the CHECK (quantity > 0) rule on order_lines
            _con.execute("INSERT INTO order_lines VALUES (999999, 1, 1, -1, 3.00)")
        refusal_message = "the database accepted it — that should not happen"
    except Exception as _e:
        refusal_message = str(_e)

    refusal_message
    return


@app.cell
def _(mo):
    mo.md(r"""## 6. Answers You Already Knew""")
    return


@app.cell
def _(ask, mo):
    members_count = ask("SELECT count(*) AS n FROM members").item()
    options_count = ask("SELECT count(*) AS n FROM options").item()
    unavailable_count = ask("SELECT count(*) AS n FROM products WHERE NOT is_available").item()

    mo.md(
        f"""
        - `SELECT count(*) FROM members` → **{members_count}**. Expected 50, because
          `make_data.py` sets `MEMBER_COUNT = 50`.
        - `SELECT count(*) FROM options` → **{options_count}**. Expected 8, because
          `OPTION_CATALOG` lists exactly 8 options.
        - `SELECT count(*) FROM products WHERE NOT is_available` → **{unavailable_count}**.
          Expected 2 — Herbal Tea and Granola Bar are the two named in
          `UNAVAILABLE_PRODUCTS`.
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## 7. A View

        `category_revenue`, created above while the database was built, is the report
        the café would pull every week: what each menu category earned, after folding
        in what its options earned. Part B's question 2 reads it by name instead of
        repeating this query.
        """
    )
    return


@app.cell
def _(ask):
    ask("SELECT * FROM category_revenue ORDER BY category")
    return


if __name__ == "__main__":
    app.run()
