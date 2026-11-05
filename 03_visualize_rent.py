
# CSCI 6201 - Fall 2026
# DMV Rental Market Analysis
# Step 3: Visualize rental data

import pandas as pd
import matplotlib.pyplot as plt
import os
import contextily as ctx

def main():
    # Step 1: Load datasets
    zillow = pd.read_csv("data/Zip_zori_uc_sfrcondomfr_sm_month.csv",
                         dtype={"RegionName": str})

    census = pd.read_csv("data/2026_Gaz_zcta_national.txt",
                         sep="|",
                         dtype={"GEOID": str})

    # Step 2: Select DMV ZIP codes
    # And I was trying to delete West Virginia
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
    plt.xlabel("Monthly Zillow Rent Index ($)")
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

    # Figure 3: Geographic rental distribution, map, and use AI to improve
    matched = pd.merge(dmv, census,
                       left_on="RegionName",
                       right_on="GEOID",
                       how="left")

    matched = matched.dropna(
        subset=["INTPTLAT", "INTPTLONG", latest_date]
    )

    fig, ax = plt.subplots(figsize=(11, 8))

    scatter = ax.scatter(
        matched["INTPTLONG"],
        matched["INTPTLAT"],
        c=matched[latest_date],
        cmap="viridis",
        s=55,
        edgecolors="black",
        linewidths=0.4,
        zorder=2
    )

    # Add OpenStreetMap background
    # And in case of bad network, use try to avoid it
    try:
        ctx.add_basemap(
            ax,
            crs="EPSG:4326",
            source=ctx.providers.Esri.WorldTopoMap,
            zoom=9
        )
    except Exception as error:
        print("Map background could not be loaded:", error)

    plt.colorbar(scatter, ax=ax, label="Monthly Zillow Rent Index ($)")
    ax.set_title("DMV Geographic Rental Distribution (September 2026)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    #add more info
    ax.text(
        0.01, 0.01,
        "Rent: Zillow ZORI | Locations: U.S. Census Bureau",
        transform=ax.transAxes,
        fontsize=8,
        bbox={"facecolor": "white", "alpha": 0.8}
    )

    plt.tight_layout()
    plt.savefig("figures/03_geographic_rent.png", dpi=200)
    plt.close()

    print("Saved Figure 3: Geographic Rental Distribution")
    print("ZIP codes plotted:", len(matched))


if __name__ == "__main__":
    main()
