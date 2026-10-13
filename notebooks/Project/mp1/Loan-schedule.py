# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
# ]
# ///
"""Mini Project 1.
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium", sql_output="polars")


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Mini Project 1

    Your choice of option, what each one asks for, the due date and how it is graded are on the Mini Project 1 page of the course site, linked from the calendar. This notebook is the shape to build it in. Keep the headings, and replace each line in italics with your own.

    Save it in your course repository as `projects/mp1/<your-tool>.py`, named for what it does, such as `loan-schedule.py`, and open it with `uv run marimo edit`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. The Question

    *Who would use this, and what decision does it help them make? Two or three sentences, in words somebody outside this course would understand.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The tool is designed for homebuyers to compare different mortgage options before making a financial decision. It helps them understand the differences in monthly payments, total interest costs, and repayment timelines between a 15-year and a 30-year mortgage. Users can also adjust interest rates and extra payments to see how these changes affect their overall costs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. My Plan Before AI

    *Before you ask your agent anything, write how you would solve it: the steps, in order, in plain words, in five lines or more. Then answer these two questions:*

    - *What does your loop carry from one step to the next, the way a running total carries its sum?*
    - *Which check will you use in section 6, and which two numbers should agree?*

    *Commit this notebook with the message `mp1: plan before AI`.*
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    1. Define loan amount, interest rates and loan terms in months.
    2. Calculate fixed monthly payment using provided formula.
    3. Create a loop to go through each month of the loan for an amortization schedule to track principal and interest for each payment.
    4. Check if final payment need to be adjusted so the loan balance is exactly 0.
    5. Compare monthly payments and total interest costs between the 15-year and 30-year loans.
    6. Test how an extra $200 monthly payment affects the repayment timeline and total interest.
    7. Explore refinancing scenario.
    8. Visualize the amortization schedules and summarize the results.

    **Question 1:**
    The loop carries the remaining loan balance and accumulated total interest from one month to the next.

    **Question 2:**
    Check if original loan amount equals the total principal paid across all monthly payments.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Inputs

    Every number the project starts from goes in the cell below, and nowhere else, so that changing one input changes every result after it.

    Copy in the default inputs for your option from the Mini Project 1 page. If you chose D, your own option, type your data in here, or ask your agent to generate it with `faker`. The required part reads no file.
    """)
    return


