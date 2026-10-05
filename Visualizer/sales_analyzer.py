# sales_analyzer.py
# --------------------------------------------------------------
# This file has the main class SalesDataAnalyzer.
# All the data work is done here: load, explore, clean,
# math operations, combine, split, search/sort/filter,
# aggregate, statistics, pivot table and some advanced things.
# --------------------------------------------------------------

import numpy as np
import pandas as pd


class SalesDataAnalyzer:

    # ---------------------- basic setup ----------------------

    def __init__(self, file_path=None):
        # self.data will keep our sales DataFrame
        self.data = None
        if file_path is not None:
            self.load_data(file_path)

    def __del__(self):
        # small cleanup when the object is deleted
        self.data = None

    def __add__(self, other):
        # operator overloading: analyzer1 + analyzer2 joins their data
        if self.data is None or other.data is None:
            print("Both analyzers need data to be added.")
            return self
        new_analyzer = SalesDataAnalyzer()
        new_analyzer.data = pd.concat([self.data, other.data], ignore_index=True)
        return new_analyzer

    # ---------------------- helper methods ----------------------

    def is_data_loaded(self):
        # checks if the user already loaded a dataset
        if self.data is None:
            print("\nNo dataset loaded. Please load a dataset first (option 1).")
            return False
        return True

    def has_columns(self, column_list):
        # checks if all the given columns are in the dataset
        for column in column_list:
            if column not in self.data.columns:
                print("\nColumn '" + str(column) + "' is not in the dataset.")
                print("Available columns:", list(self.data.columns))
                return False
        return True

    def convert_data_types(self):
        # Date column should be datetime
        if "Date" in self.data.columns:
            self.data["Date"] = pd.to_datetime(self.data["Date"], errors="coerce")
            # make a Year column if the file does not have one
            if "Year" not in self.data.columns:
                self.data["Year"] = self.data["Date"].dt.year

        # these columns should be numbers
        for column in ["Sales", "Profit", "Quantity"]:
            if column in self.data.columns:
                self.data[column] = pd.to_numeric(self.data[column], errors="coerce")

    # ---------------------- load data ----------------------

    def load_data(self, file_path):
        try:
            self.data = pd.read_csv(file_path)
            self.convert_data_types()
            print("Dataset loaded successfully!")
            return True
        except FileNotFoundError:
            print("File not found. Please check the file path.")
        except pd.errors.EmptyDataError:
            print("The file is empty.")
        except Exception as error:
            print("Something went wrong while loading the file:", error)
        return False

    def read_other_file(self, file_path):
        # reads a second csv file and gives back a DataFrame
        try:
            return pd.read_csv(file_path)
        except FileNotFoundError:
            print("File not found. Please check the file path.")
        except Exception as error:
            print("Could not read the file:", error)
        return None

    # ---------------------- explore data ----------------------

    def explore_data(self, choice):
        if choice == 1:
            print(self.data.head())
        elif choice == 2:
            print(self.data.tail())
        elif choice == 3:
            print(list(self.data.columns))
        elif choice == 4:
            print(self.data.dtypes)
        elif choice == 5:
            self.data.info()
            print()
            print(self.data.describe())
        else:
            print("Invalid choice.")

    # ---------------------- clean data ----------------------

    def clean_data(self, choice, column=None, value=None):
        if choice == 1:
            # show rows which have at least one missing value
            missing_rows = self.data[self.data.isnull().any(axis=1)]
            if missing_rows.empty:
                print("\nNo missing values found in the dataset!")
            else:
                print("\nRows with missing values:")
                print(missing_rows)
                print("\nMissing values in each column:")
                print(self.data.isnull().sum())

        elif choice == 2:
            # fill the number columns with their mean
            number_columns = self.data.select_dtypes(include=np.number).columns
            self.data[number_columns] = self.data[number_columns].fillna(
                self.data[number_columns].mean()
            )
            print("\nMissing values in number columns filled with the mean.")

        elif choice == 3:
            rows_before = len(self.data)
            self.data = self.data.dropna()
            print("\nRows before:", rows_before)
            print("Rows after :", len(self.data))
            print("Dropped", rows_before - len(self.data), "rows.")

        elif choice == 4:
            if not self.has_columns([column]):
                return
            # if the column has numbers then change the value to a number
            if pd.api.types.is_numeric_dtype(self.data[column]):
                try:
                    value = float(value)
                except ValueError:
                    print("\nThis column needs a number value.")
                    return
            self.data[column] = self.data[column].fillna(value)
            print("\nMissing values in", column, "replaced with", value)

        else:
            print("Invalid choice.")

    # ---------------------- numpy arrays ----------------------

    def numpy_operations(self):
        if not self.has_columns(["Sales", "Profit"]):
            return

        # convert DataFrame column to numpy array
        sales_array = self.data["Sales"].dropna().to_numpy()
        print("\nSales as a numpy array")
        print("Type  :", type(sales_array))
        print("Shape :", sales_array.shape)

        # indexing
        print("\n-- Indexing --")
        print("First sale :", sales_array[0])
        print("Last sale  :", sales_array[-1])

        # slicing
        print("\n-- Slicing --")
        print("First 5 sales :", sales_array[:5])
        print("Last 5 sales  :", sales_array[-5:])
        print("Every 10th sale (first 5 of them):", sales_array[::10][:5])

        # boolean indexing
        average = sales_array.mean()
        above_average = sales_array[sales_array > average]
        print("\nAverage sale :", round(average, 2))
        print("Sales above average:", len(above_average))

        # 2D array with Sales and Profit
        two_d_array = self.data[["Sales", "Profit"]].dropna().to_numpy()
        print("\n-- 2D array (Sales, Profit) --")
        print("Shape :", two_d_array.shape)
        print("First 3 rows:")
        print(two_d_array[:3, :])
        print("Profit column only (first 5):", two_d_array[:5, 1])

    # ---------------------- math operations ----------------------

    def mathematical_operations(self):
        if not self.has_columns(["Sales", "Profit"]):
            return

        sales = self.data["Sales"].to_numpy()
        profit = self.data["Profit"].to_numpy()

        # element wise operations
        self.data["Sales_With_Tax"] = np.round(sales * 1.10, 2)
        self.data["Cost"] = np.round(sales - profit, 2)
        self.data["Profit_Margin"] = np.round(profit / sales * 100, 2)

        print("\nNew columns added: Sales_With_Tax, Cost, Profit_Margin")
        print(self.data[["Sales", "Profit", "Sales_With_Tax", "Cost", "Profit_Margin"]].head())

        print("\nTotal Sales  :", np.nansum(sales))
        print("Total Profit :", round(np.nansum(profit), 2))
        print("Average Profit Margin :", round(np.nanmean(self.data["Profit_Margin"]), 2), "%")

    # ---------------------- combine data ----------------------

    def combine_data(self, other_dataframe):
        # joins our DataFrame with another one (concat)
        rows_before = len(self.data)
        self.data = pd.concat([self.data, other_dataframe], ignore_index=True)
        # first fix the data types (Date from the new file is text),
        # then remove the duplicate rows
        self.convert_data_types()
        # compare only the columns that the new file also has
        # (our data may have extra columns like Profit_Margin)
        common_columns = [c for c in other_dataframe.columns if c in self.data.columns]
        self.data = self.data.drop_duplicates(subset=common_columns).reset_index(drop=True)
        print("\nRows before :", rows_before)
        print("Rows added  :", len(other_dataframe))
        print("Rows now    :", len(self.data), "(duplicate rows are removed)")

    def merge_product_totals(self):
        # merge example: make a small table of total sales per product
        # and merge it back into the main data
        if not self.has_columns(["Product", "Sales"]):
            return

        if "Product_Total_Sales" in self.data.columns:
            self.data = self.data.drop(columns=["Product_Total_Sales"])

        product_totals = self.data.groupby("Product")["Sales"].sum().reset_index()
        product_totals.columns = ["Product", "Product_Total_Sales"]

        self.data = pd.merge(self.data, product_totals, on="Product", how="left")
        print("\nMerged total sales of each product into the data.")
        print(self.data[["Product", "Sales", "Product_Total_Sales"]].head())

    # ---------------------- split data ----------------------

    def split_data(self, column_name):
        # splits the data into small DataFrames (one for each value)
        if not self.has_columns([column_name]):
            return None

        parts = {}
        for value in self.data[column_name].dropna().unique():
            parts[value] = self.data[self.data[column_name] == value]

        print("\nData split by", column_name)
        for value in parts:
            print(value, "->", len(parts[value]), "rows")
        return parts

    # ---------------------- search, sort, filter ----------------------

    def search_sort_filter(self, action, column, value=None, ascending=True):
        if not self.has_columns([column]):
            return None

        is_number_column = pd.api.types.is_numeric_dtype(self.data[column])

        # change the typed value to a number if column is numeric
        if value is not None and is_number_column:
            try:
                value = float(value)
            except ValueError:
                print("\nThis column needs a number value.")
                return None

        if action == "search":
            if is_number_column:
                result = self.data[self.data[column] == value]
            else:
                result = self.data[
                    self.data[column].astype(str).str.contains(value, case=False)
                ]
            print("\nSearch result:", len(result), "rows found")

        elif action == "sort":
            result = self.data.sort_values(by=column, ascending=ascending)
            print("\nData sorted by", column)

        elif action == "filter":
            if is_number_column:
                result = self.data[self.data[column] >= value]
            else:
                result = self.data[self.data[column] == value]
            print("\nFilter result:", len(result), "rows")

        else:
            print("Invalid action.")
            return None

        print(result.head(10))
        return result

    # ---------------------- aggregate functions ----------------------

    def aggregate_functions(self, column="Sales"):
        if not self.has_columns([column]):
            return
        if not pd.api.types.is_numeric_dtype(self.data[column]):
            print("\nPlease choose a number column.")
            return

        print("\n== Aggregate results for", column, "==")
        print("Sum   :", round(self.data[column].sum(), 2))
        print("Mean  :", round(self.data[column].mean(), 2))
        print("Count :", self.data[column].count())
        print("Min   :", self.data[column].min())
        print("Max   :", self.data[column].max())

        # same thing but for each region
        if "Region" in self.data.columns:
            print("\n", column, "by Region:")
            print(self.data.groupby("Region")[column].agg(["sum", "mean", "count"]).round(2))

    # ---------------------- statistics ----------------------

    def statistical_analysis(self):
        number_data = self.data.select_dtypes(include=np.number)

        print("\n== Descriptive Statistics ==")
        print(number_data.describe())

        print("\nStandard deviation:")
        print(number_data.std().round(2))

        print("\nVariance:")
        print(number_data.var().round(2))

        print("\nQuantiles (25%, 50%, 75%):")
        print(number_data.quantile([0.25, 0.5, 0.75]))

        # percentiles using numpy
        if "Sales" in self.data.columns:
            sales_array = self.data["Sales"].dropna().to_numpy()
            print("\nPercentiles of Sales (numpy):")
            for p in [10, 25, 50, 75, 90]:
                print(str(p) + "th percentile :", round(np.percentile(sales_array, p), 2))

    # ---------------------- pivot table ----------------------

    def create_pivot_table(self, index="Region", columns="Year", values="Sales", aggfunc="sum"):
        if not self.has_columns([index, columns, values]):
            return None

        pivot = pd.pivot_table(
            self.data,
            index=index,
            columns=columns,
            values=values,
            aggfunc=aggfunc,
            margins=True,
        )
        print("\nPivot table:", aggfunc, "of", values, "by", index, "and", columns)
        print(pivot.round(2))
        return pivot

    # ---------------------- advanced operations ----------------------

    def reindex_and_rename(self):
        # we use a copy so the main data does not change
        if not self.has_columns(["SalesID"]):
            return

        # reindex does not work if the index has repeated values,
        # so we keep only one row for each SalesID in this copy
        temp = self.data.drop_duplicates(subset="SalesID").set_index("SalesID")
        print("\nSalesID used as the index:")
        print(temp.head())

        # change column labels
        temp = temp.rename(columns={"Sales": "Total_Sales", "Profit": "Total_Profit"})

        # change index labels
        temp = temp.rename(index=lambda number: "ID-" + str(number))
        print("\nAfter renaming column and index labels:")
        print(temp.head())

        # reindex in reverse order
        temp = temp.reindex(temp.index[::-1])
        print("\nAfter re-indexing in reverse order:")
        print(temp.head())

    def groupby_transform(self):
        if not self.has_columns(["Region", "Sales"]):
            return

        # transform gives one value for every row (not one per group)
        self.data["Region_Avg_Sales"] = (
            self.data.groupby("Region")["Sales"].transform("mean").round(2)
        )
        self.data["Sales_Vs_Region_Avg"] = (
            self.data["Sales"] - self.data["Region_Avg_Sales"]
        ).round(2)

        print("\nNew columns added: Region_Avg_Sales, Sales_Vs_Region_Avg")
        print(self.data[["Region", "Sales", "Region_Avg_Sales", "Sales_Vs_Region_Avg"]].head())
