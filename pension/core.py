from pension.config import MAX_ANNUAL_RECEIPT, MONTHLY_CONTRIBUTION

def determine_annual_receipt_jpy_pension(years_of_contribution: int) -> float:
    """This function calculates the annual receipt for a Japanese pension based on years of contribution."""
    if years_of_contribution > 40:
        raise ValueError("Years of contribution cannot exceed 40.")
    return MAX_ANNUAL_RECEIPT * (years_of_contribution * 12 / 480)

def calculate_present_value_jpy_pension(years_of_contribution: int, interest_rate_schedule: list, years_to_receive: int) -> float:
    """This function calculates the present value of a Japanese pension given annual receipt, interest rate, and years."""
    assert len(interest_rate_schedule) >= years_to_receive, "Interest rate schedule length must be at least years to receive."
    annual_receipt = determine_annual_receipt_jpy_pension(years_of_contribution)
    present_value = 0
    for t in range(0, years_to_receive):
        annual_interest_rate = interest_rate_schedule[t][1]
        present_value += annual_receipt / ((1 + (annual_interest_rate / 100)) ** t)
    return present_value

def determine_future_return_investment(annual_contribution: float, annual_investment_return: float, years_of_investment: int) -> float:
    """This function calculates the future return on an investment given present value, interest rate, and years."""
    return annual_contribution * ((1 + (annual_investment_return / 100)) ** years_of_investment)

def convert_jpy_foreign_currency(value: float, exchange_rate: float) -> float:
    """This function converts the annual contribution amount from JPY to a foreign currency.
    Args:
        value (float): The amount in JPY.
        exchange_rate (float): The exchange rate from JPY to the foreign currency (e.g. 120 JPY = 1 USD)
        or from the foreign currency to JPY (e.g. 0.0083 USD = 1 JPY).
    Returns:
        float: The annual contribution amount in the foreign currency."""
    return value / exchange_rate

def create_schedule(years_of_contribution: int, value: float) -> list:
    """This function creates a schedule over the years to receive."""
    return [(year, value) for year in range(years_of_contribution)]

def calculate_total_investment_return(contribution_schedule: list, return_rate_schedule: list) -> float:
    """This function calculates the total investment return based on contribution and interest rate schedules."""
    assert len(contribution_schedule) == len(return_rate_schedule), "Contribution and interest rate schedules must have the same length."
    total_return = 0
    years = len(contribution_schedule)
    for year in range(0, years):
        annual_contribution = contribution_schedule[year][1]
        annual_investment_return = return_rate_schedule[year][1]
        years_of_investment = years - year
        total_return += determine_future_return_investment(annual_contribution, annual_investment_return, years_of_investment)
    return total_return

def run_one_off_simulation(years_of_contribution: int, years_to_receive: int, annual_interest_rate: float, annual_return: float, exchange_rate: float) -> tuple[float, float]:
    """This function runs a one-off simulation to calculate the present value of Japanese pension and total investment return."""
    interest_rate_schedule = create_schedule(years_to_receive, annual_interest_rate)
    pv_jpy_pension = calculate_present_value_jpy_pension(years_of_contribution, interest_rate_schedule, years_to_receive)

    contribution_schedule = create_schedule(years_of_contribution, convert_jpy_foreign_currency(MONTHLY_CONTRIBUTION * 12, exchange_rate))
    return_rate_schedule = create_schedule(years_of_contribution, annual_return)
    total_investment_return = calculate_total_investment_return(contribution_schedule, return_rate_schedule)
    total_investment_return_jpy = convert_jpy_foreign_currency(total_investment_return, 1 / exchange_rate)

    return pv_jpy_pension, total_investment_return_jpy

