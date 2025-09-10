import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --------------------------
# Create images folder if it doesn't exist
# --------------------------
os.makedirs("images", exist_ok=True)

# --------------------------
# Load portfolio CSV
# --------------------------
df = pd.read_csv("portfolio.csv", index_col=0)

# Extract start and end dates
start_date = df.loc["StartDate", "Weight"]
end_date = df.loc["EndDate", "Weight"]

# Extract tickers and weights
tickers = df.index[:-2].tolist()
weights = df["Weight"][:-2].astype(float)
weights = weights / weights.sum()  # normalize if not summing to 1

# --------------------------
# Fetch stock data
# --------------------------
data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)
if isinstance(data.columns, pd.MultiIndex):
    data = data["Close"]

# --------------------------
# Calculate returns
# --------------------------
returns = data.pct_change().dropna()
portfolio_returns = (returns * weights.values).sum(axis=1)
portfolio_cum_returns = (1 + portfolio_returns).cumprod() - 1

# --------------------------
# Plot: Historical Prices
# --------------------------
plt.figure(figsize=(12,6))
for ticker in tickers:
    plt.plot(data.index, data[ticker], label=ticker)
plt.title("Historical Stock Prices")
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.legend()
plt.tight_layout()
plt.savefig("images/historical_prices.png")
plt.close()

# --------------------------
# Plot: Portfolio Cumulative Returns
# --------------------------
plt.figure(figsize=(12,6))
for ticker in tickers:
    plt.plot((1 + returns[ticker]).cumprod() - 1, label=ticker)
plt.plot(portfolio_cum_returns, label="Portfolio", color="black", linewidth=2)
plt.title("Cumulative Returns (Stocks + Portfolio)")
plt.xlabel("Date")
plt.ylabel("Cumulative Return")
plt.legend()
plt.tight_layout()
plt.savefig("images/portfolio_cumulative.png")
plt.close()

# --------------------------
# Plot: Correlation Heatmap
# --------------------------
plt.figure(figsize=(8,6))
sns.heatmap(returns.corr(), annot=True, cmap="viridis")
plt.title("Correlation Between Stocks")
plt.tight_layout()
plt.savefig("images/correlation_heatmap.png")
plt.close()

print("All images generated in 'images/' folder!")
