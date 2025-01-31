"""
This example file fetches an Excel file from the web 
and saves it to a local file named national_stock_number_2023.xlsx in a folder named data.

Please save a copy of the provided utils_logger.py file 
in the same folder as this file.
"""

#####################################
# Import Modules at the Top
#####################################

# Import from Python Standard Library
import pathlib

# Import from external packages
import requests

# Import from local project modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

fetched_folder_name = "data"

#####################################
# Define Functions
#####################################

def fetch_excel_file(folder_name: str, filename: str, url: str) -> None:
    """
    Fetch Excel data from the given URL and write it to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file (with .xlsx extension).
        url (str): URL of the Excel file to fetch.

    Returns:
        None

    Example:
        fetch_excel_file("data", "data.xlsx", "https://example.com/data.xlsx")
    """
    if not url:
        logger.error("The URL provided is empty. Please provide a valid URL.")
        return

    try:
        logger.info(f"Fetching Excel data from {url}...")
        response = requests.get(url, stream=True)  # Stream for large files
        response.raise_for_status()

        # Ensure filename has .xlsx extension
        if not filename.endswith(".xlsx"):
            filename += ".xlsx"

        write_excel_file(folder_name, filename, response.content)
        logger.info(f"SUCCESS: Excel file fetched and saved as {filename}")

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")

def write_excel_file(folder_name: str, filename: str, binary_data: bytes) -> None:
    """
    Write Excel binary data to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        binary_data (bytes): Binary content of the Excel file.

    Returns:
        None
    """
    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        logger.info(f"Writing Excel data to {file_path}...")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with file_path.open('wb') as file:
            file.write(binary_data)
        logger.info(f"SUCCESS: Excel data written to {file_path}")
    except IOError as io_err:
        logger.error(f"Error writing Excel data to {file_path}: {io_err}")

#####################################
# Define main() function
#####################################

def main():
    """
    Main function to demonstrate fetching Excel data.
    """
    excel_url = "https://inventory.data.gov/dataset/67567804-073d-40ad-a710-2b0bed8b84e2/resource/3b7ed6b7-7dce-42f1-852d-6465e3e790e4/download/nsn-extract-2-21-23.xls.xlsx"
    logger.info("Starting Excel fetch demonstration...")

    # Ensure filename has correct extension
    fetch_excel_file(fetched_folder_name, "national_stock_number_2023.xlsx", excel_url)

#####################################
# Conditional Execution
#####################################

if __name__ == '__main__':
    main()

