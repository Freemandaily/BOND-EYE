"""Simple backfill helper script placeholder."""
import argparse

def run_backfill(start_block: int, end_block: int):
    print(f"Backfilling from {start_block} to {end_block}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    args = parser.parse_args()
    run_backfill(args.start, args.end)

if __name__ == "__main__":
    main()
