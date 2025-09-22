#!/usr/bin/env python3
"""
Risk-Return Analyser for ETFs
A beginner-friendly tool to analyze and compare ETF performance metrics.

Author: Economics Student
Purpose: Demonstrate risk vs return analysis using Python
"""

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def fetch_etf_data(tickers, period="2y"):
    """
    Fetch historical price data for ETFs
    
    Args:
        tickers (list): List of ETF symbols to analyze
        period (str): Time period for data (default: 2 years)
    
    Returns:
        pandas.DataFrame: Adjusted closing prices for all ETFs
    """
    print(f"📊 Fetching data for {len(tickers)} ETFs: {', '.join(tickers)}")
    
    # Download data using yfinance
    data = yf.download(tickers, period=period, progress=False, auto_adjust=False)['Adj Close']
    
    print(f"✅ Successfully downloaded {len(data)} days of data")
    print(f"📅 Date range: {data.index[0].date()} to {data.index[-1].date()}")
    
    return data

def calculate_metrics(prices, risk_free_rate=0.02):
    """
    Calculate key risk-return metrics for each ETF
    
    Args:
        prices (DataFrame): Historical price data
        risk_free_rate (float): Annual risk-free rate (default: 2%)
    
    Returns:
        pandas.DataFrame: Calculated metrics for each ETF
    """
    print(f"\n🧮 Calculating risk-return metrics...")
    
    # Calculate daily returns
    daily_returns = prices.pct_change().dropna()
    
    # Calculate annualized metrics
    trading_days = 252  # Standard number of trading days per year
    
    # Annualized return (geometric mean)
    annual_return = (1 + daily_returns.mean()) ** trading_days - 1
    
    # Annualized volatility (standard deviation)
    annual_volatility = daily_returns.std() * np.sqrt(trading_days)
    
    # Sharpe ratio (risk-adjusted return)
    sharpe_ratio = (annual_return - risk_free_rate) / annual_volatility
    
    # Create results DataFrame
    metrics = pd.DataFrame({
        'Annual Return': annual_return,
        'Annual Volatility': annual_volatility,
        'Sharpe Ratio': sharpe_ratio
    })
    
    print(f"✅ Metrics calculated for {len(metrics)} ETFs")
    
    return metrics

def create_visualizations(prices, metrics):
    """
    Create and save visualization charts
    
    Args:
        prices (DataFrame): Historical price data
        metrics (DataFrame): Calculated metrics
    """
    print(f"\n📈 Creating visualizations...")
    
    # Create output directory if it doesn't exist
    os.makedirs('output', exist_ok=True)
    
    # Calculate cumulative returns (normalize to 100 at start)
    cumulative_returns = (prices / prices.iloc[0]) * 100
    
    # Create the plot
    plt.figure(figsize=(12, 8))
    
    # Plot cumulative returns for each ETF
    for ticker in cumulative_returns.columns:
        plt.plot(cumulative_returns.index, cumulative_returns[ticker], 
                label=f"{ticker}", linewidth=2)
    
    plt.title('ETF Performance Comparison - Cumulative Returns', fontsize=16)
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Cumulative Return (Base = 100)', fontsize=12)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Save the plot
    plt.savefig('output/etf_performance_comparison.png', dpi=300, bbox_inches='tight')
    print(f"💾 Chart saved: output/etf_performance_comparison.png")
    
    plt.show()

def display_results(metrics):
    """
    Display formatted results table
    
    Args:
        metrics (DataFrame): Calculated metrics
    """
    print(f"\n📋 RISK-RETURN ANALYSIS RESULTS")
    print("=" * 50)
    
    # Format the results for better readability
    formatted_metrics = metrics.copy()
    formatted_metrics['Annual Return'] = formatted_metrics['Annual Return'].apply(lambda x: f"{x:.2%}")
    formatted_metrics['Annual Volatility'] = formatted_metrics['Annual Volatility'].apply(lambda x: f"{x:.2%}")
    formatted_metrics['Sharpe Ratio'] = formatted_metrics['Sharpe Ratio'].apply(lambda x: f"{x:.3f}")
    
    print(formatted_metrics.to_string())
    
    # Find best performing ETF by Sharpe ratio
    best_sharpe = metrics['Sharpe Ratio'].idxmax()
    print(f"\n🏆 Best Risk-Adjusted Return: {best_sharpe} (Sharpe Ratio: {metrics.loc[best_sharpe, 'Sharpe Ratio']:.3f})")
    
    # Save results to CSV
    os.makedirs('output', exist_ok=True)
    metrics.to_csv('output/etf_analysis_results.csv')
    print(f"💾 Results saved: output/etf_analysis_results.csv")

def main():
    """
    Main function to orchestrate the analysis
    """
    print("🚀 Starting ETF Risk-Return Analysis")
    print("=" * 40)
    
    # Define ETFs to analyze (common benchmark ETFs)
    etf_tickers = ['SPY', 'QQQ', 'VTI']  # Using VTI instead of VUKE for reliability
    
    try:
        # Step 1: Fetch data
        price_data = fetch_etf_data(etf_tickers)
        
        # Step 2: Calculate metrics
        metrics = calculate_metrics(price_data)
        
        # Step 3: Create visualizations
        create_visualizations(price_data, metrics)
        
        # Step 4: Display results
        display_results(metrics)
        
        print(f"\n✅ Analysis complete! Check the 'output' folder for saved files.")
        
    except Exception as e:
        print(f"❌ Error during analysis: {str(e)}")
        print("💡 Make sure you have internet connection and try again.")

if __name__ == "__main__":
    main()