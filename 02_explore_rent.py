# CSCI 6201 - Fall 2026
# DMV Rental Market Analysis
# Step 2: Explore rental data

import pandas as pd


def summarize_rent(values):
    # Calculate minimum, maximum, and average rent
    minimum = min(values)
    maximum = max(values)
    average = sum(values) / len(values)
    return minimum, maximum, average


def count_above(values, threshold):
    # Count ZIP codes with rent above the threshold
    count = 0
    for value in values:
        if value > threshold:
            count += 1
    return count


def main():
    # Step 1: Load Zillow data
    zillow = pd.read_csv("data/Zip_zori_uc_sfrcondomfr_sm_month.csv",
                         dtype={"RegionName": str})

    # Step 2: Select DMV ZIP codes
    dmv = zillow[
        (zillow["Metro"] == "Washington-Arlington-Alexandria, DC-VA-MD-WV") &
        (zillow["State"].isin(["DC", "VA", "MD"]))
    ]

    print("Number of DMV ZIP codes:", len(dmv))

    # Step 3: Select the latest rental data
    latest_date = "2026-09-30"
    rents = dmv[latest_date].dropna().tolist()

    print("ZIP codes with rental data:", len(rents))
    print("Missing rental values:", dmv[latest_date].isna().sum())

    # Step 4: Calculate rental statistics
    minimum, maximum, average = summarize_rent(rents)

    print("\nRental statistics (September 2026):")
    print("Minimum rent: $", round(minimum, 2))
    print("Maximum rent: $", round(maximum, 2))
    print("Average rent: $", round(average, 2))

    # Step 5: Count expensive ZIP codes
    expensive = count_above(rents, 3000)
    print("ZIP codes with rent above $3000:", expensive)

    # Step 6: Load Census geographic data
    census = pd.read_csv("data/2026_Gaz_zcta_national.txt",
                         sep="|",
                         dtype={"GEOID": str})

    # Step 7: Match Zillow ZIP codes with Census ZCTAs
    matched = pd.merge(dmv, census,
                       left_on="RegionName",
                       right_on="GEOID",
                       how="left")

    missing_coordinates = matched["INTPTLAT"].isna().sum()

    print("\nGeographic data:")
    print("ZIP codes with coordinates:", len(matched) - missing_coordinates)
    print("ZIP codes without coordinates:", missing_coordinates)


if __name__ == "__main__":
    main()