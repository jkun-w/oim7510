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
    # Babson Bean Café — Answering the Business's Questions

    This notebook only reads `database.duckdb`, through the same `ask()` helper
    `build.py` uses. Run `uv run python projects/db/build.py` first to create (or
    recreate) the database from the CSV files.
    """)
    return


@app.cell
def _():
    import duckdb

    return (duckdb,)


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
        # the file again
        with duckdb.connect(database, read_only=True) as _con:
            return _con.sql(sql).pl()

    return (ask,)


@app.cell
def _():
    from datetime import date

    # the same as_of date make_data.py used as TODAY, so "last month" and "the last
    # 60 days" below mean the same thing they meant when the data was generated
    AS_OF = date(2026, 11, 1)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Question 1 · The three best-selling products last month, by units

    "Last month" means October 2026, the full calendar month before `AS_OF`.
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        SELECT p.name, sum(ol.quantity) AS units
        FROM order_lines ol
        JOIN orders o ON o.order_id = ol.order_id
        JOIN products p ON p.product_id = ol.product_id
        WHERE o.order_datetime >= DATE '2026-10-01' AND o.order_datetime < DATE '2026-11-01'
        GROUP BY p.name
        ORDER BY units DESC
        LIMIT 3
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    In October 2026 the three best sellers by units were the Blueberry Muffin
    (35), the Matcha Latte (30) and Orange Juice (28).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Question 2 · Revenue, cost and margin by menu category

    This reads `category_revenue`, the view `build.py` saved, instead of
    repeating its query — it already folds each line's options into the category
    of the product on that line.
    """)
    return


