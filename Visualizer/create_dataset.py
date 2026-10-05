# Welcome to Create Dataset file 

import numpy as np
import pandas as pd


np.random.seed(42)

number_of_rows = 1000


add_missing_values = False

products = ["Product A", "Product B", "Product C", "Product D", "Product E"]
regions = ["North", "South", "East", "West Coast", "Central"]


unit_price = {
    "Product A": 50,
    "Product B": 75,
    "Product C": 120,
    "Product D": 150,
    "Product E": 90,
}


random_days = np.random.randint(0, 1096, size=number_of_rows)
dates = pd.to_datetime("2022-01-01") + pd.to_timedelta(random_days, unit="D")


sales_data = pd.DataFrame({
    "Date": dates,
    "Product": np.random.choice(products, number_of_rows),
    "Region": np.random.choice(regions, number_of_rows),
    "Quantity": np.random.randint(1, 21, number_of_rows),
}
                          
sales_data = sales_data.sort_values("Date").reset_index(drop=True)


sales_data["Sales"] = sales_data["Quantity"] * sales_data["Product"].map(unit_price)


profit_percent = np.random.uniform(0.05, 0.30, number_of_rows)
sales_data["Profit"] = (sales_data["Sales"] * profit_percent).round(2)


sales_data["Year"] = sales_data["Date"].dt.year


sales_data.insert(0, "SalesID", np.arange(101, 101 + number_of_rows))


if add_missing_values:
    random_rows = np.random.choice(number_of_rows, 15, replace=False)
    sales_data.loc[random_rows, "Profit"] = np.nan


sales_data.to_csv("sales_data.csv", index=False)

print("sales_data.csv created successfully!")
print("Rows:", len(sales_data))
print()
print(sales_data.head())
