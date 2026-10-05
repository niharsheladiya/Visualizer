# Welcome to Menu File


def show_main_menu():
    print("\n========== Data Analysis & Visualization Program ==========")
    print("Please select an option:")
    print("1. Load Dataset")
    print("2. Explore Data")
    print("3. Perform DataFrame Operations")
    print("4. Handle Missing Data")
    print("5. Generate Descriptive Statistics")
    print("6. Data Visualization")
    print("7. Save Visualization")
    print("8. Exit")
    print("=" * 59)


def ask_number(message):
    
    while True:
        text = input(message).strip()
        if text.isdigit():
            return int(text)
        print("Please enter a number only.")


# option 1 

def load_dataset_menu(analyzer):
    print("\n== Load Dataset ==")
    file_path = input("Enter the path of the dataset (CSV file): ").strip()
    
    file_path = file_path.strip('"').strip("'")
    analyzer.load_data(file_path)


# option 2

def explore_menu(analyzer):
    print("\n== Explore Data ==")
    print("1. Display the first 5 rows")
    print("2. Display the last 5 rows")
    print("3. Display column names")
    print("4. Display data types")
    print("5. Display basic info")
    choice = ask_number("Enter your choice: ")
    print()
    analyzer.explore_data(choice)


# option 3

def operations_menu(analyzer):
    print("\n== DataFrame Operations ==")
    print("1. NumPy arrays (indexing and slicing)")
    print("2. Mathematical operations")
    print("3. Combine data (concat / merge)")
    print("4. Split data")
    print("5. Search, sort or filter")
    print("6. Aggregate functions (sum, mean, count)")
    print("7. Create pivot table")
    print("8. Re-index and rename labels")
    print("9. Group by and transform")
    choice = ask_number("Enter your choice: ")

    if choice == 1:
        analyzer.numpy_operations()

    elif choice == 2:
        analyzer.mathematical_operations()

    elif choice == 3:
        print("\n1. Add rows from another CSV file (concat)")
        print("2. Merge total sales of each product (merge)")
        sub_choice = ask_number("Enter your choice: ")
        if sub_choice == 1:
            other_path = input("Enter the path of the second CSV file: ").strip()
            other_path = other_path.strip('"').strip("'")
            other_data = analyzer.read_other_file(other_path)
            if other_data is not None:
                analyzer.combine_data(other_data)
        elif sub_choice == 2:
            analyzer.merge_product_totals()
        else:
            print("Invalid choice.")

    elif choice == 4:
        print("\n1. Split by Region")
        print("2. Split by Product")
        sub_choice = ask_number("Enter your choice: ")
        if sub_choice == 1:
            column_name = "Region"
        elif sub_choice == 2:
            column_name = "Product"
        else:
            print("Invalid choice.")
            return
        parts = analyzer.split_data(column_name)
        if parts is not None:
            name = input("\nType a name to see its rows (or press Enter to skip): ").strip()
            if name in parts:
                print(parts[name].head())

    elif choice == 5:
        print("\n1. Search")
        print("2. Sort")
        print("3. Filter")
        sub_choice = ask_number("Enter your choice: ")
        if sub_choice not in [1, 2, 3]:
            print("Invalid choice.")
            return
        column = input("Enter column name: ").strip()
        if sub_choice == 1:
            value = input("Enter the value to search: ").strip()
            analyzer.search_sort_filter("search", column, value)
        elif sub_choice == 2:
            order = input("Ascending order? (y/n): ").strip().lower()
            analyzer.search_sort_filter("sort", column, ascending=(order == "y"))
        else:
            print("(number column: rows >= value, text column: rows equal to value)")
            value = input("Enter the value to filter: ").strip()
            analyzer.search_sort_filter("filter", column, value)

    elif choice == 6:
        column = input("Enter column name (press Enter for Sales): ").strip()
        if column == "":
            column = "Sales"
        analyzer.aggregate_functions(column)

    elif choice == 7:
        analyzer.create_pivot_table()

    elif choice == 8:
        analyzer.reindex_and_rename()

    elif choice == 9:
        analyzer.groupby_transform()

    else:
        print("Invalid choice.")


# option 4 

def missing_data_menu(analyzer):
    print("\n== Handle Missing Data ==")
    print("1. Display rows with missing values")
    print("2. Fill missing values with mean")
    print("3. Drop rows with missing values")
    print("4. Replace missing values with a specific value")
    choice = ask_number("Enter your choice: ")

    if choice == 4:
        column = input("Enter column name: ").strip()
        value = input("Enter the value to use: ").strip()
        analyzer.clean_data(4, column, value)
    else:
        analyzer.clean_data(choice)


# option 6 

def visualization_menu(analyzer):
    print("\n== Data Visualization ==")
    print("1. Bar Plot")
    print("2. Line Plot")
    print("3. Scatter Plot")
    print("4. Pie Chart")
    print("5. Histogram")
    print("6. Stack Plot")
    print("7. Subplots (4 plots in one figure)")
    print("8. Heatmap (Seaborn)")
    print("9. Box Plot (Seaborn)")
    choice = ask_number("Enter your choice: ")

    if choice == 3:
        print("\n== Scatter Plot ==")
        x_column = input("Enter x-axis column name: ").strip()
        y_column = input("Enter y-axis column name: ").strip()
        analyzer.visualize_data(3, x_column, y_column)
    else:
        print()
        analyzer.visualize_data(choice)


# option 7

def save_visualization_menu(analyzer):
    print("\n== Save Visualization ==")
    file_name = input("Enter file name to save the plot (e.g., scatter_plot.png): ").strip()
    analyzer.save_visualization(file_name)


# main loop 

def run_menu(analyzer):
    while True:
        show_main_menu()
        choice = ask_number("\nEnter your choice: ")

        if choice == 1:
            load_dataset_menu(analyzer)

        elif choice == 2:
            if analyzer.is_data_loaded():
                explore_menu(analyzer)

        elif choice == 3:
            if analyzer.is_data_loaded():
                operations_menu(analyzer)

        elif choice == 4:
            if analyzer.is_data_loaded():
                missing_data_menu(analyzer)

        elif choice == 5:
            if analyzer.is_data_loaded():
                analyzer.statistical_analysis()

        elif choice == 6:
            if analyzer.is_data_loaded():
                visualization_menu(analyzer)

        elif choice == 7:
            save_visualization_menu(analyzer)

        elif choice == 8:
            print("\nExiting the program. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter a number from 1 to 8.")
