import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from indicators import add_moving_averages, add_rsi, add_bollinger_bands, add_volume_spike
from scoring import generate_score
from backtester import backtest_strategy


# Fetch data
ticker = 'AAPL'
data = yf.download(ticker, start='2023-01-01', end='2024-12-31', progress=False)

# Check if data is valid
if data is None or data.empty:
    print("Error: Failed to fetch data. Check your ticker symbol or internet connection.")
    exit()

# Save CSV
data.to_csv(f"{ticker}_historical_data.csv")

# Apply indicators
data = add_moving_averages(data)
data = add_rsi(data)
data = add_bollinger_bands(data)
data = add_volume_spike(data)

# Preview result
print(data[['Close', 'MA20', 'MA50', 'RSI', 'BB_upper', 'BB_lower', 'Volume_Spike']].tail())

# ----------- VISUALIZATIONS -----------

# 1. Price with MA20 & MA50
plt.figure(figsize=(14, 6))
plt.plot(data['Close'], label='Close', color='black')
plt.plot(data['MA20'], label='MA20', color='blue', linestyle='--')
plt.plot(data['MA50'], label='MA50', color='red', linestyle='--')
plt.title(f'{ticker} Closing Price with Moving Averages')
plt.legend()
plt.grid(True)
plt.show()

# 2. Bollinger Bands
plt.figure(figsize=(14, 6))
plt.plot(data['Close'], label='Close Price', color='black')
plt.plot(data['BB_upper'], label='Upper Band', color='green', linestyle='--')
plt.plot(data['BB_lower'], label='Lower Band', color='orange', linestyle='--')
plt.fill_between(data.index, data['BB_lower'], data['BB_upper'], color='gray', alpha=0.1)
plt.title(f'{ticker} Bollinger Bands')
plt.legend()
plt.grid(True)
plt.show()

# 3. RSI
plt.figure(figsize=(14, 4))
plt.plot(data['RSI'], label='RSI', color='purple')
plt.axhline(70, color='red', linestyle='--', label='Overbought')
plt.axhline(30, color='green', linestyle='--', label='Oversold')
plt.title(f'{ticker} RSI (Relative Strength Index)')
plt.legend()
plt.grid(True)
plt.show()

# 4. Volume with spikes (clean fix)
plt.figure(figsize=(14, 4))

# Convert explicitly to NumPy arrays to fix Pylance type error
dates = data.index.to_numpy()
volumes = data['Volume'].to_numpy()
spike_dates = data[data['Volume_Spike']].index.to_numpy()
spike_volumes = data[data['Volume_Spike']]['Volume'].to_numpy()

# Plot total volume in gray
plt.bar(dates, volumes, color='gray', label='Volume')

# Plot spike volumes in red
plt.bar(spike_dates, spike_volumes, color='red', label='Spike')

plt.title(f'{ticker} Volume with Spikes Highlighted')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# Apply scoring function
data['Score'] = data.apply(generate_score, axis=1)

# Get the top 5 recent high-score rows
top_signals = data.sort_values(by='Score', ascending=False).tail(5)
print("\n📈 Top Recent Buy Signals (Score >= 3):")
print(top_signals[['Close', 'MA20', 'MA50', 'RSI', 'Score']].tail())

# ---------- BACKTESTING ------------
backtest_results = backtest_strategy(data)

print("\n🔁 Backtest Results (Buy on Score ≥ 3, hold for 10 days):")
for res in backtest_results[-5:]:  # last 5 signals
    print(res)

from news_helper import get_latest_headlines

# Show headlines
print(f"\n📰 Latest News for {ticker}:")
for line in get_latest_headlines(ticker):
    print("-", line)

from ml_model import train_ml_model

# Train ML Model
model, acc = train_ml_model(data)
print(f"\n🤖 ML Model Accuracy (10-day direction): {round(acc * 100, 2)}%")


# Support/Resistance

from indicators import add_support_resistance
data = add_support_resistance(data)
# Support/Resistance plot
plt.figure(figsize=(14, 5))
plt.plot(data['Close'], label='Close', color='black')
plt.plot(data['Support'], label='Support', color='green', linestyle='--')
plt.plot(data['Resistance'], label='Resistance', color='red', linestyle='--')
plt.title(f"{ticker} Support & Resistance Zones")
plt.legend()
plt.grid(True)
plt.show()
