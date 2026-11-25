# zahrang.github.io

Personal portfolio site for Zahra Goraya, served at <https://zahrang.github.io/> via GitHub Pages.

It is plain HTML and CSS with no framework or build step. Every page links to the shared `style.css`, and any page-specific rules sit in a small `<style>` block on that page.

| Page | Contents |
|------|----------|
| `index.html` | About / home page with selected work |
| `Projects.html` | All projects |
| `Project1.html` | Stock Portfolio Tracker |
| `Project2.html` | Bond Pricing & Yield Analysis |
| `dissertation.html` | Dissertation overview and progress |
| `contact.html` | Contact links |
| `GitHub_Projects.html` | Redirects to `Projects.html` (kept so old links still work) |

## Generating the charts

The charts in `images/` and the figures quoted on the project pages come from two Python scripts. Run them from the repo root:

```bash
pip install -r requirements.txt
python generate_images.py        # Stock Portfolio Tracker
python generate_bond_project.py  # Bond Pricing & Yield Analysis
```

- **`generate_images.py`** reads tickers, weights and the date range from `portfolio.csv`, then downloads adjusted prices from Yahoo Finance (`yfinance`) along with SPY as an S&P 500 benchmark. It saves the price, cumulative-return, rolling-volatility and correlation charts, and prints total return, annualised volatility, Sharpe ratio, max drawdown and correlations. The risk-free rate is set at the top of the script.
- **`generate_bond_project.py`** prices 3% and 6% coupon 10-year bonds. It prints Macaulay and modified duration, convexity, and duration-based price estimates compared with exact repricing for ±1% yield shifts, and saves the price/yield, price/maturity and duration-vs-convexity charts.

If you rerun the scripts, update the tables on `Project1.html` and `Project2.html` to match the printed output.
