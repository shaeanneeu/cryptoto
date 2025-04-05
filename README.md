# Cryptoto

## Project Overview

This repository contains the codes and methodologies for our portfolio trading algorithm. Steps to replicate our project results can be seen below.

All raw data was collected in March 2025 using the Python libraries Yahoo Finance and Tessa.

## Step 0 - Prerequisites

Install `pipx`:

```bash
python -m pip install --user pipx
```

Install `Poetry`:

```bash
pipx install poetry
pipx ensurepath
```

Install dependencies:

```bash
poetry install --no-root
```

For your IDE:

- Remember to select the right interpreter (the poetry one)

Installing packages (example):

```bash
poetry add example-package-here
```

## Step 1 - Run Efficient Frontier (EF)

Our EF notebook `notebooks/efficient_frontier.ipynb` allows us to derive the optimal set of assests and their respective allocations. We tested several objective functions before deciding on **optimising min semideviation** for our target return of 30%. This objective function was chosen for our portfolio to have a greater proportion of crypto assets in our portfolio as per the project instructions.

The EF was also run on both a 1-year window (March 2024 - Feb 2025) and a 2-month window (Jan - Feb 2025).
Results can be found in `data/processed/starting_portfolio.csv` and `data/processed/starting_portfolio_2months.csv` respectively. As a nearer window was a better representation of our testing period (March 2025), we used the EF results from the 2-month window.

## Step 1 - Develop Strategies

Several strategies involving technical indicators were tested by our team. These can be found in `src/strategies`. Each strategy was coded in 2 formats - one to fit the external backtesting library we used (`src/strategies/backtest`) and one for our custom autotrading mechanism (`src/strategies/custom`).

## Step 2 - Time Series

Stationarity checks, ACF/PACF plots and AR modelling were performed on asset data in `notebooks/timeseries.ipynb`. The results can be found in `data/processed/ar_model_2months.csv` (our main file) and `data/processed/ar_model_1year.csv`.

## Step 3 - Backtesting

We used a Python backtesting library [`backtesting.py`](https://kernc.github.io/backtesting.py/) to check the performance of our strategies **at the asset level** within the 2-month window. This allowed us to find the optimal strategy **for each asset**.

This notebook can be found in `notebooks/backtesting.ipynb`. The results of our backtesting can be found in `data/experiments`, with our main result file being `asset_strategies_2_months_with_tpsl.csv`. The other csv files represent our backtesting results when run without Take Profit/Stop Loss or on different timeframes.

## Step 5 - Autotrade

Our portfolio-level autotrading mechanism can be found in `notebooks/autotrade.ipynb`. This file requires the results from AR modelling (`data/processed/ar_model_2months.csv`) and backtesting (`data/experiments/asset_strategies_2_months_with_tpsl.csv`).

Validation period results are saved as `data/misc/daily_portfolio_value_validation.csv` and `data/misc/trade_log_validation.csv`. Testing period results are saved as `data/misc/daily_portfolio_value.csv` and `data/misc/trade_log.csv`.

## Step 6 - Dashboard

A dashboard was created to visualise our results. To run the dashboard, follow the steps below.

Change to correct directory

```bash
cd src
```

Run dashboard in terminal

```bash
streamlit run streamlit_app.py
```
