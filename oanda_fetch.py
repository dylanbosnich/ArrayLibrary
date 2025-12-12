import requests
import pandas as pd
from datetime import datetime


# ====== CONFIG –– PUT YOUR DETAILS HERE ======
OANDA_API_TOKEN = "dfdd4db5e4ee4c45b568e2357a14a806-c6d10d6fd392020e17a52dfa1f619f03"
OANDA_ACCOUNT_ID = "101-011-31532902-001"

# practice API base
BASE_URL = "https://api-fxpractice.oanda.com/v3"
INSTRUMENT = "EUR_USD"
# ============================================


def fetch_candles_granularity(granularity="H1", count=5000):
    """
    Fetch candles from OANDA and return as a pandas DataFrame.
    granularity examples:
        S5, S10, S30
        M1, M5, M15, M30
        H1, H2, H3, H4, H6, H8, H12
        D, W, M
    """

    url = f"{BASE_URL}/instruments/{INSTRUMENT}/candles"

    headers = {
        "Authorization": f"Bearer {OANDA_API_TOKEN}",
        "Content-Type": "application/json",
    }

    params = {
        "granularity": granularity,
        "count": count,
        "price": "M",   # mid prices
    }

    resp = requests.get(url, headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json()

    candles = data.get("candles", [])

    rows = []
    for c in candles:
        t = c["time"]  # e.g. "2025-12-10T12:00:00.000000000Z"
        # strip the nanoseconds + Z
        t = t.split(".")[0].replace("Z", "")
        t_dt = datetime.fromisoformat(t)

        mid = c["mid"]
        o = float(mid["o"])
        h = float(mid["h"])
        l = float(mid["l"])
        close = float(mid["c"])

        rows.append({
            "time": t_dt,
            "Open": o,
            "High": h,
            "Low": l,
            "Close": close,
        })

    df = pd.DataFrame(rows)
    df.set_index("time", inplace=True)
    return df


def save_eurusd_timeframes():
    """
    Download and save EUR/USD candles for the timeframes
    you care about into CSVs under data/raw.
    """

    mapping = {
        "M15": "15m",
        "H1": "1h",
        "H4": "4h",
        "D": "1d",
        "W": "1wk",
    }

    for granularity, tf_name in mapping.items():
        print(f"Fetching {INSTRUMENT} {granularity} ...")
        df = fetch_candles_granularity(granularity=granularity, count=5000)

        path = f"data/raw/EURUSD_{tf_name}.csv"
        df.to_csv(path)
        print(f"Saved {len(df)} candles to {path}")


if __name__ == "__main__":
    save_eurusd_timeframes()
