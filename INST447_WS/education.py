import argparse
import pandas as pd
import sys

def most_educated(file, state):
    df = pd.read_csv(file)
    filter = df["State"] == state 
    edu = df[filter]
    percent = edu["Percent of adults with a bachelor's degree or higher"]
    max_percent = percent.max()
    highest_education_county = edu[percent == max_percent]
    county_name = highest_education_county.iloc[0]['Area name']
    return (county_name, max_percent)

def parse_args(args):
    parser = argparse.ArgumentParser(description="Identify the county in a given state with the highest education level per capita")
    parser.add_argument('csv_file', type=str, help="Path to the CSV file")
    parser.add_argument('state', type=str, help="Two-letter state abbreviation")

    return parser.parse_args(args)

if __name__ == "__main__":
    # Parse command-line arguments
    args = parse_args(sys.argv[1:])

    # Find the county with the highest educational achievement per capita
    county, percent = most_educated(args.csv_file, args.state)

    # Print the results
    print(f"{percent}% of adults in {county} have at least a bachelor’s degree")