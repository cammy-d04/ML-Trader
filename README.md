# AI-Driven Algorithmic Trading Bot with Sentiment Analysis
This project is an algorithmic trading bot that autonomously executes trades based on real-time sentiment analysis of financial news. Leveraging Yahoo Finance news data and Alpaca’s paper trading API, the bot evaluates recent headlines, gauges market sentiment using an AI model, and performs trades based on high-confidence sentiment predictions.

# Key Features
Sentiment Analysis: Integrates an AI sentiment analysis model to interpret financial news and generate buy/sell signals based on sentiment (positive/negative) and confidence level.
Automated Trading Execution: Utilizes Alpaca’s API to place trades, with support for bracket orders to set take-profit and stop-loss limits.
Dynamic Position Sizing: Calculates optimal share quantities per trade based on available cash and adjustable risk thresholds.
Backtesting: Validates strategy performance on historical data (2021-2024) with adjustable parameters to refine trading rules (this can be adjusted).

# Tech Stack
Python, Lumibot, Alpaca API, FinBERT Sentiment Analysis
Emphasis on algorithmic trading, data analysis, financial APIs, and AI-driven decision making.

# How to Use
Configure Alpaca API credentials.
Run MLTrader strategy with custom parameters for symbol, risk, and sentiment thresholds.
Backtest using historical data to evaluate performance or connect directly to Alpaca for paper trading.
This project is ideal for exploring sentiment-based trading strategies, financial data analysis, and automated trading workflows in Python.
