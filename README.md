# 📈 Risk-Return Analyser

A beginner-friendly Python project that calculates and visualises risk-adjusted returns for selected ETFs.

---

## 🎯 Project Purpose

This tool demonstrates understanding of **risk vs return** by comparing performance metrics such as cumulative return, volatility, and Sharpe ratio across benchmark ETFs like SPY, QQQ, and VUKE.

It was built as a learning project and professional asset to showcase:
- Python data analysis skills
- Interest in financial markets
- Application of key investment concepts

---

## 🔍 Features

- Pulls historical ETF data using `yfinance`
- Calculates:
  - Annualised return
  - Volatility
  - Sharpe Ratio (risk-free rate = 2%)
- Visualises cumulative return of all ETFs
- Saves output charts for sharing or reporting

---

## 📦 Libraries Used

- `yfinance`
- `pandas`
- `numpy`
- `matplotlib`
- `os` (built-in)

---

## 🚀 How to Run

1. Install the required libraries:

   ```bash
   pip3 install -r requirements.txt
