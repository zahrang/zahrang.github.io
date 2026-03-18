import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# -----------------------------
# Bond pricing functions
# -----------------------------
def bond_price(face_value, coupon_rate, years_to_maturity, yield_rate, payments_per_year=1):
    """
    Calculate the price of a plain vanilla coupon bond.

    Parameters
    ----------
    face_value : float
        Redemption value of the bond, e.g. 100.
    coupon_rate : float
        Annual coupon rate as a decimal, e.g. 0.05 for 5%.
    years_to_maturity : int
        Number of years until maturity.
    yield_rate : float
        Annual yield to maturity as a decimal, e.g. 0.04 for 4%.
    payments_per_year : int, optional
        Number of coupon payments per year. Default is 1.

    Returns
    -------
    float
        Present value / price of the bond.
    """
    periods = years_to_maturity * payments_per_year
    coupon_payment = face_value * coupon_rate / payments_per_year
    periodic_yield = yield_rate / payments_per_year

    cashflows = np.full(periods, coupon_payment, dtype=float)
    cashflows[-1] += face_value

    discount_factors = np.array(
        [(1 + periodic_yield) ** (-t) for t in range(1, periods + 1)]
    )

    return float(np.sum(cashflows * discount_factors))


def macaulay_duration(face_value, coupon_rate, years_to_maturity, yield_rate, payments_per_year=1):
    """
    Calculate Macaulay duration.
    """
    periods = years_to_maturity * payments_per_year
    coupon_payment = face_value * coupon_rate / payments_per_year
    periodic_yield = yield_rate / payments_per_year

    cashflows = np.full(periods, coupon_payment, dtype=float)
    cashflows[-1] += face_value

    times = np.arange(1, periods + 1)
    discount_factors = np.array(
        [(1 + periodic_yield) ** (-t) for t in times]
    )
    present_values = cashflows * discount_factors
    price = np.sum(present_values)

    duration_periods = np.sum(times * present_values) / price
    duration_years = duration_periods / payments_per_year

    return float(duration_years)


def modified_duration(face_value, coupon_rate, years_to_maturity, yield_rate, payments_per_year=1):
    """
    Calculate modified duration.
    """
    mac_dur = macaulay_duration(
        face_value, coupon_rate, years_to_maturity, yield_rate, payments_per_year
    )
    periodic_yield = yield_rate / payments_per_year
    return float(mac_dur / (1 + periodic_yield))


# -----------------------------
# Main project generation
# -----------------------------
def main():
    output_dir = "images"
    os.makedirs(output_dir, exist_ok=True)

    # Example bond assumptions
    face_value = 100
    years_to_maturity = 10
    payments_per_year = 1

    # Two example bonds for comparison
    bonds = [
        {"name": "Low Coupon Bond", "coupon_rate": 0.03},
        {"name": "High Coupon Bond", "coupon_rate": 0.06},
    ]

    # Range of yields for plotting
    yields = np.linspace(0.01, 0.10, 100)

    # Store results for summary table
    summary_rows = []

    # ---------------------------------
    # Plot 1: Price vs Yield
    # ---------------------------------
    plt.figure(figsize=(10, 6))

    for bond in bonds:
        prices = [
            bond_price(
                face_value=face_value,
                coupon_rate=bond["coupon_rate"],
                years_to_maturity=years_to_maturity,
                yield_rate=y,
                payments_per_year=payments_per_year,
            )
            for y in yields
        ]

        plt.plot(yields * 100, prices, label=bond["name"])

        # Add summary row at a sample yield of 5%
        sample_yield = 0.05
        price_at_sample = bond_price(
            face_value=face_value,
            coupon_rate=bond["coupon_rate"],
            years_to_maturity=years_to_maturity,
            yield_rate=sample_yield,
            payments_per_year=payments_per_year,
        )
        mac_dur = macaulay_duration(
            face_value=face_value,
            coupon_rate=bond["coupon_rate"],
            years_to_maturity=years_to_maturity,
            yield_rate=sample_yield,
            payments_per_year=payments_per_year,
        )
        mod_dur = modified_duration(
            face_value=face_value,
            coupon_rate=bond["coupon_rate"],
            years_to_maturity=years_to_maturity,
            yield_rate=sample_yield,
            payments_per_year=payments_per_year,
        )

        summary_rows.append({
            "Bond": bond["name"],
            "Coupon Rate (%)": bond["coupon_rate"] * 100,
            "Yield Used (%)": sample_yield * 100,
            "Price": round(price_at_sample, 2),
            "Macaulay Duration (Years)": round(mac_dur, 2),
            "Modified Duration": round(mod_dur, 2),
        })

    plt.xlabel("Yield to Maturity (%)")
    plt.ylabel("Bond Price")
    plt.title("Bond Price vs Yield")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "bond_price_vs_yield.png"), dpi=300)
    plt.close()

    # ---------------------------------
    # Plot 2: Price sensitivity to maturity
    # ---------------------------------
    maturities = np.arange(1, 21)
    comparison_yield = 0.05

    plt.figure(figsize=(10, 6))

    for bond in bonds:
        maturity_prices = [
            bond_price(
                face_value=face_value,
                coupon_rate=bond["coupon_rate"],
                years_to_maturity=int(m),
                yield_rate=comparison_yield,
                payments_per_year=payments_per_year,
            )
            for m in maturities
        ]

        plt.plot(maturities, maturity_prices, label=bond["name"])

    plt.xlabel("Years to Maturity")
    plt.ylabel("Bond Price")
    plt.title("Bond Price vs Maturity at 5% Yield")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, "bond_price_vs_maturity.png"), dpi=300)
    plt.close()

    # ---------------------------------
    # Save summary table
    # ---------------------------------
    summary_df = pd.DataFrame(summary_rows)
    summary_df.to_csv("bond_summary.csv", index=False)

    print("Project files created successfully:")
    print("- images/bond_price_vs_yield.png")
    print("- images/bond_price_vs_maturity.png")
    print("- bond_summary.csv")
    print("\nSummary table:")
    print(summary_df.to_string(index=False))


if __name__ == "__main__":
    main()
