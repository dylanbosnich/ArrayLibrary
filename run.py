from array_definitions.swing_hl import detect_swing_highs, detect_swing_lows

def main():
    sh = detect_swing_highs()
    sl = detect_swing_lows()

    for tf in sh:
        print(f"\nTimeframe: {tf}")
        print("  last 5 swing highs:")
        for s in sh[tf][-5:]:
            print(f"    {s}")
        print("  last 5 swing lows:")
        for s in sl[tf][-5:]:
            print(f"    {s}")

if __name__ == "__main__":
    main()
