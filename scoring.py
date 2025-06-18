def generate_score(row):
    score = 0.0

    # Weighted MA crossover (more reliable)
    if row['MA20'] > row['MA50']:
        score += 2.0

    # RSI < 30 (oversold)
    if row['RSI'] < 30:
        score += 1.5

    # Price below Bollinger Band lower
    if row['Close'] < row['BB_lower']:
        score += 1.5

    # Volume Spike
    if row['Volume_Spike']:
        score += 1.0

    return score
