import argparse
import csv
import json
import os
import random
from collections import defaultdict
from datetime import datetime

import pandas as pd


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--business_csv", default="data/01-interim/philly_business.csv")
    parser.add_argument("--review_json", default="data/00-raw/yelp_dataset/yelp_academic_dataset_review.json")
    parser.add_argument("--out_agg", default="data/01-interim/philly_review_agg.csv")
    parser.add_argument("--sample_size", type=int, default=0)  # 0 = no sampling
    parser.add_argument("--out_sample", default="data/01-interim/philly_reviews_sample.jsonl")
    args = parser.parse_args()

    # Load Philly business_ids
    ph_ids = set(pd.read_csv(args.business_csv, usecols=["business_id"])["business_id"].astype(str))
    print("Philly businesses:", len(ph_ids))

    # Aggregate per business_id
    agg = defaultdict(lambda: {"review_ct": 0, "sum_stars": 0.0, "latest_date": None})
    sample = []
    seen = 0
    random.seed(42)

    with open(args.review_json, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            r = json.loads(line)
            bid = str(r.get("business_id", ""))

            if bid in ph_ids:
                a = agg[bid]
                a["review_ct"] += 1
                a["sum_stars"] += float(r.get("stars", 0.0))

                d = r.get("date")
                if d:
                    try:
                        dt = datetime.fromisoformat(d)
                        if a["latest_date"] is None or dt > a["latest_date"]:
                            a["latest_date"] = dt
                    except ValueError:
                        pass

                # Optional reservoir sample of Philly reviews
                if args.sample_size > 0:
                    seen += 1
                    if len(sample) < args.sample_size:
                        sample.append(line)
                    else:
                        j = random.randint(0, seen - 1)
                        if j < args.sample_size:
                            sample[j] = line

            if i % 500000 == 0:
                print("Processed:", i)

    # Write aggregate CSV (small)
    os.makedirs(os.path.dirname(args.out_agg), exist_ok=True)
    with open(args.out_agg, "w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(["business_id", "review_ct_in_file", "avg_review_stars", "latest_review_date"])
        for bid, a in agg.items():
            ct = a["review_ct"]
            avg = (a["sum_stars"] / ct) if ct else ""
            latest = a["latest_date"].date().isoformat() if a["latest_date"] else ""
            writer.writerow([bid, ct, avg, latest])

    print("Wrote:", args.out_agg)

    # Write optional sample JSONL
    if args.sample_size > 0:
        os.makedirs(os.path.dirname(args.out_sample), exist_ok=True)
        with open(args.out_sample, "w", encoding="utf-8") as out:
            out.writelines(sample)
        print("Wrote sample:", args.out_sample)


if __name__ == "__main__":
    main()
UT_PATH, index=False)

    print("Done!")

if __name__ == "__main__":
    main()
