from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST 
from timedelta import Timedelta 
from finbert_utils import estimate_sentiment

API_KEY = "PKN2E0HQZ380C9ZUCD5V"
API_SECRET = "pFsdSAZwW7YxkUeUCsFmvwbiGQF6sic46Ft5kL95"
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET,
    ## Fake money trading
    "PAPER": True
}

class MLTrader(Strategy): 
    def initialize(self, symbol:str="SPY", cash_at_risk:float=.5):
        self.symbol = symbol
        self.sleeptime = "24H" # Dictates how frequently it trades
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key=API_SECRET)

    def position_sizing(self):
        cash = self.get_cash() # check how much cash in account
        last_price = self.get_last_price(self.symbol)
        # number of shares to buy calc
        quantity = round(cash * self.cash_at_risk / last_price, 0)
        return cash, last_price, quantity


    def get_dates(self): 
        today = self.get_datetime()
        three_days_prior = today - Timedelta(days=3)
        return today.strftime('%Y-%m-%d'), three_days_prior.strftime('%Y-%m-%d')


    def get_sentiment(self): 
        today, three_days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, 
                                 start=three_days_prior, 
                                 end=today)
        news = [ev.__dict__["_raw"]["headline"] for ev in news] # Formats news
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment 

    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() # get amount of cash, price of share and how many shares to buy
        probability, sentiment = self.get_sentiment() # get sentiment and probability that sentiment is correct from


        if cash > last_price: 
            if sentiment == "positive" and probability > .999:
                # if pos and last trade sell. close shorts and place buy
                if self.last_trade == "sell": 
                    self.sell_all()

                # Buy order
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "buy", 
                    type="bracket", 
                    take_profit_price=last_price*1.20, 
                    stop_loss_price=last_price*.95
                )
                self.submit_order(order) 
                self.last_trade = "buy"



            elif sentiment == "negative" and probability > .999:
                # if neg and last trade buy, close long place short
                if self.last_trade == "buy": 
                    self.sell_all()

                    # Sell order
                order = self.create_order(
                    self.symbol, 
                    quantity, 
                    "sell", 
                    type="bracket", 
                    take_profit_price=last_price*.8, 
                    stop_loss_price=last_price*1.05
                )
                self.submit_order(order) 
                self.last_trade = "sell"


# Backtesting

start_date = datetime(2021,12,1)
end_date = datetime(2024,10,31)
broker = Alpaca(ALPACA_CREDS)
strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol":"SPY", "cash_at_risk":.5})
strategy.backtest(YahooDataBacktesting, start_date, end_date, parameters={"symbol":"SPY", "cash_at_risk":.5})

# runs it for  real
#trader = Trader()
#trader.add_strategy(strategy)
#trader.run_all()
