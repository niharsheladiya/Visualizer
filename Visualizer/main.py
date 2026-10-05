# main.py
# --------------------------------------------------------------
# Run this file to start the program:   python main.py
#
# Files in this project:
#   create_dataset.py   -> makes sales_data.csv
#   sales_analyzer.py   -> SalesDataAnalyzer class (data work)
#   sales_visualizer.py -> SalesVisualizer class (plots)
#   menu.py             -> menu / user interface
#   main.py             -> starts the program
# --------------------------------------------------------------

from sales_visualizer import SalesVisualizer
from menu import run_menu


def main():
    # make the object (no file loaded yet, user loads it from the menu)
    analyzer = SalesVisualizer()
    run_menu(analyzer)


if __name__ == "__main__":
    main()
