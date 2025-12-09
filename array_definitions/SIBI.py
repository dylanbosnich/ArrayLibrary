import pandas as pd


class SIBI:
    def __init__(self, timeframe, time, high, low, mid):
        self.timeframe = timeframe
        self.time = time
        self.high = high
        self.low = low
        self.mid = mid


def _detect_sibi_in_timeframe(timeframe, df):
    sibis = []
    for i in range(2, len(df)):
        c1 = df.iloc[i - 2]
        c2 = df.iloc[i - 1]
        c3 = df.iloc[i]

        l1 = float(c1["Low"])
        o2 = float(c2["Open"])
        c2_close = float(c2["Close"])
        h3 = float(c3["High"])

        if (l1 > c2_close) and (c2_close < o2) and (h3 < l1):
            high = l1          # SIBI high = candle 1 low
            low = h3           # SIBI low = candle 3 high
            mid = (low + high) / 2
            time = c2.name     # time of middle candle

            sibis.append(SIBI(timeframe, time, high, low, mid))

    return sibis


def detect_sibi(ohlc_dict):
    sibi_by_timeframe = {}
    for timeframe, ohlc in ohlc_dict.items():
        df = ohlc.data
        sibis_for_tf = _detect_sibi_in_timeframe(timeframe, df)
        sibi_by_timeframe[timeframe] = sibis_for_tf
    return sibi_by_timeframe


def debug_print_last_sibis(sibi_by_timeframe, n=20):
    for timeframe, sibis in sibi_by_timeframe.items():
        print(f"\nTimeframe: {timeframe}")
        if not sibis:
            print("  No SIBIs detected.")
            continue

        for s in sibis[-n:]:
            ts = s.time

            if isinstance(ts, pd.Timestamp):
                if ts.tzinfo is None:
                    ts = ts.tz_localize("UTC")
                nyt_time = ts.tz_convert("America/New_York")
                nyt_time_str = nyt_time.strftime("%Y-%m-%d %H:%M")
            else:
                nyt_time_str = str(ts)

            print(
                f"  time_NYT={nyt_time_str}, "
                f"low={s.low}, high={s.high}, mid={s.mid}"
            )
