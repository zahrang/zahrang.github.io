import os
import numpy as np
import matplotlib.pyplot as plt

# Create images folder if it doesn't exist
os.makedirs("images", exist_ok=True)

# Bond pricing function
def bond_price(face, coupon_rate, maturity, y):
    coupon = face * coupon_rate
    price = sum([coupon / (1 + y)**t for t in range(1, maturity + 1)])
    price += face / (1 + y)**maturity
    return price

# Parameters
face = 100
maturity = 10

# Yield range
yields = np.linspace(0.01, 0.10, 100)

# Low vs High coupon
low_coupon = 0.03
high_coupon = 0.06

# Price vs Yield
low_prices = [bond_price(face, low_coupon, maturity, y) for y in yields]
high_prices = [bond_price(face, high_coupon, maturity, y) for y in yields]

plt.figure()
plt.plot(yields * 100, low_prices, label="Low Coupon Bond (3%)")
plt.plot(yields * 100, high_prices, label="High Coupon Bond (6%)")
plt.xlabel("Yield (%)")
plt.ylabel("Bond Price")
plt.title("Bond Price vs Yield")
plt.legend()
plt.grid()
plt.savefig("images/bond_price_vs_yield.png")
plt.close()

# Price vs Maturity
maturities = range(1, 21)
yield_rate = 0.05

low_prices_m = [bond_price(face, low_coupon, m, yield_rate) for m in maturities]
high_prices_m = [bond_price(face, high_coupon, m, yield_rate) for m in maturities]

plt.figure()
plt.plot(maturities, low_prices_m, label="Low Coupon Bond (3%)")
plt.plot(maturities, high_prices_m, label="High Coupon Bond (6%)")
plt.xlabel("Years to Maturity")
plt.ylabel("Bond Price")
plt.title("Bond Price vs Maturity (5% Yield)")
plt.legend()
plt.grid()
plt.savefig("images/bond_price_vs_maturity.png")
plt.close()

print("Images generated successfully!")
