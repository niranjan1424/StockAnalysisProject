import pandas as pd

# 1. Moving Averages
def add_moving_averages(df, short_window=20, long_window=50):
    df['MA20'] = df['Close'].rolling(window=short_window).mean()
    df['MA50'] = df['Close'].rolling(window=long_window).mean()
    return df

# 2. Relative Strength Index (RSI)
def add_rsi(df, period=14):
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    return df

# 3. Bollinger Bands
def add_bollinger_bands(df, window=20):
    rolling_mean = df['Close'].rolling(window).mean()
    rolling_std = df['Close'].rolling(window).std()
    df['BB_upper'] = rolling_mean + (2 * rolling_std)
    df['BB_lower'] = rolling_mean - (2 * rolling_std)
    return df

# 4. Volume Spike Detector
def add_volume_spike(df, spike_multiplier=1.5):
    avg_volume = df['Volume'].rolling(window=20).mean()
    df['Volume_Spike'] = df['Volume'] > (avg_volume * spike_multiplier)
    return df
