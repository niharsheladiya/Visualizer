# Welcome to Sales Visualizer File

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


from sales_analyzer import SalesDataAnalyzer


class SalesVisualizer(SalesDataAnalyzer):

    def __init__(self, file_path=None):
       
        self.last_figure = None
        super().__init__(file_path)
        sns.set_theme(style="whitegrid")

    
    def load_data(self, file_path):
        loaded = super().load_data(file_path)
        self.last_figure = None
        return loaded

# small helper methods

    def _show_plot(self, fig, plot_name):
        fig.tight_layout()
        self.last_figure = fig
        plt.show()
        print(plot_name + " displayed successfully!")

    def _monthly_labels(self):
       
        return self.data["Date"].dt.strftime("%Y-%m")

    def _show_every_third_month(self, ax, labels):
       
        ax.set_xticks(range(0, len(labels), 3))
        ax.set_xticklabels(labels[::3], rotation=45)

# drawing parts (used by plots and subplots)

    def _draw_bar(self, ax):
        sales_by_region = self.data.groupby("Region")["Sales"].sum()
        ax.bar(sales_by_region.index, sales_by_region.values,
               color="skyblue", edgecolor="black", label="Total Sales")
        ax.set_title("Total Sales by Region")
        ax.set_xlabel("Region")
        ax.set_ylabel("Total Sales")
        ax.legend()

    def _draw_line(self, ax):
        monthly_sales = self.data.groupby(self._monthly_labels())["Sales"].sum()
        ax.plot(monthly_sales.index, monthly_sales.values,
                marker="o", color="green", label="Monthly Sales")
        self._show_every_third_month(ax, monthly_sales.index)
        ax.set_title("Monthly Sales Trend")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Sales")
        ax.legend()

    def _draw_pie(self, ax):
        sales_by_product = self.data.groupby("Product")["Sales"].sum()
        ax.pie(sales_by_product.values, labels=sales_by_product.index,
               autopct="%1.1f%%", startangle=90)
        ax.set_title("Sales Share of Each Product")
       
        ax.legend(title="Product", loc="center left", bbox_to_anchor=(1, 0.5))

    def _draw_histogram(self, ax):
        ax.hist(self.data["Sales"].dropna(), bins=20,
                color="orange", edgecolor="black", label="Sales")
        ax.set_title("Distribution of Sales")
        ax.set_xlabel("Sales")
        ax.set_ylabel("Number of Orders")
        ax.legend()

# Matplotlib plots

    def bar_plot(self):
        if not self.has_columns(["Region", "Sales"]):
            return
        print("Generating bar plot...")
        fig, ax = plt.subplots(figsize=(8, 5))
        self._draw_bar(ax)
        self._show_plot(fig, "Bar plot")

    def line_plot(self):
        if not self.has_columns(["Date", "Sales"]):
            return
        print("Generating line plot...")
        fig, ax = plt.subplots(figsize=(10, 5))
        self._draw_line(ax)
        self._show_plot(fig, "Line plot")

    def scatter_plot(self, x_column, y_column):
        if not self.has_columns([x_column, y_column]):
            return
        print("Generating scatter plot...")
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.scatter(self.data[x_column], self.data[y_column],
                   color="red", alpha=0.6, label=x_column + " vs " + y_column)
        ax.set_title("Scatter Plot: " + x_column + " vs " + y_column)
        ax.set_xlabel(x_column)
        ax.set_ylabel(y_column)
        ax.legend()
        self._show_plot(fig, "Scatter plot")

    def pie_chart(self):
        if not self.has_columns(["Product", "Sales"]):
            return
        print("Generating pie chart...")
        fig, ax = plt.subplots(figsize=(7, 7))
        self._draw_pie(ax)
        self._show_plot(fig, "Pie chart")

    def histogram(self):
        if not self.has_columns(["Sales"]):
            return
        print("Generating histogram...")
        fig, ax = plt.subplots(figsize=(8, 5))
        self._draw_histogram(ax)
        self._show_plot(fig, "Histogram")

    def stack_plot(self):
        if not self.has_columns(["Date", "Region", "Sales"]):
            return
        print("Generating stack plot...")


# rows = months, columns = regions, values = total sales
        monthly_region = self.data.pivot_table(
            index=self._monthly_labels(),
            columns="Region",
            values="Sales",
            aggfunc="sum",
        ).fillna(0)

        fig, ax = plt.subplots(figsize=(10, 5))
        x_positions = range(len(monthly_region))
        y_values = [monthly_region[region] for region in monthly_region.columns]
        ax.stackplot(x_positions, y_values, labels=monthly_region.columns)
        self._show_every_third_month(ax, monthly_region.index)
        ax.set_title("Monthly Sales by Region (Stack Plot)")
        ax.set_xlabel("Month")
        ax.set_ylabel("Total Sales")
        ax.legend(title="Region", loc="center left", bbox_to_anchor=(1, 0.5))
        self._show_plot(fig, "Stack plot")

    def subplots_plot(self):
        
        if not self.has_columns(["Date", "Region", "Product", "Sales"]):
            return
        print("Generating subplots...")
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        self._draw_bar(axes[0, 0])
        self._draw_pie(axes[0, 1])
        self._draw_histogram(axes[1, 0])
        self._draw_line(axes[1, 1])
        fig.suptitle("Sales Dashboard", fontsize=16)
        self._show_plot(fig, "Subplots")

# Seaborn plots

    def heatmap_plot(self):
        print("Generating heatmap...")
        number_data = self.data.select_dtypes(include=np.number)
        number_data = number_data.drop(columns=["SalesID"], errors="ignore")
        correlation = number_data.corr()

        fig, ax = plt.subplots(figsize=(8, 6))
        sns.heatmap(correlation, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap")
        self._show_plot(fig, "Heatmap")

    def box_plot(self):
        if not self.has_columns(["Region", "Sales"]):
            return
        print("Generating box plot...")
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.boxplot(x="Region", y="Sales", data=self.data, color="lightblue", ax=ax)
        ax.set_title("Sales Spread in Each Region")
        self._show_plot(fig, "Box plot")


 # main method for visualization 

    def visualize_data(self, choice, x_column=None, y_column=None):
        if choice == 1:
            self.bar_plot()
        elif choice == 2:
            self.line_plot()
        elif choice == 3:
            self.scatter_plot(x_column, y_column)
        elif choice == 4:
            self.pie_chart()
        elif choice == 5:
            self.histogram()
        elif choice == 6:
            self.stack_plot()
        elif choice == 7:
            self.subplots_plot()
        elif choice == 8:
            self.heatmap_plot()
        elif choice == 9:
            self.box_plot()
        else:
            print("Invalid choice.")

# save the plot

    def save_visualization(self, file_name):
        if self.last_figure is None:
            print("\nThere is no plot to save. Please create a plot first (option 6).")
            return

        
        if "." not in file_name:
            file_name = file_name + ".png"

        try:
            self.last_figure.savefig(file_name, dpi=150)
            print("Visualization saved as " + file_name + " successfully!")
        except Exception as error:
            print("Could not save the plot:", error)
