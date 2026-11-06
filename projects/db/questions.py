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
        # Babson Bean Café — Answering the Business's Questions

        This notebook only reads `database.duckdb`, through the same `ask()` helper
        `build.py` uses. Run `uv run python projects/db/build.py` first to create (or
        recreate) the database from the CSV files.
        """
    )
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
    return (AS_OF,)


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 1 · The three best-selling products last month, by units

        _(answered below, after the prediction in "Reading It Back" is committed)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 2 · Revenue, cost and margin by menu category

        _(answered below, after the prediction in "Reading It Back" is committed)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 3 · Members above the members' average spend

        _(answered below, after the prediction in "Reading It Back" is committed)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 4 · Orders whose payments do not match their total (checks a rule)

        _(answered below, after the prediction in "Reading It Back" is committed)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 5 · Members who joined and have never ordered

        _(answered below, after the prediction in "Reading It Back" is committed)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 6 · Share of orders paid at least partly with points, by month

        _(answered below, after the prediction in "Reading It Back" is committed)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 7 · Products that have not sold in the last 60 days

        _(answered below, after the prediction in "Reading It Back" is committed)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Question 8 (my own) · Which option earns its keep?

        The scenario asks which add-ons "earn their keep." Question 2 totals options
        into each category's revenue, but it never says which *option* is doing the
        earning. This question ranks the 8 options by the profit (what they charged,
        minus what they cost) they generated across every line that carried them.

        _(answered below, after the prediction in "Reading It Back" is committed)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## How I Know These Numbers Are Right

        _(written after the questions above are answered)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Working With the Agent

        _(written after the questions above are answered)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
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
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Going Further

        _(written after the questions above are answered)_
        """
    )
    return


@app.cell
def _(mo):
    mo.md(
        r"""
        ## Time Spent

        _(not graded — written after the questions above are answered)_
        """
    )
    return


if __name__ == "__main__":
    app.run()
