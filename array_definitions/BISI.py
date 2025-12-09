from data.ohlc import ohlc_by_timeframe
import pandas as pd



class BISI:
    def __init__(self, timeframe, time, high, low, mid):
        self.timeframe = timeframe
        self.time = time
        self.high = high
        self.low = low
        self.mid = mid


def _detect_bisi_in_timeframe(timeframe, df):
    bisis = []
    for i in range(2, len(df)):
        c1 = df.iloc[i - 2]
        c2 = df.iloc[i - 1]
        c3 = df.iloc[i]

        h1 = float(c1["High"])
        o2 = float(c2["Open"])
        c2_close = float(c2["Close"])
        l3 = float(c3["Low"])

        if (h1 < c2_close) and (c2_close > o2) and (l3 > h1):
            low = h1          # BISI low = candle 1 high
            high = l3         # BISI high = candle 3 low
            mid = (low + high) / 2
            time = c2.name    # time of middle candle

            bisis.append(BISI(timeframe, time, high, low, mid))

    return bisis



def detect_bisi(ohlc_dict):
    bisi_by_timeframe = {}
    for timeframe, ohlc in ohlc_dict.items():
        df = ohlc.data
        bisis_for_tf = _detect_bisi_in_timeframe(timeframe, df)
        bisi_by_timeframe[timeframe] = bisis_for_tf
    return bisi_by_timeframe


def debug_print_last_bisis(bisi_by_timeframe, n=20):
    for timeframe, bisis in bisi_by_timeframe.items():
        print(f"\nTimeframe: {timeframe}")
        if not bisis:
            print("  No BISIs detected.")
            continue

        for b in bisis[-n:]:
            ts = b.time

            if isinstance(ts, pd.Timestamp):
                if ts.tzinfo is None:
                    ts = ts.tz_localize("UTC")
                nyt_time = ts.tz_convert("America/New_York")
                # strip timezone info for cleaner display
                nyt_time_str = nyt_time.strftime("%Y-%m-%d %H:%M")
            else:
                nyt_time_str = str(ts)

            print(
                f"  time_NYT={nyt_time_str}, "
                f"low={b.low}, high={b.high}, mid={b.mid}"
            )


