"""Bond Pricing & Yield Analysis: charts and duration/convexity figures.

Prices two 10-year bonds with annual coupons (3% and 6%, face value 100),
computes Macaulay duration, modified duration and convexity at a 5% yield,
and compares the price change predicted by duration (and duration +
convexity) with the exact repriced change for a +/-1% yield shift.

Run from the repo root:  python generate_bond_project.py
"""

import os

import matplotlib.pyplot as plt
import numpy as np

os.makedirs("images", exist_ok=True)

COLOURS = {"low": "#257de0", "high": "#f47230"}
plt.rcParams.update({
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": "#e5e5e5",
    "grid.linewidth": 0.8,
    "axes.edgecolor": "#999999",
    "legend.frameon": False,
})


# --------------------------
# Bond maths (annual coupons, yield y as a decimal)
# --------------------------
def cash_flows(face, coupon_rate, maturity):
    t = np.arange(1, maturity + 1)
    cf = np.full(maturity, face * coupon_rate, dtype=float)
    cf[-1] += face
    return t, cf


def bond_price(face, coupon_rate, maturity, y):
    t, cf = cash_flows(face, coupon_rate, maturity)
    return float(np.sum(cf / (1 + y) ** t))


def macaulay_duration(face, coupon_rate, maturity, y):
    t, cf = cash_flows(face, coupon_rate, maturity)
    pv = cf / (1 + y) ** t
    return float(np.sum(t * pv) / np.sum(pv))


def modified_duration(face, coupon_rate, maturity, y):
    return macaulay_duration(face, coupon_rate, maturity, y) / (1 + y)


def convexity(face, coupon_rate, maturity, y):
    t, cf = cash_flows(face, coupon_rate, maturity)
    pv = cf / (1 + y) ** t
    return float(np.sum(t * (t + 1) * pv) / (np.sum(pv) * (1 + y) ** 2))


# --------------------------
# Parameters
# --------------------------
face = 100
maturity = 10
base_yield = 0.05
shift = 0.01
bonds = {"low": ("Low Coupon Bond (3%)", 0.03), "high": ("High Coupon Bond (6%)", 0.06)}

# --------------------------
# Duration / convexity table
# --------------------------
print(f"{maturity}-year bonds, face {face}, annual coupons, base yield {base_yield:.0%}\n")
results = {}
for key, (label, c) in bonds.items():
    p0 = bond_price(face, c, maturity, base_yield)
    mac = macaulay_duration(face, c, maturity, base_yield)
    mod = modified_duration(face, c, maturity, base_yield)
    conv = convexity(face, c, maturity, base_yield)
    results[key] = (p0, mod, conv)
    print(f"{label}: price {p0:.2f}, Macaulay {mac:.2f} yrs, "
          f"modified {mod:.2f}, convexity {conv:.1f}")
    for dy in (+shift, -shift):
        actual = bond_price(face, c, maturity, base_yield + dy) / p0 - 1
        dur = -mod * dy
        dur_conv = dur + 0.5 * conv * dy ** 2
        print(f"   yield {dy:+.0%}: actual {actual:+.2%} | duration {dur:+.2%} "
              f"(error {dur - actual:+.2%}) | duration+convexity {dur_conv:+.2%} "
              f"(error {dur_conv - actual:+.3%})")
    print()

yields = np.linspace(0.01, 0.10, 100)

# --------------------------
# Plot: Price vs Yield
# --------------------------
plt.figure()
for key, (label, c) in bonds.items():
    plt.plot(yields * 100, [bond_price(face, c, maturity, y) for y in yields],
             label=label, color=COLOURS[key], linewidth=2)
plt.xlabel("Yield (%)")
plt.ylabel("Bond Price")
plt.title(f"Bond Price vs Yield ({maturity}-year bonds)")
plt.legend()
plt.tight_layout()
plt.savefig("images/bond_price_vs_yield.png")
plt.close()

# --------------------------
# Plot: Price vs Maturity
# --------------------------
maturities = range(1, 21)
plt.figure()
for key, (label, c) in bonds.items():
    plt.plot(maturities, [bond_price(face, c, m, base_yield) for m in maturities],
             label=label, color=COLOURS[key], linewidth=2)
plt.axhline(face, color="#999999", linewidth=0.8)
plt.xlabel("Years to Maturity")
plt.ylabel("Bond Price")
plt.title(f"Bond Price vs Maturity ({base_yield:.0%} Yield)")
plt.legend()
plt.tight_layout()
plt.savefig("images/bond_price_vs_maturity.png")
plt.close()

# --------------------------
# Plot: Duration vs duration + convexity approximation (low coupon bond)
# --------------------------
label, c = bonds["low"]
p0, mod, conv = results["low"]
dys = np.linspace(-0.03, 0.03, 121)
exact = np.array([bond_price(face, c, maturity, base_yield + d) for d in dys])
dur_line = p0 * (1 - mod * dys)
dur_conv_line = p0 * (1 - mod * dys + 0.5 * conv * dys ** 2)

plt.figure(figsize=(8, 5))
plt.plot((base_yield + dys) * 100, exact, color="#000000", linewidth=2.5, label="Exact price")
plt.plot((base_yield + dys) * 100, dur_line, color=COLOURS["low"], linewidth=2,
         linestyle="--", label="Duration (linear)")
plt.plot((base_yield + dys) * 100, dur_conv_line, color=COLOURS["high"], linewidth=2,
         linestyle=":", label="Duration + convexity")
plt.scatter([base_yield * 100], [p0], color="#000000", s=40, zorder=5)
plt.xlabel("Yield (%)")
plt.ylabel("Bond Price")
plt.title(f"Price Approximations Around {base_yield:.0%} Yield ({label})")
plt.legend()
plt.tight_layout()
plt.savefig("images/bond_duration_convexity.png")
plt.close()

print("Images generated successfully!")
