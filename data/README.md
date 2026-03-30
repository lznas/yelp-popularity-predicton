To reproduce Philidelphia dataset:
1. Download the Yelp Open Dataset from: https://www.yelp.com/dataset
2. Place yelp_academic_dataset_business.json in: data/00-raw/
3. Run the wrangling script from the project root: python src/wrangle_philly.py
4. This generates data/01-interim/philly_business.csv

To reproduce Philidelphia reviews dataset:
1. Download the Yelp Open Dataset from: https://www.yelp.com/dataset
2. Place yelp_academic_dataset_review.json in: data/00-raw/
3. Run the wrangling script from the project root: python src/wrangle_philly_reviews.py
4. This generates data/01-interim/philly_review_agg.csv
5. To create a review text sample: python src/wrangle_philly_reviews.py --sample_size 5000 --out_sample data/01-interim/philly_reviews_sample_5000.jsonl

