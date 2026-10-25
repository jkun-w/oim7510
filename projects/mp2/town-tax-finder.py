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


@app.cell
def _(mo):
    mo.md(r"""
    # 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.
    """)
    return


@app.cell
def _():
    county = "Middlesex"
    budget_dollars = 700000
    tax_limit_dollars = 8000
    fiscal_year = 2026
    return budget_dollars, county, fiscal_year, tax_limit_dollars


@app.cell
def _(mo):
    mo.md(r"""
    # 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(county):
    import requests

    first_page = requests.get(
        "https://oim.zhili.dev/ma/towns",
        params={"county": county, "per_page": 100},
        timeout=10,
    ).json()

    first_page
    return (requests,)


@app.cell
def _(requests):
    sample_history = requests.get(
        "https://oim.zhili.dev/ma/towns/002/history",
        timeout=10,
    ).json()

    sample_history
    return


@app.cell
def _(county, requests):
    county_towns = []
    _page = 1

    while True:
        _reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": county, "per_page": 100, "page": _page},
            timeout=10,
        ).json()

        county_towns.extend(_reply["items"])

        if not _reply["pagination"]["has_next"]:
            break
        _page += 1

    len(county_towns), county_towns[0]["name"]
    return (county_towns,)


@app.cell
def _(county_towns, fiscal_year, requests):
    town_records = []
    skipped_towns = []

    for _town in county_towns:
        _history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{_town['dor_code']}/history",
            timeout=10,
        ).json()

        _year_data = None
        for _year in _history["years"]:
            if _year["fiscal_year"] == fiscal_year:
                _year_data = _year
                break

        if _year_data is None:
            skipped_towns.append(_town["name"])
            continue

        town_records.append({
            "name": _town["name"],
            "average_single_family_value_dollars": _year_data["average_single_family_value_dollars"],
            "residential_rate_per_thousand": _year_data["residential_rate_per_thousand"],
            "average_single_family_bill_dollars": _year_data["average_single_family_bill_dollars"],
        })

    len(town_records), skipped_towns
    return (town_records,)


@app.cell
def _(budget_dollars, tax_limit_dollars, town_records):
    qualifying_towns = []

    for _record in town_records:
        if _record["average_single_family_value_dollars"] <= budget_dollars and _record["average_single_family_bill_dollars"] < tax_limit_dollars:
            qualifying_towns.append(_record)

    qualifying_towns.sort(key=lambda _record: _record["average_single_family_bill_dollars"])

    len(qualifying_towns)
    return (qualifying_towns,)


@app.cell
def _(mo):
    mo.md(r"""
    # 5. The Answer

    A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.
    """)
    return


@app.cell
def _(
    budget_dollars,
    county,
    fiscal_year,
    qualifying_towns,
    tax_limit_dollars,
):
    print(f"Towns in {county} County under ${budget_dollars:,} with an annual tax bill under ${tax_limit_dollars:,} (fiscal year {fiscal_year})")
    print(f"{'Town':<16} {'Avg. Home Value':>16} {'Tax Rate':>10} {'Avg. Annual Bill':>18}")
    for _town in qualifying_towns:
        print(f"{_town['name']:<16} {_town['average_single_family_value_dollars']:>16,.0f} {_town['residential_rate_per_thousand']:>10.2f} {_town['average_single_family_bill_dollars']:>18,.0f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    In Middlesex County, 12 towns have an average single-family home value of $700,000 or less and an average annual property tax bill under $8,000 for fiscal year 2026, with Malden offering the lowest average bill at $4,952.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 6. Going Further

    ### 1. Rank by Tax Rate Instead of Bill

    The same 12 towns, sorted by `residential_rate_per_thousand` instead of the average annual bill. Does the order change, and why?
    """)
    return


