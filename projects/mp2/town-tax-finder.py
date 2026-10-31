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

    A couple house-hunting for a single-family home would use this tool to narrow down which towns in a county are actually within their budget, before they start touring homes. Given a maximum home price and a maximum annual property tax bill they're willing to pay, the tool returns every town that fits both, ranked from the cheapest tax bill to the most expensive, so they know where to start looking. They can change the county, the budget, or the tax limit and get a fresh answer without touching any code.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 2. My Plan Before AI

    1. **Set the inputs:** Start with Middlesex County, a $700,000 home budget, an $8,000 annual property tax limit, and fiscal year 2026.

    2. **Get the data:** Write a function that gets all towns in a given county from the Massachusetts API, checking the pagination information to make sure no towns are missing.

    3. **Find the tax information:** Write a second function that takes one town's `dor_code` and a fiscal year, and returns that town's average single-family home value, residential tax rate, and average property tax bill for that year.

    4. **Filter the towns:** Use `if` statements to check whether each town meets both the home budget and property tax requirements.

    5. **Sort the results:** Store the qualifying towns in a list and sort them by annual property tax bill, from lowest to highest.

    6. **Display the results:** Print a table showing each qualifying town's name, average home value, residential tax rate, and average annual tax bill. Print a sentence summarizing the best option from an f-string, so it updates when the data does.

    7. **Make the program reusable:** Allow users to change the county, budget, and tax limit to run the comparison again.

    **Which functions will your tool need? For each, what goes in and what comes out?**
    - `get_county_towns(county)` — takes a county name, returns a list of every town record in that county (looping through every page the API sends).
    - `get_town_tax_record(dor_code, fiscal_year)` — takes a town's code and a year, returns that one town's home value, tax rate and bill for that year, or `None` if that year isn't on file.

    **Which addresses will they request?**
    - `https://oim.zhili.dev/ma/towns?county=...&page=...&per_page=100` for the list of towns in a county.
    - `https://oim.zhili.dev/ma/towns/{dor_code}/history` for one town's year-by-year tax history.

    **How will you know you have every record?**
    The towns endpoint reports a `pagination` field with `total` and `has_next`. I keep requesting pages until `has_next` is `false`, then compare `len(county_towns)` against `pagination["total"]` to confirm nothing was missed.

    **Which check will you use in section 6, and which two numbers should agree?**
    For one town in the result table, I will compute its bill a second way: average home value × tax rate ÷ 1,000, and compare that to the bill the API reports directly. The two should be very close.
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
    county = "Norfolk"
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
    def get_county_towns(county):
        """Return every town record for a county, paging through the API until none are left."""
        towns = []
        page = 1

        while True:
            reply = requests.get(
                "https://oim.zhili.dev/ma/towns",
                params={"county": county, "per_page": 100, "page": page},
                timeout=10,
            ).json()

            towns.extend(reply["items"])

            if not reply["pagination"]["has_next"]:
                break
            page += 1

        return towns


    county_towns = get_county_towns(county)
    len(county_towns), county_towns[0]["name"]
    return (county_towns,)


@app.cell
def _(county_towns, fiscal_year, requests):
    def get_town_tax_record(dor_code, fiscal_year):
        """Return one town's home value, tax rate and bill for a fiscal year, or None if that year isn't on file."""
        history = requests.get(
            f"https://oim.zhili.dev/ma/towns/{dor_code}/history",
            timeout=10,
        ).json()

        for year in history["years"]:
            if year["fiscal_year"] == fiscal_year:
                return {
                    "average_single_family_value_dollars": year["average_single_family_value_dollars"],
                    "residential_rate_per_thousand": year["residential_rate_per_thousand"],
                    "average_single_family_bill_dollars": year["average_single_family_bill_dollars"],
                }

        return None


    town_records = []
    skipped_towns = []

    for _town in county_towns:
        _tax_record = get_town_tax_record(_town["dor_code"], fiscal_year)

        if _tax_record is None:
            skipped_towns.append(_town["name"])
            continue

        town_records.append({"name": _town["name"], **_tax_record})

    len(town_records), skipped_towns
    return (town_records,)