@app.cell
def _():
    home_price = 500000
    down_payment_rate = 0.20
    loan_amount = home_price * (1 - down_payment_rate)
    annual_rates = {30: 0.0703, 15: 0.0642}
    extra_payment = 200
    refinance_after_years = 5
    refinance_rate = 0.06
    refinance_cost = 6000
    return (
        annual_rates,
        extra_payment,
        loan_amount,
        refinance_after_years,
        refinance_cost,
        refinance_rate,
    )


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. The Work

    Add as many cells as you need. Try each step yourself before you ask your agent, and commit as you go.
    """)
    return


@app.cell
def _(annual_rates, loan_amount):
    r_30 = annual_rates[30] / 12
    n_30 = 30 * 12
    monthly_payment_30 = round(loan_amount * r_30 / (1 - (1 + r_30) ** -n_30), 2)

    r_15 = annual_rates[15] / 12
    n_15 = 15 * 12
    monthly_payment_15 = round(loan_amount * r_15 / (1 - (1 + r_15) ** -n_15), 2)

    monthly_payment_30, monthly_payment_15
    return monthly_payment_15, monthly_payment_30, n_15, n_30, r_15, r_30


@app.cell
def _(loan_amount, monthly_payment_30, n_30, r_30):
    schedule_30 = []
    balance_30 = loan_amount
    total_interest_30 = 0

    for _month in range(1, n_30 + 1):
        _interest = round(balance_30 * r_30, 2)
        _principal = monthly_payment_30 - _interest
        _payment = monthly_payment_30

        if balance_30 - _principal < 0 or _month == n_30:
            _principal = balance_30
            _payment = round(_principal + _interest, 2)

        balance_30 = round(balance_30 - _principal, 2)
        total_interest_30 += _interest

        schedule_30.append({
            "month": _month,
            "payment": _payment,
            "interest": _interest,
            "principal": _principal,
            "balance": balance_30,
        })

    schedule_30
    return schedule_30, total_interest_30


@app.cell
def _(loan_amount, monthly_payment_15, n_15, r_15):
    schedule_15 = []
    balance_15 = loan_amount
    total_interest_15 = 0

    for _month in range(1, n_15 + 1):
        _interest = round(balance_15 * r_15, 2)
        _principal = monthly_payment_15 - _interest
        _payment = monthly_payment_15

        if balance_15 - _principal < 0 or _month == n_15:
            _principal = balance_15
            _payment = round(_principal + _interest, 2)

        balance_15 = round(balance_15 - _principal, 2)
        total_interest_15 += _interest

        schedule_15.append({
            "month": _month,
            "payment": _payment,
            "interest": _interest,
            "principal": _principal,
            "balance": balance_15,
        })

    schedule_15
    return schedule_15, total_interest_15


@app.cell
def _(
    monthly_payment_15,
    monthly_payment_30,
    total_interest_15,
    total_interest_30,
):
    total_interest_30_rounded = round(total_interest_30, 2)
    total_interest_15_rounded = round(total_interest_15, 2)

    print(f"30-year loan: monthly payment ${monthly_payment_30:,.2f}, total interest ${total_interest_30_rounded:,.2f}")
    print(f"15-year loan: monthly payment ${monthly_payment_15:,.2f}, total interest ${total_interest_15_rounded:,.2f}")

    if monthly_payment_30 < monthly_payment_15:
        print(f"The 30-year loan has a lower monthly payment, but the 15-year loan saves ${total_interest_30_rounded - total_interest_15_rounded:,.2f} in total interest.")
    return total_interest_15_rounded, total_interest_30_rounded


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Answer

    *A table of your results in the cell below, printed with `print` and f-strings, then one sentence here that answers the question in section 1, with the number in it.*
    """)
    return


@app.cell
def _(
    loan_amount,
    monthly_payment_15,
    monthly_payment_30,
    total_interest_15_rounded,
    total_interest_30_rounded,
):
    total_paid_30 = round(loan_amount + total_interest_30_rounded, 2)
    total_paid_15 = round(loan_amount + total_interest_15_rounded, 2)

    print("Loan comparison")
    print(f"30-year: monthly payment ${monthly_payment_30:,.2f}, total interest ${total_interest_30_rounded:,.2f}, total paid ${total_paid_30:,.2f}")
    print(f"15-year: monthly payment ${monthly_payment_15:,.2f}, total interest ${total_interest_15_rounded:,.2f}, total paid ${total_paid_15:,.2f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    For a $500,000 condo with 20% down, the 15-year mortgage costs $336,906.69 less in total interest than the 30-year mortgage, even though its monthly payment is $797.59 higher.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. How I Know These Numbers Are Right

    *At least one check that reaches a result a second, independent way. Name what you compared and what came out.*
    """)
    return


@app.cell
def _(loan_amount, schedule_15, schedule_30):
    total_principal_30 = 0
    for _row in schedule_30:
        total_principal_30 += _row["principal"]
    total_principal_30 = round(total_principal_30, 2)

    total_principal_15 = 0
    for _row in schedule_15:
        total_principal_15 += _row["principal"]
    total_principal_15 = round(total_principal_15, 2)

    print(f"Original loan amount: ${loan_amount:,.2f}")
    print(f"30-year: sum of principal paid ${total_principal_30:,.2f}")
    print(f"15-year: sum of principal paid ${total_principal_15:,.2f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Working With the Agent

    *Pick one piece of AI output you did not accept as-is. What did it give you, what did you change, and how did you know? Point to the commit or the cell.*

    *If the agent got it right the first time: what did you do to verify that?*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The amortization loops the agent first wrote for the two loans used the same variable names (month, interest, principal, balance) in both cells. Marimo's lint check caught this as a "defined in multiple cells" error before I ran anything, so I asked the agent to give each loop its own private names. I verified the fix by re-running the lint tool, which came back clean, and confirming the total interest figures were unchanged.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Going Further

    *Take at least one step past the main task, in any direction, and use your agent as much as you like. It does not have to work. State what you tried, what you found, and where it is in this notebook.*
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Extra $200 a Month

    Pay an extra $200 every month. How many months, and how much interest, does that save on each loan?
    """)
    return