@app.cell
def _(
    budget_dollars,
    county,
    fiscal_year,
    qualifying_towns,
    tax_limit_dollars,
):
    towns_by_rate = sorted(qualifying_towns, key=lambda _record: _record["residential_rate_per_thousand"])

    print(f"Towns in {county} County under ${budget_dollars:,} with an annual tax bill under ${tax_limit_dollars:,} (fiscal year {fiscal_year}), ranked by tax rate")
    print(f"{'Town':<16} {'Avg. Home Value':>16} {'Tax Rate':>10} {'Avg. Annual Bill':>18}")
    for _town in towns_by_rate:
        print(f"{_town['name']:<16} {_town['average_single_family_value_dollars']:>16,.0f} {_town['residential_rate_per_thousand']:>10.2f} {_town['average_single_family_bill_dollars']:>18,.0f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    The order changes: Malden has the lowest bill but only the 5th-lowest tax rate, while Dracut has the lowest tax rate but only the 3rd-lowest bill. This is because the annual bill depends on both the tax rate and the town's average home value, so a town with a middling rate but cheaper homes, like Malden, can still produce a lower bill than a town with a lower rate but pricier homes, like Dracut.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 2. Ten Years of Bills for the Three Cheapest Towns

    For the three towns with the lowest bill on the list, their average annual bill for each of the last 10 fiscal years.
    """)
    return


@app.cell
def _(county_towns, fiscal_year, qualifying_towns, requests):
    cheapest_three = qualifying_towns[:3]

    town_name_to_code = {}
    for _town in county_towns:
        town_name_to_code[_town["name"]] = _town["dor_code"]

    ten_year_bills = {}
    for _town in cheapest_three:
        _dor_code = town_name_to_code[_town["name"]]
        _history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{_dor_code}/history",
            timeout=10,
        ).json()

        _bills_by_year = {}
        for _year in _history["years"]:
            if fiscal_year - 9 <= _year["fiscal_year"] <= fiscal_year:
                _bills_by_year[_year["fiscal_year"]] = _year["average_single_family_bill_dollars"]

        ten_year_bills[_town["name"]] = _bills_by_year

    ten_year_bills
    return cheapest_three, ten_year_bills


@app.cell
def _(cheapest_three, fiscal_year, ten_year_bills):
    years_available = list(range(fiscal_year - 9, fiscal_year + 1))

    print(f"{'Year':<6}" + "".join(f"{_town['name']:>12}" for _town in cheapest_three))
    for _year in years_available:
        _row = f"{_year:<6}"
        for _town in cheapest_three:
            _bill = ten_year_bills[_town["name"]].get(_year)
            if _bill is None:
                _row += f"{'n/a':>12}"
            else:
                _row += f"{_bill:>12,.0f}"
        print(_row)
    return


@app.cell
def _(mo):
    mo.md(r"""
    Dracut's bill rose steadily from $4,440 in fiscal year 2017 to $5,737 in 2026, an increase of about 29% over 10 years. Malden and Waltham only have history on file back to 2022 (shown as n/a above for 5 years), but over that shorter stretch, Malden's bill rose from $4,278 to $4,952 (about 16%), and Waltham's from $4,631 to $5,189 (about 12%).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 3. The Bill as a Share of Income

    For the 12 qualifying towns, the average annual tax bill alongside each town's income per capita, and the bill stated as a percentage of that income.
    """)
    return


@app.cell
def _(county_towns, qualifying_towns):
    town_name_to_income = {}
    for _town in county_towns:
        town_name_to_income[_town["name"]] = _town["income_per_capita_dollars"]

    print(f"{'Town':<16} {'Avg. Annual Bill':>18} {'Income/Capita':>16} {'Bill as % of Income':>22}")
    for _town in qualifying_towns:
        _income = town_name_to_income[_town["name"]]
        _bill = _town["average_single_family_bill_dollars"]
        _share_percent = _bill / _income * 100
        print(f"{_town['name']:<16} {_bill:>18,.0f} {_income:>16,.0f} {_share_percent:>21.1f}%")
    return


@app.cell
def _(mo):
    mo.md(r"""
    Everett and Lowell have the lowest bills in dollar terms on this list (\$5,887 and \$5,844), but because their income per capita is also among the lowest, the bill eats up 22.3% and 21.3% of income, the highest share of any qualifying town. Waltham, by contrast, has a similar dollar bill (\$5,189) but a lower share of income (10.5%), since its income per capita is nearly double Lowell's. The dollar amount and the share of income tell different stories about affordability, and the couple may want to weigh both.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### 4. Change the County and Limits Without Editing Code

    A dropdown for the county, and number inputs for the budget and tax limit. Press the button to rerun the search with whatever is selected.
    """)
    return


@app.cell
def _(requests):
    all_counties = requests.get("https://oim.zhili.dev/ma/counties", timeout=10).json()
    all_counties
    return (all_counties,)


@app.cell
def _(all_counties, mo):
    county_names = []
    for _county in all_counties:
        county_names.append(_county["name"])

    county_dropdown = mo.ui.dropdown(options=county_names, value="Middlesex", label="County")
    budget_input = mo.ui.number(start=100000, stop=5000000, value=700000, step=10000, label="Home budget ($)")
    tax_limit_input = mo.ui.number(start=1000, stop=50000, value=8000, step=100, label="Annual tax limit ($)")
    search_button = mo.ui.run_button(label="Search")

    mo.vstack([county_dropdown, budget_input, tax_limit_input, search_button])
    return budget_input, county_dropdown, search_button, tax_limit_input


@app.cell
def _(
    budget_input,
    county_dropdown,
    fiscal_year,
    mo,
    requests,
    search_button,
    tax_limit_input,
):
    mo.stop(not search_button.value, mo.md("*Press **Search** to run.*"))

    custom_county = county_dropdown.value
    custom_budget = budget_input.value
    custom_tax_limit = tax_limit_input.value

    custom_county_towns = []
    _page = 1

    while True:
        _reply = requests.get(
            "https://oim.zhili.dev/ma/towns",
            params={"county": custom_county, "per_page": 100, "page": _page},
            timeout=10,
        ).json()

        custom_county_towns.extend(_reply["items"])

        if not _reply["pagination"]["has_next"]:
            break
        _page += 1

    custom_town_records = []
    for _town in custom_county_towns:
        _history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{_town['dor_code']}/history",
            timeout=10,
        ).json()

        _year_data = None
        for _year in _history["years"]:
            if _year["fiscal_year"] == fiscal_year:
                _year_data = _year
                break

        if _year_data is None:
            continue

        custom_town_records.append({
            "name": _town["name"],
            "average_single_family_value_dollars": _year_data["average_single_family_value_dollars"],
            "residential_rate_per_thousand": _year_data["residential_rate_per_thousand"],
            "average_single_family_bill_dollars": _year_data["average_single_family_bill_dollars"],
        })

    custom_qualifying_towns = []
    for _record in custom_town_records:
        if _record["average_single_family_value_dollars"] <= custom_budget and _record["average_single_family_bill_dollars"] < custom_tax_limit:
            custom_qualifying_towns.append(_record)

    custom_qualifying_towns.sort(key=lambda _record: _record["average_single_family_bill_dollars"])

    print(f"Towns in {custom_county} County under ${custom_budget:,} with an annual tax bill under ${custom_tax_limit:,} (fiscal year {fiscal_year})")
    print(f"{'Town':<16} {'Avg. Home Value':>16} {'Tax Rate':>10} {'Avg. Annual Bill':>18}")
    for _town in custom_qualifying_towns:
        print(f"{_town['name']:<16} {_town['average_single_family_value_dollars']:>16,.0f} {_town['residential_rate_per_thousand']:>10.2f} {_town['average_single_family_bill_dollars']:>18,.0f}")
    return


if __name__ == "__main__":
    app.run()
