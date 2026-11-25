"""Stock Portfolio Tracker: charts and summary metrics.

Reads tickers, weights and the date range from portfolio.csv, downloads
adjusted close prices from Yahoo Finance, then:
  * saves the charts used on Project1.html into images/
  * prints total return over the period, annualised volatility, Sharpe ratio
    and max drawdown for
    the portfolio, each stock and an S&P 500 benchmark, plus pairwise
    correlations of daily returns.

Sharpe ratio = annualised mean daily excess return / annualised volatility,
i.e. mean(r - rf_daily) / std(r) * sqrt(252).

Run from the repo root:  python generate_images.py
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import yfinance as yf

# --------------------------
# Settings
# --------------------------
RISK_FREE_RATE = 0.05   # annual; roughly the average 3-month US T-bill yield in 2023
TRADING_DAYS = 252
BENCHMARK = "SPY"       # S&P 500 ETF (dividend-adjusted, so comparable with the stocks)
ROLLING_WINDOW = 30     # trading days, for the rolling volatility chart

COLOURS = {"AAPL": "#257de0", "TSLA": "#f47230", "MSFT": "#00b894"}
PORTFOLIO_COLOUR = "#000000"
BENCHMARK_COLOUR = "#8a8a8a"

plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#e5e5e5",
    "grid.linewidth": 0.8,
    "axes.edgecolor": "#999999",
    "font.size": 11,
    "legend.frameon": False,
})

os.makedirs("images", exist_ok=True)

# --------------------------
# Load portfolio CSV
# --------------------------
df = pd.read_csv("portfolio.csv", index_col=0)
start_date = df.loc["StartDate", "Weight"]
end_date = df.loc["EndDate", "Weight"]

tickers = df.index[:-2].tolist()
weights = df["Weight"][:-2].astype(float)
weights = weights / weights.sum()  # normalise if not summing to 1

# --------------------------
# Fetch price data (stocks + benchmark)
# --------------------------
# Start a couple of weeks early so the first day's return in the period can be computed
fetch_start = (pd.Timestamp(start_date) - pd.Timedelta(days=14)).strftime("%Y-%m-%d")
fetch_end = (pd.Timestamp(end_date) + pd.Timedelta(days=1)).strftime("%Y-%m-%d")  # end is exclusive
raw = yf.download(tickers + [BENCHMARK], start=fetch_start, end=fetch_end,
                  auto_adjust=True, progress=False, threads=False)
if isinstance(raw.columns, pd.MultiIndex):
    raw = raw["Close"]
missing = [c for c in tickers + [BENCHMARK] if c not in raw or raw[c].dropna().empty]
if missing:
    raise SystemExit(f"Download failed for {missing}; try running again.")

in_period = slice(start_date, end_date)
data = raw[tickers].loc[in_period]

# --------------------------
# Returns
# --------------------------
daily = raw.pct_change().loc[in_period].dropna()
returns = daily[tickers]
bench_returns = daily[BENCHMARK]
# Fixed weights applied to daily returns (i.e. rebalanced daily)
portfolio_returns = (returns * weights[tickers].values).sum(axis=1)

all_returns = returns.copy()
all_returns["Portfolio"] = portfolio_returns
all_returns["S&P 500 (SPY)"] = bench_returns
cumulative = (1 + all_returns).cumprod() - 1


# --------------------------
# Metrics
# --------------------------
def summarise(r: pd.Series) -> dict:
    growth = (1 + r).prod()   # compounded over the period (last close / prior close)
    ann_vol = r.std() * np.sqrt(TRADING_DAYS)
    daily_rf = (1 + RISK_FREE_RATE) ** (1 / TRADING_DAYS) - 1
    sharpe = (r - daily_rf).mean() / r.std() * np.sqrt(TRADING_DAYS)
    wealth = (1 + r).cumprod()
    max_dd = (wealth / wealth.cummax() - 1).min()
    return {
        "Total return": growth - 1,
        "Ann. volatility": ann_vol,
        "Sharpe": sharpe,
        "Max drawdown": max_dd,
    }


metrics = pd.DataFrame({name: summarise(all_returns[name]) for name in all_returns.columns}).T
corr = returns.corr()

pd.set_option("display.width", 120)
print(f"Period: {returns.index[0].date()} to {returns.index[-1].date()} "
      f"({len(returns)} daily returns)")
print("Weights: " + ", ".join(f"{t} {w:.0%}" for t, w in weights.items()))
print(f"Risk-free rate: {RISK_FREE_RATE:.1%} p.a.\n")
fmt = metrics.copy()
for col in ["Total return", "Ann. volatility", "Max drawdown"]:
    fmt[col] = fmt[col].map(lambda x: f"{x:.1%}")
fmt["Sharpe"] = fmt["Sharpe"].map(lambda x: f"{x:.2f}")
print(fmt.to_string(), "\n")
print("Correlation of daily returns:")
print(corr.round(2).to_string())


def finish(path: str) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=110)
    plt.close()


# --------------------------
# Plot: Historical Prices
# --------------------------
plt.figure(figsize=(12, 6))
for t in tickers:
    plt.plot(data.index, data[t], label=t, color=COLOURS.get(t), linewidth=2)
plt.title("Historical Stock Prices (adjusted close)")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
finish("images/historical_prices.png")

# --------------------------
# Plot: Cumulative Returns, with S&P 500 benchmark
# --------------------------
plt.figure(figsize=(12, 6))
for t in tickers:
    plt.plot(cumulative.index, cumulative[t], label=t, color=COLOURS.get(t), linewidth=1.5)
plt.plot(cumulative.index, cumulative["S&P 500 (SPY)"], label="S&P 500 (SPY)",
         color=BENCHMARK_COLOUR, linewidth=2, linestyle="--")
plt.plot(cumulative.index, cumulative["Portfolio"], label="Portfolio",
         color=PORTFOLIO_COLOUR, linewidth=2.5)
plt.axhline(0, color="#999999", linewidth=0.8)
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
plt.title("Cumulative Returns: Stocks, Portfolio and S&P 500")
plt.xlabel("Date")
plt.ylabel("Cumulative return")
plt.legend()
finish("images/portfolio_cumulative.png")

# --------------------------
# Plot: Rolling 30-day annualised volatility
# --------------------------
rolling_vol = all_returns.rolling(ROLLING_WINDOW).std().dropna() * np.sqrt(TRADING_DAYS)
plt.figure(figsize=(12, 6))
for t in tickers:
    plt.plot(rolling_vol.index, rolling_vol[t], label=t, color=COLOURS.get(t), linewidth=1.5)
plt.plot(rolling_vol.index, rolling_vol["S&P 500 (SPY)"], label="S&P 500 (SPY)",
         color=BENCHMARK_COLOUR, linewidth=2, linestyle="--")
plt.plot(rolling_vol.index, rolling_vol["Portfolio"], label="Portfolio",
         color=PORTFOLIO_COLOUR, linewidth=2.5)
plt.ylim(bottom=0)
plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
plt.title(f"Rolling {ROLLING_WINDOW}-Day Volatility (annualised)")
plt.xlabel("Date")
plt.ylabel("Annualised volatility")
plt.legend()
finish("images/rolling_volatility.png")

# --------------------------
# Plot: Correlation Heatmap
# --------------------------
plt.figure(figsize=(8, 6))
sns.heatmap(corr, annot=True, fmt=".2f", cmap="Blues", vmin=0, vmax=1,
            square=True, linewidths=2, linecolor="white", cbar_kws={"label": "Correlation"})
plt.grid(False)
plt.xlabel("")
plt.ylabel("")
plt.title("Correlation of Daily Returns")
finish("images/correlation_heatmap.png")

print("\nAll images generated in 'images/' folder!")
