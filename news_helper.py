from yahoo_fin import news

def get_latest_headlines(ticker):
    try:
        headlines = news.get_yf_rss(ticker)
        return headlines[:5]  # return top 5 headlines
    except:
        return ["News not available."]
