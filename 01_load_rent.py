# CSCI 6201 - Fall 2026
# DMV Rental Market Analysis
# Step 1: Load Zillow and Census datasets

import pandas as pd


def main():
    # Step 1: Load Zillow rental data
    zillow = pd.read_csv("data/Zip_zori_uc_sfrcondomfr_sm_month.csv",
                         dtype={"RegionName": str})

    # Step 2: Load Census geographic data
    census = pd.read_csv("data/2026_Gaz_zcta_national.txt",
                         sep="|",
                         dtype={"GEOID": str})

    # Step 3: Display Zillow dataset information
    print("Zillow dataset:")
    print("Number of ZIP codes:", len(zillow))
    print("Number of columns:", len(zillow.columns))

    # Step 4: Display Census dataset information
    print("\nCensus dataset:")
    print("Number of geographic records:", len(census))
    print("Number of columns:", len(census.columns))

    # Step 5: Display the first record from each dataset
    print("\nFirst Zillow record:")
    print(zillow.iloc[0])

    print("\nFirst Census record:")
    print(census.iloc[0])


if __name__ == "__main__":
    main()