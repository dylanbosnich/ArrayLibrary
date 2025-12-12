from array_definitions.weekly_liquidity import get_weekly_liquidity, detect_weekly_swing_highs, detect_weekly_swing_lows

def main():
    w = get_weekly_liquidity()
    print("Weekly PD levels:")
    for k, v in w.items():
        print(f"  {k}: {v}")

    sh = detect_weekly_swing_highs()
    sl = detect_weekly_swing_lows()

    print("\nLast 5 weekly swing highs:")
    for x in sh[-5:]:
        print(" ", x)

    print("\nLast 5 weekly swing lows:")
    for x in sl[-5:]:
        print(" ", x)

if __name__ == "__main__":
    main()
