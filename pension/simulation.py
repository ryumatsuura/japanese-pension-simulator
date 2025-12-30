import numpy as np
import matplotlib.pyplot as plt

from pension.core import (
    calculate_present_value_jpy_pension, 
    calculate_total_investment_return, 
    convert_jpy_foreign_currency,
    create_schedule,
)

from pension.config import MONTHLY_CONTRIBUTION

def freedman_diaconis_bins(data: list) -> int:
    """Calculate the number of bins for a histogram using the Freedman-Diaconis rule.
    Args:
        data (list): The data to be plotted in the histogram.
    Returns:
        int: The number of bins for the histogram."""
    data = np.asarray(data)
    q25, q75 = np.percentile(data, [25, 75])
    iqr = q75 - q25
    bin_width = 2 * iqr * len(data) ** (-1 / 3)

    if bin_width <= 0:
        return 50  # fallback

    return int(np.ceil((data.max() - data.min()) / bin_width))

def run_simulation(
    years_to_receive: int,
    interest_rate_mean: float,
    interest_rate_sd: float,
    years_of_contribution: int,
    exchange_rate_mean: float,
    exchange_rate_sd: float,
    return_mean: float,
    return_sd: float,
    n_simulations: int = 10_000,
):
    """This function runs a simulation to compare Japanese pension present value and investment return.
    Args:
        years_to_receive (int): The number of years the individual will receive the pension.
        interest_rate_mean (float): The mean annual interest rate in Japan (as a percentage).
        interest_rate_sd (float): The standard deviation of the annual interest rate in Japan.
        years_of_contribution (int): The number of years the individual has contributed to the pension.
        exchange_rate_mean (float): The mean exchange rate from JPY to foreign currency.
        exchange_rate_sd (float): The standard deviation of the exchange rate.
        return_mean (float): The mean annual investment return rate (as a percentage).
        return_sd (float): The standard deviation of the annual investment return rate.
        n_simulations (int): The number of simulations to run.
    Returns:
        fig: The matplotlib figure object containing the histogram.
        pension_better_ratio (float): The ratio of simulations where pension present value exceeds investment return.
        mean_pension (float): The mean present value of the pension across simulations.
        mean_investment (float): The mean investment return across simulations."""
    results = []
    rng = np.random.default_rng(seed=42)

    for _ in range(n_simulations):

        interest_rate_schedule = create_schedule(
            interest_rate_mean,
            interest_rate_sd,
            years_to_receive,
            rng,
        )
        exchange_rate_schedule = create_schedule(
            exchange_rate_mean,
            exchange_rate_sd,
            years_of_contribution,
            rng,
        )
        return_rate_schedule = create_schedule(
            return_mean,
            return_sd,
            years_of_contribution,
            rng,
        )
        contribution_schedule = [] 
        for year in range(0, years_of_contribution): 
            annual_contribution = convert_jpy_foreign_currency(MONTHLY_CONTRIBUTION * 12, exchange_rate_schedule[year][1]) 
            contribution_schedule.append((year, annual_contribution)) 

        final_exchange_rate = np.random.normal(
            exchange_rate_mean,
            exchange_rate_sd,
        )

        present_value_of_pension = calculate_present_value_jpy_pension(
            years_of_contribution,
            interest_rate_schedule,
            years_to_receive,
        )
        total_return_of_investment = convert_jpy_foreign_currency(calculate_total_investment_return(
            contribution_schedule,
            return_rate_schedule,
        ), 1 / final_exchange_rate)
        results.append([present_value_of_pension, total_return_of_investment])

    pensions, investments = zip(*results)
    
    bins_pensions = freedman_diaconis_bins(pensions)
    bins_investments = freedman_diaconis_bins(investments)

    fig, ax1 = plt.subplots(figsize=(8, 6))
    ax2 = ax1.twinx()
    ax1.hist(pensions, bins=bins_pensions, density=True, alpha=0.5, label="Pension")
    ax2.hist(investments, bins=bins_investments, density=True, alpha=0.5, label="Investment", color="orange")
    ax1.set_xlabel("Total Amount (¥)")
    ax1.set_ylabel("Pension density")
    ax2.set_ylabel("Investment density")
    ax1.set_title("Japanese Pension vs Investment Return Simulation")
    
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(
        handles1 + handles2,
        labels1 + labels2,
        loc="upper right",
        frameon=True,
    )

    pension_better_ratio = sum(p > i for p, i in results) / n_simulations

    return fig, pension_better_ratio, np.mean(pensions), np.mean(investments)