from colorama import Fore, Style
from lumibot.brokers import Alpaca
from lumibot.strategies.strategy import Strategy
from alpaca_trade_api import REST
from datetime import timedelta
from finbert_utils import estimate_sentiment
import pandas as pd
import colorama

API_KEY = "PKN2E0HQZ380C9ZUCD5V"
API_SECRET = "pFsdSAZwW7YxkUeUCsFmvwbiGQF6sic46Ft5kL95"
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY": API_KEY,
    "API_SECRET": API_SECRET,
    "PAPER": True  # Fake money trading
}


class MLTrader(Strategy):
    def initialize(self, symbol, days):
        self.symbol = symbol
        self.days = days
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def get_dates(self):
        today = self.get_datetime()
        three_days_prior = today - timedelta(days=self.days)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self):
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=three_days_prior, end=today)
        if not news:
            print("No news found for symbol:", self.symbol)
            return None, None
        news = [ev.__dict__["_raw"]["headline"] for ev in news]  # Formats news
        probability, sentiment = estimate_sentiment(news, True, self.symbol)
        return float(probability), sentiment  # Convert probability to float



def main():

    days = int(input("How recent?: "))
    symbols = list(input("Enter symbols seperated by spaces: ").split())

    broker = Alpaca(ALPACA_CREDS)

    data = []
    for symbol in symbols:
        strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol": symbol})
        strategy.initialize(symbol, days)  # Explicitly call initialize
        probability, sentiment = strategy.get_sentiment()
        if probability is not None and sentiment is not None:
            data.append({"Symbol": symbol, "Probability": probability, "Sentiment": sentiment})

    df = pd.DataFrame(data)

    for index, row in df.iterrows():
        color = Fore.CYAN if row["Sentiment"] == "positive" else Fore.RED if row["Sentiment"] == "negative" else Fore.YELLOW
        print("\n")
        print(f"{color}{row['Symbol']} - Probability: {row['Probability']}, Sentiment: {row['Sentiment']}{Style.RESET_ALL}")


if __name__ == "__main__":
    main()
