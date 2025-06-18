def backtest_strategy(df, holding_days=10, min_score=4.5, stop_loss_pct=5, take_profit_pct=10):
    results = []
    df = df.copy()
    df = df.dropna()

    for i in range(len(df) - holding_days):
        row = df.iloc[i]

        if row['Score'] >= min_score:
            buy_date = df.index[i]
            buy_price = row['Close']
            max_hold_price = buy_price * (1 + take_profit_pct / 100)
            min_hold_price = buy_price * (1 - stop_loss_pct / 100)

            # simulate next 10 days
            sell_price = df.iloc[i + holding_days]['Close']
            for j in range(1, holding_days):
                day_price = df.iloc[i + j]['Close']
                if day_price >= max_hold_price:
                    sell_price = max_hold_price
                    break
                elif day_price <= min_hold_price:
                    sell_price = min_hold_price
                    break

            return_pct = ((sell_price - buy_price) / buy_price) * 100

            results.append({
                'Buy Date': buy_date.strftime('%Y-%m-%d'),
                'Buy Price': round(buy_price, 2),
                'Sell Price': round(sell_price, 2),
                'Return (%)': round(return_pct, 2)
            })

    return results
