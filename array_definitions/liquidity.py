import pandas as pd

class Liquidity:
    def __init__(self, timeframe, name, price, time_label, group=None):
        self.timeframe = timeframe      # "1d", "1h", "15m", etc.
        self.name = name               # "PDH", "PDL", "ARH", "ARL", etc.
        self.price = float(price)      # numeric level
        self.time = time_label         # usually a pd.Timestamp or date
        self.group = group             # "daily", "weekly", "intraday", etc.

    def __repr__(self):
        return (
            f"Liquidity(group={self.group}, tf={self.timeframe}, "
            f"name={self.name}, price={self.price}, time={self.time})"
        )
