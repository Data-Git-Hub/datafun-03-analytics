"""
Process an Excel file to determine the NSN, common_name, and highest price for each rep_office.

"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib

# Import from external packages
import openpyxl

# Import from local project modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

fetched_folder_name: str = "data"
processed_folder_name: str = "data_processed"

#####################################
# Define Functions
#####################################

def find_highest_price_nsn(file_path: pathlib.Path) -> dict:
    """
    Find the NSN, common_name, and highest price for each rep_office.

    Args:
        file_path (pathlib.Path): Path to the Excel file.

    Returns:
        dict: Dictionary with rep_office as key and (NSN, common_name, Price) tuple as value.
    """
    try:
        workbook = openpyxl.load_workbook(file_path, data_only=True)
        sheet = workbook.active
        
        # Find column indexes from headers
        headers = [cell.value for cell in sheet[1]]  # Read first row as headers
        
        required_columns = {"NSN", "rep_office", "common_name", "Price"}
        if not required_columns.issubset(set(headers)):
            logger.error(f"Missing required columns in Excel file. Found headers: {headers}")
            return {}

        nsn_idx = headers.index("NSN") + 1
        rep_office_idx = headers.index("rep_office") + 1
        common_name_idx = headers.index("common_name") + 1
        price_idx = headers.index("Price") + 1

        rep_office_highest = {}

        for row in sheet.iter_rows(min_row=2, values_only=True):
            rep_office = row[rep_office_idx - 1]
            nsn = row[nsn_idx - 1]
            common_name = row[common_name_idx - 1]
            price = row[price_idx - 1]

            # Ensure data validity
            if rep_office and nsn and common_name and isinstance(price, (int, float)):
                if rep_office not in rep_office_highest or price > rep_office_highest[rep_office][2]:
                    rep_office_highest[rep_office] = (nsn, common_name, price)

        return rep_office_highest

    except Exception as e:
        logger.error(f"Error processing Excel file: {e}")
        return {}

def process_excel_file():
    """Read an Excel file, find the highest-priced NSN per rep_office, and save the result."""
    input_file = pathlib.Path(fetched_folder_name, "national_stock_number_2023.xlsx")
    output_file = pathlib.Path(processed_folder_name, "highest_price_nsn_per_rep_office.txt")

    # Get highest price NSN for each rep_office
    highest_prices = find_highest_price_nsn(input_file)

    # Save to text file
    with output_file.open('w', encoding='utf-8') as file:
        file.write("Highest Price NSN per rep_office:\n")
        file.write("=" * 80 + "\n")
        file.write(f"{'Rep Office':<20}{'NSN':<20}{'Common Name':<20}{'Price'}\n")
        file.write("=" * 80 + "\n")

        for rep_office, (nsn, common_name, price) in highest_prices.items():
            file.write(f"{rep_office:<20}{nsn:<20}{common_name:<20}{price:.2f}\n")

    logger.info(f"Processed Excel file: {input_file}, Statistics saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting Excel processing...")
    process_excel_file()
    logger.info("Excel processing complete.")
