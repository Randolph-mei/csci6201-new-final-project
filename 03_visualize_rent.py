
# CSCI 6201 - Fall 2026
# DMV Rental Market Analysis
# Step 3: Visualize rental data

import pandas as pd
import matplotlib.pyplot as plt
import os
import folium

def main():
    # Step 1: Load datasets
    zillow = pd.read_csv("data/Zip_zori_uc_sfrcondomfr_sm_month.csv",
                         dtype={"RegionName": str})

    census = pd.read_csv("data/2026_Gaz_zcta_national.txt",
                         sep="|",
                         dtype={"GEOID": str})

    # Step 2: Select DMV ZIP codes (exclude West Virginia)
    dmv = zillow[
        (zillow["Metro"] == "Washington-Arlington-Alexandria, DC-VA-MD-WV") &
        (zillow["State"].isin(["DC", "VA", "MD"]))
    ].copy()

    latest_date = "2026-09-30"

    # Step 3: Create figures folder
    os.makedirs("figures", exist_ok=True)

    # Figure 1: Rental price distribution
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

    # Figure 2: Average rent by state
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

    # Figure 3: Geographic rental distribution

    # Match ZIP codes with Census coordinates
    census.columns = census.columns.str.strip()
    dmv = pd.merge(
        dmv,
        census,
        left_on="RegionName",
        right_on="GEOID"
    )

    # Create interactive map
    dmv_map = folium.Map(
        location=[38.90, -77.10],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    # Add ZIP code markers
    for index, row in dmv.iterrows():
        price = row[latest_date]

        if pd.isna(price):
            continue

        if price < 2000:
            color = "green"
        elif price < 3000:
            color = "orange"
        else:
            color = "red"

        popup_text = (
            "ZIP Code: " + row["RegionName"] +
            "<br>State: " + row["State"] +
            "<br>Monthly Rent: $" + str(round(price, 2))
        )

        folium.CircleMarker(
            location=[row["INTPTLAT"], row["INTPTLONG"]],
            # "INTPTLAT" means "Internal Point Latitude"
            # "INTPTLONG" means "Internal Point Longitude"
            # They are in the American Census Dataset, and it's just two name
            radius=6,
            color=color,
            fill=True,
            fill_color=color,
            fill_opacity=0.7,
            popup=popup_text
        ).add_to(dmv_map)

    dmv_map.save("figures/03_rental_map.html")

    print("Saved Figure 3: Interactive Rental Map")
    print("Done!")


if __name__ == "__main__":
    main()
