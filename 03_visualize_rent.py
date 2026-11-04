
# CSCI 6201 - Fall 2026
# DMV Rental Market Analysis
# Step 3: Visualize rental data

import pandas as pd
import matplotlib.pyplot as plt
import os


def main():
    # Step 1: Load datasets
    zillow = pd.read_csv("data/Zip_zori_uc_sfrcondomfr_sm_month.csv",
                         dtype={"RegionName": str})

    census = pd.read_csv("data/2026_Gaz_zcta_national.txt",
                         sep="|",
                         dtype={"GEOID": str})

    # Step 2: Select DMV ZIP codes
    dmv = zillow[
        (zillow["Metro"] == "Washington-Arlington-Alexandria, DC-VA-MD-WV") &
        (zillow["State"].isin(["DC", "VA", "MD"]))
    ].copy()

    latest_date = "2026-09-30"

    # Step 3: Create figures folder
    os.makedirs("figures", exist_ok=True)

    # Figure 1: Rental price distribution, chart
    plt.figure(figsize=(8, 5))
    plt.hist(dmv[latest_date].dropna(), bins=15,
             edgecolor="black")
    plt.title("DMV Rental Price Distribution (September 2026)")
    plt.xlabel("Monthly Rent ($)")
    plt.ylabel("Number of ZIP Codes")
    plt.tight_layout()
    plt.savefig("figures/01_rental_distribution.png")
    plt.close()

    print("Saved Figure 1: Rental Price Distribution")

    # Figure 2: Average rent by state, table
    states = ["DC", "VA", "MD"]
    average_rents = []

    for state in states:
        state_data = dmv[dmv["State"] == state]
        average = state_data[latest_date].mean()
        average_rents.append(average)

    plt.figure(figsize=(8, 5))
    plt.bar(states, average_rents, edgecolor="black")
    plt.title("Average Monthly Rent by State (September 2026)")
    plt.xlabel("State")
    plt.ylabel("Average Monthly Rent ($)")
    plt.tight_layout()
    plt.savefig("figures/02_average_rent_by_state.png")
    plt.close()

    print("Saved Figure 2: Average Rent by State")

    # Figure 3: Geographic rental distribution, map
    matched = pd.merge(dmv, census,
                       left_on="RegionName",
                       right_on="GEOID",
                       how="left")

    matched = matched.dropna(
        subset=["INTPTLAT", "INTPTLONG", latest_date]
    )

    plt.figure(figsize=(9, 7))
    scatter = plt.scatter(
        matched["INTPTLONG"],
        matched["INTPTLAT"],
        c=matched[latest_date],
        cmap="viridis",
        s=45,
        edgecolors="black",
        linewidths=0.3
    )

    plt.colorbar(scatter, label="Monthly Rent ($)")
    plt.title("DMV Geographic Rental Distribution (September 2026)")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.tight_layout()
    plt.savefig("figures/03_geographic_rent.png")
    plt.close()

    print("Saved Figure 3: Geographic Rental Distribution")
    print("ZIP codes plotted:", len(matched))


if __name__ == "__main__":
    main()
