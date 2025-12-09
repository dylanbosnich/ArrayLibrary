class Candle:
    def __init__(self, timeframe, time, open_, high, low, close):
        self.timeframe = timeframe
        self.time = time          # see OHLC for how this is set
        self.open = float(open_)
        self.high = float(high)
        self.low = float(low)
        self.close = float(close)

    def __repr__(self):
        return (
            f"Candle(tf={self.timeframe}, time={self.time}, "
            f"o={self.open}, h={self.high}, l={self.low}, c={self.close})"
        )