@app.cell
def _(ask):
    ask(
        "SELECT category, total_revenue, total_cost, total_revenue - total_cost AS margin "
        "FROM category_revenue ORDER BY total_revenue DESC"
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    Coffee earns the most revenue ($9,710.69) and the most margin ($7,201.49,
    about 74 cents of every coffee dollar). Tea earns the best margin rate (about
    76%), while "other" earns the worst (about 61%), even though "other" and tea
    bring in almost the same revenue — "other" costs the café more per dollar it
    takes in.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Question 3 · Members above the members' average spend

    "Total spent" follows the scenario's own definition of revenue: a line's
    price charged, plus whatever its options were charged — however the order was
    paid. `order_totals` adds those two up per order; `member_totals` adds orders
    up per member; the last query keeps only members above the average of
    `member_totals.total_spent`.
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        WITH order_totals AS (
            SELECT
                o.order_id,
                o.member_id,
                coalesce(lines.lines_total, 0) + coalesce(opts.options_total, 0) AS order_total
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
        ),
        member_totals AS (
            SELECT
                m.member_id,
                m.first_name,
                count(*) AS order_count,
                sum(order_total) AS total_spent,
                avg(order_total) AS avg_order
            FROM members m
            JOIN order_totals ot ON ot.member_id = m.member_id
            GROUP BY m.member_id, m.first_name
        )
        SELECT * FROM member_totals
        WHERE total_spent > (SELECT avg(total_spent) FROM member_totals)
        ORDER BY total_spent DESC
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    20 of the 42 members who have ordered spent more than the members' average of
    $313.84. Diana (member 45) spent the most, $525.67 over 25 orders.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Question 4 · Orders whose payments do not match their total (checks a rule)

    A `CHECK` cannot hold a rule that spans `order_lines`, `order_line_options`
    and `payments`, so this is a query instead. It totals the lines and their
    options on one side, the payments on the other, *before* comparing them — not
    a single join across all three, which would multiply lines by payments.
    """)
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
    mo.md(r"""
    Two orders don't balance: order 50 was charged $14.00 but paid $17.30, and
    order 900 was charged $26.17 but paid $29.39. Every other order's payments add
    up to its total.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Question 5 · Members who joined and have never ordered

    A member who has never ordered has no row in `orders` where `member_id`
    matches theirs — `NOT EXISTS` finds exactly that.
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        SELECT member_id, first_name, join_date
        FROM members m
        WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.member_id = m.member_id)
        ORDER BY join_date
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    8 of the 50 members have never placed an order, from Diana (joined
    2025-02-06) to Danielle, the most recently joined of the eight
    (2026-09-07).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Question 6 · Share of orders paid at least partly with points, by month

    `points_orders` is the distinct set of orders with at least one `points`
    payment — an order with two points payments still counts once. A `LEFT JOIN`
    from every order keeps months and orders that never used points, at 0%.
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        WITH monthly_orders AS (
            SELECT date_trunc('month', order_datetime) AS month, order_id FROM orders
        ),
        points_orders AS (
            SELECT DISTINCT order_id FROM payments WHERE method = 'points'
        )
        SELECT
            mo.month,
            count(*) AS orders_count,
            count(po.order_id) AS orders_with_points,
            round(100.0 * count(po.order_id) / count(*), 1) AS points_share_pct
        FROM monthly_orders mo
        LEFT JOIN points_orders po ON po.order_id = mo.order_id
        GROUP BY mo.month
        ORDER BY mo.month
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    The points share of orders sits mostly between 12% and 20% month to month,
    with no clear trend up or down — February 2026 is the high point at 20.2%.
    (November 2026 shows 6 orders and 0%, but that month only runs through
    `AS_OF`, November 1, so it is not a full month and shouldn't be compared to
    the rest.)
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Question 7 · Products that have not sold in the last 60 days

    "The last 60 days" means the 60 days ending on `AS_OF`, so 2026-09-02 through
    2026-11-01 inclusive. A product counts as stale if no `order_lines` row for it
    joins to an order in that window, available or not.
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        SELECT p.product_id, p.name, p.is_available
        FROM products p
        WHERE NOT EXISTS (
            SELECT 1 FROM order_lines ol
            JOIN orders o ON o.order_id = ol.order_id
            WHERE ol.product_id = p.product_id
            AND o.order_datetime::DATE BETWEEN (DATE '2026-11-01' - INTERVAL 60 DAY) AND DATE '2026-11-01'
        )
        ORDER BY p.name
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    Three products haven't sold in the last 60 days: the Babson Bean Tote Bag,
    which is still on the menu as available, and Granola Bar and Herbal Tea,
    which are both marked unavailable — so all three are candidates to drop or
    promote, not just the two already pulled from the menu.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Question 8 (my own) · Which option earns its keep?

    The scenario asks which add-ons "earn their keep." Question 2 totals options
    into each category's revenue, but it never says which *option* is doing the
    earning. This question ranks the 8 options by the profit (what they charged,
    minus what they cost) they generated across every line that carried them.
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        SELECT
            opt.name,
            count(*) AS times_added,
            sum(ol.quantity) AS units_added,
            sum(ol.quantity * (olo.price_charged - opt.cost)) AS total_profit
        FROM order_line_options olo
        JOIN options opt ON opt.option_id = olo.option_id
        JOIN order_lines ol ON ol.order_line_id = olo.order_line_id
        GROUP BY opt.name
        ORDER BY total_profit DESC
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    Extra Shot earns the café the most profit overall ($451.00 across 820 units),
    even though it isn't the most-added option. Decaf is added almost as often as
    any other option (420 times) but earns **$0** in profit — its price charged
    equals its cost on every line, so the café should either price it like the
    other options or stop treating it as free to make.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## How I Know These Numbers Are Right

    Three of the answers above were each reached a second way.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Question 5, a count checked by counting the same rows another way.** 8
    members have never ordered. A second query counts it the opposite way — all
    50 members, minus the 42 distinct members who *do* appear in `orders` — and
    gets 50 − 42 = 8 too.
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        SELECT
            (SELECT count(*) FROM members) AS total_members,
            (SELECT count(DISTINCT member_id) FROM orders WHERE member_id IS NOT NULL) AS members_with_orders,
            (SELECT count(*) FROM members) - (SELECT count(DISTINCT member_id) FROM orders WHERE member_id IS NOT NULL) AS difference
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Question 4, a number checked against the data generated in Part A.** The
    query names orders 50 and 900. `make_data.py` records the IDs it deliberately
    broke in its own `MISMATCHED_ORDER_IDS` list — `[50, 900]`, the same two.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Question 2, a total checked against the sum of its parts.** The four
    categories' `total_revenue` should add up to the café's overall revenue —
    every line's price charged, plus every option charged on it — computed
    directly, without grouping by category at all.
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        SELECT
            (SELECT sum(total_revenue) FROM category_revenue) AS sum_of_category_totals,
            (
                SELECT sum(ol.quantity * ol.price_charged) + coalesce((
                    SELECT sum(ol2.quantity * olo.price_charged)
                    FROM order_line_options olo
                    JOIN order_lines ol2 ON ol2.order_line_id = olo.order_line_id
                ), 0)
                FROM order_lines ol
            ) AS cafe_total_revenue
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    Both come to $28,629.73 — the categories don't miss or double-count a line.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Working With the Agent

    The agent's first draft of `make_data.py` picked each order's hour of day
    uniformly at random across the day. That passed every rule and every row
    count, so nothing in `build.py`'s checks caught it — but once "A Look at the
    Data" charted orders by hour, a flat bar chart across all 24 hours is not what
    a café looks like; a real café has a morning rush and a lunch bump. I had the
    agent replace the uniform pick with `random.choices(HOURS, weights=HOUR_WEIGHTS)`,
    weighted toward 8 a.m. and noon, in `make_data.py` and regenerated the CSVs —
    documented in the commit `db: rework build.py to match the assignment's
    required structure` and in the note under the chart in `build.py`'s
    section 3.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Reading It Back

    I'm using **question 4** — the payments-vs-total check — for this section,
    because the scenario itself warns about exactly this join: "joined together,
    every line meets every payment."

    **The join I'm about to run:** `order_lines` joined straight to `payments`,
    matching only on `order_id`, with no `GROUP BY` yet.

    **My prediction, before running it:** this join does not produce one row per
    order line, and it does not produce one row per payment. For one order, every
    one of its lines gets paired with every one of its payments — an order with 3
    lines and 2 payments contributes 3 × 2 = 6 rows to the result, not 3, not 2,
    and not 5.

    From the row counts `build.py` already printed (section 4 there), the café has
    3,048 `order_lines` over 1,200 orders — 2.54 lines per order, on average — and
    1,377 `payments` over the same 1,200 orders — 1.1475 payments per order, on
    average, since roughly 3 orders in 10 split into two payments. If which orders
    get extra lines and which orders get a split payment are unrelated to each
    other, I'd expect this ungrouped join to have roughly
    3,048 × 1.1475 ≈ **3,500 rows** — more than the 3,048 lines alone, and nowhere
    close to 3,048 × 1,377, which would be every line in the café paired with
    every payment in the café, not just the ones on the same order.

    _(the actual row count, and what one row of it means, are written below after
    this prediction is committed)_
    """)
    return


@app.cell
def _(ask):
    ask("SELECT count(*) FROM order_lines ol JOIN payments p ON p.order_id = ol.order_id")
    return


@app.cell
def _(mo):
    mo.md(r"""
    **The actual count is 3,489 rows** — close to the roughly 3,500 I predicted,
    and well above the 3,048 order lines alone, which confirms the fan-out really
    happened and wasn't small enough to ignore.

    To see why, here is every row this join produces for a single order, number
    957, which has 3 lines and 2 payments:
    """)
    return


@app.cell
def _(ask):
    ask(
        """
        SELECT ol.order_id, ol.order_line_id, ol.product_id, p.payment_id, p.method, p.amount
        FROM order_lines ol
        JOIN payments p ON p.order_id = ol.order_id
        WHERE ol.order_id = 957
        ORDER BY ol.order_line_id, p.payment_id
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    Order 957 becomes 3 × 2 = 6 rows: each of its 3 lines (2434, 2435, 2436)
    appears twice, once next to each of its 2 payments (one by points, one by
    card). One row of this joined, ungrouped table does **not** mean "this payment
    was for this line" — payments settle a whole order, not one line of it — it is
    just every pairing the join can make before anyone groups or totals anything.
    That is exactly why question 4 totals the lines (with their options) and the
    payments *separately*, in their own subqueries, before ever comparing the two:
    joining them first and summing afterward would count each payment once for
    every line on the order, inflating `paid_total` by a factor of the line count.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Going Further

    A dropdown, so the café can check any one category's best sellers without
    touching a query — it re-runs the moment the dropdown changes, because that's
    how a marimo `mo.ui.dropdown` works.
    """)
    return


@app.cell
def _(ask, mo):
    category_choice = mo.ui.dropdown(
        options=ask("SELECT DISTINCT category FROM products ORDER BY category")["category"].to_list(),
        value="coffee",
        label="Category",
    )
    category_choice
    return (category_choice,)


@app.cell
def _(ask, category_choice):
    ask(
        f"""
        SELECT p.name, sum(ol.quantity) AS units, sum(ol.quantity * ol.price_charged) AS revenue
        FROM order_lines ol
        JOIN products p ON p.product_id = ol.product_id
        WHERE p.category = '{category_choice.value}'
        GROUP BY p.name
        ORDER BY units DESC
        """
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Time Spent

    About 5 hours in total, across the design, Part A's build, and Part B.
    """)
    return


if __name__ == "__main__":
    app.run()
