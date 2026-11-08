
# CSCI 6201 - Fall 2026
# DMV Rental Market Analysis
# Step 4: Predict rental prices using Linear Regression
# And I will use 20% as test, the other 80% as training

import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

def main():
    # Step 1: Load Zillow dataset
    zillow = pd.read_csv("data/Zip_zori_uc_sfrcondomfr_sm_month.csv",
                         dtype={"RegionName": str})

    # Step 2: Select DMV ZIP codes (exclude West Virginia)
    dmv = zillow[
        (zillow["Metro"] == "Washington-Arlington-Alexandria, DC-VA-MD-WV") &
        (zillow["State"].isin(["DC", "VA", "MD"]))
    ].copy()

    # Step 3: Select rental prices
    august = "2026-08-31"
    september = "2026-09-30"

    dmv = dmv.dropna(subset=[august, september])

    X = dmv[[august]]
    y = dmv[september]

    #Step 4: Split training and testing data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Step 5: Train Linear Regression model
    model = LinearRegression()
    model.fit(X_train, y_train)
    # will train to learn the relation between 8 and 9, then to step 6

    # Step 6: Predict September rental prices
    predictions = model.predict(X_test)

    # Step 7: Evaluate the model
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    # R² is Coefficient of Determination

    print("DMV Rental Price Prediction\n")
    print("Training samples:", len(X_train))
    print("Testing samples:", len(X_test))
    print("Mean Absolute Error (MAE):", round(mae, 2))
    print("R-squared (R2):", round(r2, 3))

    # Step 8: Save results
    os.makedirs("results", exist_ok=True)

    with open("results/04_prediction_results.txt", "w") as file:
        file.write("DMV Rental Price Prediction\n")
        file.write("Model: Linear Regression\n")
        file.write("Feature: August 2026 Rent\n")
        file.write("Target: September 2026 Rent\n")
        file.write("Training samples: " + str(len(X_train)) + "\n")
        file.write("Testing samples: " + str(len(X_test)) + "\n")
        file.write("MAE: " + str(round(mae, 2)) + "\n")
        file.write("R-squared: " + str(round(r2, 3)) + "\n")

    print("Results saved to results/04_prediction_results.txt")


if __name__ == "__main__":
    main()