@app.cell
def _(extra_payment, loan_amount, monthly_payment_30, n_30, r_30):
    schedule_30_extra = []
    balance_30_extra = loan_amount
    total_interest_30_extra = 0

    for _month in range(1, n_30 + 1):
        _interest = round(balance_30_extra * r_30, 2)
        _payment = monthly_payment_30 + extra_payment
        _principal = _payment - _interest

        if balance_30_extra - _principal < 0:
            _principal = balance_30_extra
            _payment = round(_principal + _interest, 2)

        balance_30_extra = round(balance_30_extra - _principal, 2)
        total_interest_30_extra += _interest

        schedule_30_extra.append({
            "month": _month,
            "payment": _payment,
            "interest": _interest,
            "principal": _principal,
            "balance": balance_30_extra,
        })

        if balance_30_extra <= 0:
            break

    total_interest_30_extra = round(total_interest_30_extra, 2)
    months_30_extra = len(schedule_30_extra)
    schedule_30_extra
    return months_30_extra, total_interest_30_extra


@app.cell
def _(extra_payment, loan_amount, monthly_payment_15, n_15, r_15):
    schedule_15_extra = []
    balance_15_extra = loan_amount
    total_interest_15_extra = 0

    for _month in range(1, n_15 + 1):
        _interest = round(balance_15_extra * r_15, 2)
        _payment = monthly_payment_15 + extra_payment
        _principal = _payment - _interest

        if balance_15_extra - _principal < 0:
            _principal = balance_15_extra
            _payment = round(_principal + _interest, 2)

        balance_15_extra = round(balance_15_extra - _principal, 2)
        total_interest_15_extra += _interest

        schedule_15_extra.append({
            "month": _month,
            "payment": _payment,
            "interest": _interest,
            "principal": _principal,
            "balance": balance_15_extra,
        })

        if balance_15_extra <= 0:
            break

    total_interest_15_extra = round(total_interest_15_extra, 2)
    months_15_extra = len(schedule_15_extra)
    schedule_15_extra
    return months_15_extra, total_interest_15_extra


@app.cell
def _(
    months_15_extra,
    months_30_extra,
    n_15,
    n_30,
    total_interest_15_extra,
    total_interest_15_rounded,
    total_interest_30_extra,
    total_interest_30_rounded,
):
    months_saved_30 = n_30 - months_30_extra
    interest_saved_30 = round(total_interest_30_rounded - total_interest_30_extra, 2)

    months_saved_15 = n_15 - months_15_extra
    interest_saved_15 = round(total_interest_15_rounded - total_interest_15_extra, 2)

    print(f"30-year with extra $200/month: paid off in {months_30_extra} months instead of {n_30}, saving {months_saved_30} months and ${interest_saved_30:,.2f} in interest.")
    print(f"15-year with extra $200/month: paid off in {months_15_extra} months instead of {n_15}, saving {months_saved_15} months and ${interest_saved_15:,.2f} in interest.")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Refinancing the 30-Year Loan

    Refinance the 30-year loan: after five years the rate falls to 6%, and refinancing costs $6,000. In which month do the savings overtake the cost?
    """)
    return


@app.cell
def _(monthly_payment_30, refinance_after_years, refinance_rate, schedule_30):
    balance_at_refinance = schedule_30[refinance_after_years * 12 - 1]["balance"]

    r_refi = refinance_rate / 12
    n_refi = (30 - refinance_after_years) * 12
    monthly_payment_refi = round(balance_at_refinance * r_refi / (1 - (1 + r_refi) ** -n_refi), 2)

    monthly_savings = round(monthly_payment_30 - monthly_payment_refi, 2)

    balance_at_refinance, monthly_payment_refi, monthly_savings
    return monthly_savings, n_refi


@app.cell
def _(monthly_savings, n_refi, refinance_cost):
    breakeven_month = None
    cumulative_savings = 0

    for _month in range(1, n_refi + 1):
        cumulative_savings = round(cumulative_savings + monthly_savings, 2)
        if cumulative_savings >= refinance_cost:
            breakeven_month = _month
            break

    print(f"Monthly savings after refinancing: ${monthly_savings:,.2f}")
    print(f"Refinance cost: ${refinance_cost:,.2f}")
    if breakeven_month is not None:
        print(f"The savings overtake the cost in month {breakeven_month} after refinancing.")
    else:
        print("The savings never overtake the cost over the life of the new loan.")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Try Your Own Numbers

    The three sliders below let somebody who does not write code try a different rate for each loan, and a different extra monthly payment. Moving a slider recomputes the monthly payment below it right away.
    """)
    return


