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
    # 1. The Question

    Which towns in Middlesex County, Massachusetts, have an average single-family home value of $700,000 or less and an average annual property tax bill under $8,000 in fiscal year 2026?

    The goal is to identify towns that meet both requirements and rank them from the lowest to the highest average property tax bill. The program should also allow users to change the county, home budget, and tax limit to compare different options.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 2. My Plan Before AI

    1. **Set the inputs:** Start with Middlesex County, a $700,000 home budget, an $8,000 annual property tax limit, and fiscal year 2026.

    2. **Get the data:** Use Python's `requests` library to get all towns in the selected county from the Massachusetts API. Check the pagination information to make sure no towns are missing.

    3. **Find the tax information:** Use a `for` loop to get each town's historical data and find its average single-family home value, residential tax rate, and average property tax bill for 2026.

    4. **Filter the towns:** Use `if` statements to check whether each town meets both the home budget and property tax requirements.

    5. **Sort the results:** Store the qualifying towns in a list and sort them by annual property tax bill, from lowest to highest.

    6. **Display the results:** Print a table showing each qualifying town's name, average home value, residential tax rate, and average annual tax bill. Add a sentence summarizing the best options.

    7. **Make the program reusable:** Allow users to change the county, budget, and tax limit to run the comparison again.
    """)
    return


if __name__ == "__main__":
    app.run()
