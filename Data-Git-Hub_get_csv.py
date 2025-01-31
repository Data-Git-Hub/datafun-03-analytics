"""
This example file fetches a CSV file from the web 
and saves it to a local file named FDIC_bank_list.csv in a folder named data.

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

def fetch_csv_file(folder_name: str, filename: str, url: str) -> None:
    """
    Fetch CSV data from the given URL and write it to a file.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        url (str): URL of the CSV file to fetch.

    Returns:
        None
    """
    if not url:
        logger.error("The URL provided is empty. Please provide a valid URL.")
        return

    try:
        logger.info(f"Fetching CSV data from {url}...")
        response = requests.get(url)
        response.raise_for_status()

        # Try decoding with utf-8-sig first, then fall back to ISO-8859-1 (Latin-1)
        try:
            csv_content = response.content.decode('utf-8-sig')
        except UnicodeDecodeError:
            logger.warning("UTF-8 decoding failed. Trying ISO-8859-1 (Latin-1)...")
            csv_content = response.content.decode('ISO-8859-1')  # Fix encoding issue

        write_csv_file(folder_name, filename, csv_content)
        logger.info(f"SUCCESS: CSV file fetched and saved as {filename}")

    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        logger.error(f"Request error occurred: {req_err}")

def write_csv_file(folder_name: str, filename: str, string_data: str) -> None:
    """
    Write CSV data to a file with UTF-8 encoding.

    Args:
        folder_name (str): Name of the folder to save the file.
        filename (str): Name of the output file.
        string_data (str): CSV content as a string.

    Returns:
        None
    """
    file_path = pathlib.Path(folder_name).joinpath(filename)
    try:
        logger.info(f"Writing CSV data to {file_path}...")
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write file using UTF-8 encoding
        with file_path.open('w', encoding='utf-8', newline='') as file:  
            file.write(string_data)

        logger.info(f"SUCCESS: CSV data written to {file_path}")
    except IOError as io_err:
        logger.error(f"Error writing CSV data to {file_path}: {io_err}")

#####################################
# Define main() function
#####################################

def main():
    """
    Main function to demonstrate fetching CSV data.
    """
    csv_url = 'https://www.fdic.gov/bank-failures/download-data'
    logger.info("Starting CSV fetch demonstration...")
    fetch_csv_file(fetched_folder_name, "FDIC_failed_bank_list.csv", csv_url)

#####################################
# Conditional Execution
#####################################

if __name__ == '__main__':
    main()
