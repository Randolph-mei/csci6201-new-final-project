# CSCI 6201 - Fall 2026
# DMV Rental Market Analysis
# Step 5: Test rental data and regression
# This part I followed a lot form the diabetes_regression sample, but I just feel confused that why we need to do this
# becauseI have downloaded, load, and explore the dataset

import unittest
import pandas as pd
from sklearn.linear_model import LinearRegression

class TestRent(unittest.TestCase):
    # Test 1: Check dataset columns
    def test_columns(self):
        zillow = pd.read_csv(
            "data/Zip_zori_uc_sfrcondomfr_sm_month.csv",
            dtype={"RegionName": str}
        )

        self.assertIn("RegionName", zillow.columns)
        self.assertIn("Metro", zillow.columns)
        self.assertIn("State", zillow.columns)
        self.assertIn("2026-08-31", zillow.columns)
        self.assertIn("2026-09-30", zillow.columns)

    # Test 2: Check DMV filtering
    def test_dmv(self):
        zillow = pd.read_csv(
            "data/Zip_zori_uc_sfrcondomfr_sm_month.csv",
            dtype={"RegionName": str}
        )

        dmv = zillow[
            (zillow["Metro"] == "Washington-Arlington-Alexandria, DC-VA-MD-WV") &
            (zillow["State"].isin(["DC", "VA", "MD"]))
        ].copy()

        self.assertGreater(len(dmv), 0)
        self.assertTrue(dmv["State"].isin(["DC", "VA", "MD"]).all())

    # Test 3: Check Linear Regression
    def test_regression(self):
        X = [[1000], [2000], [3000], [4000]]
        y = [1100, 2100, 3100, 4100]

        model = LinearRegression()
        model.fit(X, y)
        prediction = model.predict([[2500]])
        self.assertAlmostEqual(prediction[0], 2600)


if __name__ == "__main__":
    unittest.main(verbosity=2)
