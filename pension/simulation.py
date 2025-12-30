import numpy as np
import matplotlib.pyplot as plt

from pension.core import (
    calculate_present_value_jpy_pension, 
    calculate_total_investment_return, 
    convert_jpy_foreign_currency,
)

from pension.config import MONTHLY_CONTRIBUTION

def freedman_diaconis_bins(data: list) -> int:
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
    results = []

    for _ in range(n_simulations):
        interest_rates = np.random.normal(
            interest_rate_mean,
            interest_rate_sd,
            years_to_receive,
        )
        exchange_rates = np.random.normal(
            exchange_rate_mean,
            exchange_rate_sd,
            years_of_contribution,
        )
        returns = np.random.normal(
            return_mean,
            return_sd,
            years_of_contribution,
        )

        interest_rate_schedule = list(enumerate(interest_rates))
        exchange_rate_schedule = list(enumerate(exchange_rates))
        return_rate_schedule = list(enumerate(returns))
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
    ax1.hist(pensions, bins=bins_pensions, density=True, alpha=0.5, label="Pensions")
    ax2.hist(investments, bins=bins_investments, density=True, alpha=0.5, label="Investments", color="orange")
    ax1.set_xlabel("Total Amount (JPY)")
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

    return fig, pension_better_ratio