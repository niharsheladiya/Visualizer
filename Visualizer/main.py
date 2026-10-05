# Welcome to Main File

from sales_visualizer import SalesVisualizer
from menu import run_menu


def main():
    
    analyzer = SalesVisualizer()
    run_menu(analyzer)


if __name__ == "__main__":
    main()
