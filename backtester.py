def backtest_strategy(df, holding_days=10, min_score=3):
    results = []
    df = df.copy()

    for current_day in range(len(df) - holding_days):
        row = df.iloc[current_day]
        if row['Score'] >= min_score:
            buy_date = df.index[current_day]
            buy_price = row['Close']
            sell_price = df.iloc[current_day + holding_days]['Close']
            sell_date = df.index[current_day + holding_days]
            pct_return = ((sell_price - buy_price) / buy_price) * 100

            results.append({
                'Buy Date': buy_date,
                'Buy Price': round(buy_price, 2),
                'Sell Date': sell_date,
                'Sell Price': round(sell_price, 2),
                'Return (%)': round(pct_return, 2)
            })

    return results