@app.cell
def _(annual_rates, extra_payment, mo):
    rate_30_slider = mo.ui.slider(1.0, 12.0, value=annual_rates[30] * 100, step=0.01, label="30-year rate (%)")
    rate_15_slider = mo.ui.slider(1.0, 12.0, value=annual_rates[15] * 100, step=0.01, label="15-year rate (%)")
    extra_payment_slider = mo.ui.slider(0, 1000, value=extra_payment, step=25, label="Extra monthly payment ($)")

    mo.vstack([rate_30_slider, rate_15_slider, extra_payment_slider])
    return extra_payment_slider, rate_15_slider, rate_30_slider


@app.cell
def _(
    extra_payment_slider,
    loan_amount,
    n_15,
    n_30,
    rate_15_slider,
    rate_30_slider,
):
    custom_r_30 = (rate_30_slider.value / 100) / 12
    custom_monthly_payment_30 = round(loan_amount * custom_r_30 / (1 - (1 + custom_r_30) ** -n_30), 2)

    custom_r_15 = (rate_15_slider.value / 100) / 12
    custom_monthly_payment_15 = round(loan_amount * custom_r_15 / (1 - (1 + custom_r_15) ** -n_15), 2)

    print(f"At {rate_30_slider.value:.2f}%, the 30-year payment is ${custom_monthly_payment_30:,.2f}")
    print(f"At {rate_15_slider.value:.2f}%, the 15-year payment is ${custom_monthly_payment_15:,.2f}")
    print(f"With an extra ${extra_payment_slider.value:,.2f} a month, the 30-year payment becomes ${custom_monthly_payment_30 + extra_payment_slider.value:,.2f}")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Charting the Balance Over Time

    The chart below shows the loan balance falling to zero over time, for both the 30-year and the 15-year loan, side by side.
    """)
    return


@app.cell
def _():
    import altair as alt

    return (alt,)


@app.cell
def _(schedule_15, schedule_30):
    combined_schedule = []
    for _row in schedule_30:
        combined_schedule.append({"month": _row["month"], "balance": _row["balance"], "loan": "30-year"})
    for _row in schedule_15:
        combined_schedule.append({"month": _row["month"], "balance": _row["balance"], "loan": "15-year"})
    return (combined_schedule,)


@app.cell
def _(alt, combined_schedule):
    balance_chart = alt.Chart(alt.Data(values=combined_schedule)).mark_line().encode(
        x=alt.X("month:Q", title="Month"),
        y=alt.Y("balance:Q", title="Balance ($)"),
        color=alt.Color("loan:N", title="Loan"),
        tooltip=["loan:N", "month:Q", "balance:Q"],
    ).properties(
        title="Loan Balance Over Time",
        width=600,
        height=350,
    )

    balance_chart
    return


if __name__ == "__main__":
    app.run()
