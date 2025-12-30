import numpy as np

from pension.config import MAX_ANNUAL_RECEIPT

def determine_annual_receipt_jpy_pension(years_of_contribution: int) -> float:
    """This function calculates the annual receipt for a Japanese pension based on years of contribution.
    Args:
        years_of_contribution (int): The number of years the individual has contributed to the pension.
    Returns:
        float: The annual receipt amount for the Japanese pension."""
    if years_of_contribution > 40:
        raise ValueError("Years of contribution cannot exceed 40.")
    return MAX_ANNUAL_RECEIPT * (years_of_contribution * 12 / 480)

def calculate_present_value_jpy_pension(years_of_contribution: int, interest_rate_schedule: list, years_to_receive: int) -> float:
    """This function calculates the present value of a Japanese pension given annual receipt, interest rate, and years.
    Args:
        years_of_contribution (int): The number of years the individual has contributed to the pension.
        interest_rate_schedule (list): A list of tuples containing (year, interest rate) for each year of pension receipt.
        years_to_receive (int): The number of years the individual will receive the pension.
    Returns:
        float: The present value of the Japanese pension."""
    assert len(interest_rate_schedule) >= years_to_receive, "Interest rate schedule length must be at least years to receive."
    annual_receipt = determine_annual_receipt_jpy_pension(years_of_contribution)
    present_value = 0
    for t in range(0, years_to_receive):
        annual_interest_rate = interest_rate_schedule[t][1]
        present_value += annual_receipt / ((1 + (annual_interest_rate / 100)) ** t)
    return present_value

def determine_future_return_investment(annual_contribution: float, annual_investment_return: float, years_of_investment: int) -> float:
    """This function calculates the future return on an investment given present value, interest rate, and years.
    Args:
        annual_contribution (float): The annual contribution amount.
        annual_investment_return (float): The annual investment return rate (as a percentage).
        years_of_investment (int): The number of years the investment is held.
    Returns:
        float: The future value of the investment."""
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

def calculate_total_investment_return(contribution_schedule: list, return_rate_schedule: list) -> float:
    """This function calculates the total investment return based on contribution and interest rate schedules.
    Args:
        contribution_schedule (list): A list of tuples containing (year, annual contribution in foreign currency).
        return_rate_schedule (list): A list of tuples containing (year, annual investment return rate as a percentage).
    Returns:
        float: The total investment return."""
    assert len(contribution_schedule) == len(return_rate_schedule), "Contribution and interest rate schedules must have the same length."
    total_return = 0
    years = len(contribution_schedule)
    for year in range(0, years):
        annual_contribution = contribution_schedule[year][1]
        annual_investment_return = return_rate_schedule[year][1]
        years_of_investment = years - year
        total_return += determine_future_return_investment(annual_contribution, annual_investment_return, years_of_investment)
    return total_return

def create_schedule(mean: float, sd: float, years: int, rng: np.random.Generator) -> list:
    """This function creates a schedule of values based on a normal distribution.
    Args:
        mean (float): The mean value.
        sd (float): The standard deviation.
        years (int): The number of years to generate values for.
    Returns:
        list: A list of tuples containing (year, value) for each year."""
    values = rng.normal(mean, sd, years)
    return list(enumerate(values))