@app.cell
def _(town_records):
    import csv
    import os

    os.makedirs("projects/mp2/data", exist_ok=True)
    town_records_csv = "projects/mp2/data/middlesex-town-tax-records.csv"

    csv_columns = [
        "name",
        "average_single_family_value_dollars",
        "residential_rate_per_thousand",
        "average_single_family_bill_dollars",
    ]

    with open(town_records_csv, "w", newline="", encoding="utf-8") as _file:
        _writer = csv.DictWriter(_file, fieldnames=csv_columns, extrasaction="ignore")
        _writer.writeheader()
        _writer.writerows(town_records)

    town_records_csv
    return


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

    cheapest_town = qualifying_towns[0]
    print()
    print(
        f"In {county} County, {len(qualifying_towns)} towns have an average single-family home value of "
        f"${budget_dollars:,} or less and an average annual property tax bill under ${tax_limit_dollars:,} "
        f"for fiscal year {fiscal_year}, with {cheapest_town['name']} offering the lowest average bill at "
        f"${cheapest_town['average_single_family_bill_dollars']:,}."
    )
    return (cheapest_town,)


@app.cell
def _(mo):
    mo.md(r"""
    # 6. How I Know These Numbers Are Right

    For the cheapest town in the table, I compute its average bill a second way: average home value × residential tax rate ÷ 1,000. This should come out very close to the bill the API reports directly.
    """)
    return


@app.cell
def _(cheapest_town):
    cheapest_town_bill_check = round(
        cheapest_town["average_single_family_value_dollars"] * cheapest_town["residential_rate_per_thousand"] / 1000,
        2,
    )

    print(f"{cheapest_town['name']}: bill reported by the API is ${cheapest_town['average_single_family_bill_dollars']:,}")
    print(f"{cheapest_town['name']}: value x rate / 1,000 works out to ${cheapest_town_bill_check:,.2f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 7. Working With the Agent

    My agent's first draft of `get_county_towns` did not check `pagination["has_next"]` at all — it just requested one page and stopped, which silently would have dropped towns past the first 100 in any county larger than that. I asked it to add the pagination check and verify the count against `pagination["total"]`. I confirmed the fix by comparing `len(county_towns)` to the `total` the API reports for Middlesex (54), which matched. See the cell defining `get_county_towns` in section 4.

    For `get_town_tax_record`, the agent's first version returned the whole `history` dictionary instead of just the one year's figures, which would have made the filtering code in section 4 more complicated than it needed to be. I asked it to loop through `history["years"]` and return only the one matching `fiscal_year`, or `None` if that year is missing — which is also what let me catch towns with no fiscal-2026 data in `skipped_towns`, rather than crashing on them.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 8. Reading It Back

    **`get_county_towns(county)`** — goes in: a county name, as text. Comes out: a list of every town record in that county, each one a dictionary with fields like `name`, `dor_code`, `population`, and so on. One line I had to ask about: `reply["pagination"]["has_next"]` — I didn't know at first that the API's own reply tells you whether there's another page, so the loop knows when to stop instead of guessing a fixed number of pages.

    **`get_town_tax_record(dor_code, fiscal_year)`** — goes in: one town's code and the year I want. Comes out: a small dictionary with that town's home value, tax rate, and bill for that year, or `None` if that year isn't on file. One line I had to ask about: `return None` with no value after it — I hadn't used a function that could return "nothing found" before, and I asked why that was better than just leaving the town out silently. The answer: returning `None` lets the calling code decide what to do (here, record it in `skipped_towns`) instead of hiding the gap.

    **My prediction.** I will change `county` in the Inputs cell from `"Middlesex"` to `"Norfolk"`. I expect the number of qualifying towns to change, since Norfolk has different towns with different home values and tax bills than Middlesex, and I expect the cheapest-bill town in the result table to be a different town entirely, since Malden (the current cheapest) is a Middlesex town and isn't in Norfolk County at all.

    *(Commit this cell with the message `mp2: prediction` before making the change below.)*

    **What happened.** After changing `county` to `"Norfolk"` and rerunning the notebook, the number of qualifying towns dropped from 12 to 7, and the cheapest-bill town changed from Malden ($4,952, Middlesex) to Bellingham ($6,073, Norfolk). Both parts of my prediction were correct: Norfolk has only 28 towns in total against Middlesex's 54, so a smaller county naturally produced a smaller result, and since Malden sits in Middlesex, it could not appear once the county changed. Section 6's check still holds on the new data too: Bellingham's reported bill of $6,073 is very close to its value times its tax rate divided by 1,000 ($6,073.26).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    # 9. Going Further

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


@app.cell
def _(mo):
    mo.md(r"""
    # 10. Time Spent

    Estimate 4 hours (forgot to count)
    """)
    return


if __name__ == "__main__":
    app.run()
