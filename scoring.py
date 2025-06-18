def generate_score(row):
    score = 0

    # Rule 1: MA20 crosses above MA50 (bullish)
    if row['MA20'] > row['MA50']:
        score += 1

    # Rule 2: RSI below 30 (oversold = potential buy)
    if row['RSI'] < 30:
        score += 1

    # Rule 3: Price near lower Bollinger Band (undervalued)
    if row['Close'] < row['BB_lower']:
        score += 1

    # Rule 4: Volume Spike (unusual activity)
    if row['Volume_Spike']:
        score += 1

    return score
