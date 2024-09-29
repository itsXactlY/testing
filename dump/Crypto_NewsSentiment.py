from fastquant import get_yahoo_data, get_bt_news_sentiment, backtest
data = get_yahoo_data("TSLA", "2020-01-01", "2020-07-04")
sentiments = get_bt_news_sentiment(keyword="tesla", page_nums=3)
backtest("sentiment", data, sentiments=sentiments, senti=0.2)


# from fastquant import get_yahoo_data, get_bt_news_sentiment
# from datetime import datetime, timedelta

# # we get the current date and delta time of 30 days
# current_date = datetime.now().strftime("%Y-%m-%d")
# delta_date = (datetime.now() - timedelta(30)).strftime("%Y-%m-%d")
# data = get_yahoo_data("TSLA", delta_date, current_date)
# sentiments = get_bt_news_sentiment(keyword="tesla", page_nums=3)
# backtest("sentiment", data, sentiments=sentiments, senti=0.2)