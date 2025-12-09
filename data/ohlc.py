import yfinance as yf
import pandas as pd
from datetime import timedelta

from data.candle import Candle


class OHLC:
    def __init__(self, symbol, interval):
        self.symbol = symbol
        self.interval = interval

        if interval == "15m":
            period = "60d"
        elif interval in ["1h", "4h"]:
            period = "730d"
        else:
            period = "max"

        raw = yf.download(
            tickers=self.symbol,
            interval=self.interval,
            period=period,
            auto_adjust=False,
            progress=False,
        )

        if isinstance(raw.columns, pd.MultiIndex):
            df = raw.copy()
            df.columns = [str(col[0]) for col in raw.columns]
        else:
            df = raw.copy()
            df.columns = [str(c) for c in raw.columns]

        self.data = df

        idx = df.index
        if not isinstance(idx, pd.DatetimeIndex):
            idx = pd.to_datetime(idx)
        if idx.tz is None:
            idx = idx.tz_localize("UTC")

        idx_nyt = idx.tz_convert("America/New_York")

        candles = []
        for ts_nyt, (_, row) in zip(idx_nyt, df.iterrows()):
            o = row.get("Open")
            h = row.get("High")
            l = row.get("Low")
            c = row.get("Close")

            if pd.isna(o) or pd.isna(h) or pd.isna(l) or pd.isna(c):
                continue

            if self.interval in ["15m", "1h", "4h"]:
                # NY clock time, but drop tzinfo so no "-05:00" prints
                time_value = ts_nyt.replace(tzinfo=None)
            elif self.interval == "1d":
                # session day = date of the 00:00 candle in the 17:00–17:00 NYT day
                time_value = (ts_nyt + timedelta(hours=7)).date()
            elif self.interval == "1wk":
                # weekly: Monday date for that session week
                shifted = ts_nyt + timedelta(hours=7)
                d = shifted.date()
                monday = d - timedelta(days=d.weekday())
                time_value = monday
            else:
                time_value = ts_nyt.replace(tzinfo=None)

            candles.append(
                Candle(self.interval, time_value, o, h, l, c)
            )

        self.candles = candles


TIMEFRAMES = ["15m", "1h", "4h", "1d", "1wk"]

ohlc_by_timeframe = {
    tf: OHLC("EURUSD=X", tf)
    for tf in TIMEFRAMES
}
