# risk-return-analyser/main.py

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Make sure output directory exists
os.makedirs("output/charts", exist_ok=True)

# ETFs to analyse
tickers = ["SPY", "QQQ", "VUKE.L", "EEM"]

# Download historical data
data = yf.download(tickers, start="2018-01-01", end="2025-01-01", group_by='ticker')

# Extract only the 'Adj Close' price for each ticker
adj_close = data.loc[:, (slice(None), 'Adj Close')]
adj_close.columns = adj_close.columns.droplevel(1)  # Clean up MultiIndex
etf_data = adj_close


# Calculate daily returns
daily_returns = etf_data.pct_change().dropna()

# Cumulative returns
cumulative_returns = (1 + daily_returns).cumprod()

# Annualised metrics
annual_return = daily_returns.mean() * 252
volatility = daily_returns.std() * np.sqrt(252)
sharpe_ratio = (annual_return - 0.02) / volatility  # Assume risk-free rate = 2%

# Plot cumulative returns
plt.figure(figsize=(10,6))
for ticker in cumulative_returns.columns:
    plt.plot(cumulative_returns.index, cumulative_returns[ticker], label=ticker)

plt.title("Cumulative Returns (2018–2025)")
plt.xlabel("Date")
plt.ylabel("Growth of $1")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("output/charts/cumulative_returns.png")
plt.show()

# Print performance summary
summary = pd.DataFrame({
    "Annual Return": annual_return,
    "Volatility": volatility,
    "Sharpe Ratio": sharpe_ratio
}).round(3)

print("\n📊 ETF Risk/Return Summary:")
print(summary)
