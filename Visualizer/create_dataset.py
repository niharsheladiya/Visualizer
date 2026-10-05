# create_dataset.py
# --------------------------------------------------------------
# This file makes a sales dataset (sales_data.csv) for our project.
# I could not download from Kaggle here, so this file creates
# a similar sales dataset. If you download a Kaggle sales CSV,
# just keep the same column names (Date, Product, Region, Sales,
# Profit) and the project will work with that file too.
#
# Run this file ONE time:   python create_dataset.py
# --------------------------------------------------------------

import numpy as np
import pandas as pd

# same random numbers every time we run the file
np.random.seed(42)

number_of_rows = 1000

# set this to True if you want some missing values in the data
# (useful for testing the "Handle Missing Data" menu)
add_missing_values = False

products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
regions = ["North", "South", "East", "West Coast", "Central"]

# price of one item of each product
unit_price = {
    "Product A": 50,
    "Product B": 75,
    "Product C": 120,
    "Product D": 150,
    "Product E": 90,
}

# random dates between 2022-01-01 and 2024-12-31 (1096 days)
random_days = np.random.randint(0, 1096, size=number_of_rows)
dates = pd.to_datetime("2022-01-01") + pd.to_timedelta(random_days, unit="D")

# make the DataFrame
sales_data = pd.DataFrame({
    "Date": dates,
    "Product": np.random.choice(products, number_of_rows),
    "Region": np.random.choice(regions, number_of_rows),
    "Quantity": np.random.randint(1, 21, number_of_rows),
})

# sort by date so the data looks natural
sales_data = sales_data.sort_values("Date").reset_index(drop=True)

# Sales = quantity x price
sales_data["Sales"] = sales_data["Quantity"] * sales_data["Product"].map(unit_price)

# Profit is 5% to 30% of the sales
profit_percent = np.random.uniform(0.05, 0.30, number_of_rows)
sales_data["Profit"] = (sales_data["Sales"] * profit_percent).round(2)

# Year column (the example in the project uses Year)
sales_data["Year"] = sales_data["Date"].dt.year

# SalesID column at the first position
sales_data.insert(0, "SalesID", np.arange(101, 101 + number_of_rows))

# put some empty values in Profit if we want
if add_missing_values:
    random_rows = np.random.choice(number_of_rows, 15, replace=False)
    sales_data.loc[random_rows, "Profit"] = np.nan

# save to csv
sales_data.to_csv("sales_data.csv", index=False)

print("sales_data.csv created successfully!")
print("Rows:", len(sales_data))
print()
print(sales_data.head())
