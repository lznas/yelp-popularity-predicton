import pandas as pd
import os

RAW_PATH = "data/00-raw/yelp_dataset/yelp_academic_dataset_business.json"
OUT_PATH = "data/02-processed/philly_business.csv"

def main():
    print("Loading raw data...")
    df = pd.read_json(RAW_PATH, lines=True)

    print("Filtering Philadelphia businesses...")
    ph = df[
        (df['city'] == 'Philadelphia') &
        (df['state'] == 'PA')
    ]

    os.makedirs("data/02-processed", exist_ok=True)

    print("Saving processed file...")
    ph.to_csv(OUT_PATH, index=False)

    print("Done!")

if __name__ == "__main__":
    main()
