"""
Process a CSV file to determine the top 10 states with the most failed banks 
and their percentage of total bank failures.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import csv
from collections import Counter

# Import from local project modules
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

fetched_folder_name: str = "data"
processed_folder_name: str = "processed"

#####################################
# Define Functions
#####################################

def get_top_10_states(file_path: pathlib.Path) -> list:
    """
    Analyze the CSV file to find the top 10 states with the most failed banks
    and calculate their percentage of total failures.

    Args:
        file_path (pathlib.Path): Path to the CSV file.

    Returns:
        list: List of tuples containing state, count, and percentage of total failures.
    """
    try:
        # Initialize a Counter to store failed bank counts by state
        state_counts = Counter()

        with file_path.open('r', encoding='utf-8-sig') as file:
            csv_reader = csv.DictReader(file)

            # Normalize column names by stripping whitespace and removing non-breaking spaces
            csv_reader.fieldnames = [col.strip().replace("\xa0", "") for col in csv_reader.fieldnames]

            # Check if the expected "State" column exists in the CSV
            if "State" not in csv_reader.fieldnames:
                logger.error(f"CSV missing 'State' column. Found headers: {csv_reader.fieldnames}")
                return []

            for row in csv_reader:
                state = row.get("State", "").strip()  # Ensure no whitespace issues
                if state:  
                    state_counts[state] += 1  # Increment count for the state
        
        if not state_counts:
            logger.error("No state data found in CSV file.")
            return []

        # Get total failed banks
        total_failures = sum(state_counts.values())

        # Sort by highest count and get the top 10 states
        top_10 = state_counts.most_common(10)

        # Calculate percentage of total failures for each state
        top_10_percentages = [(state, count, (count / total_failures) * 100) for state, count in top_10]

        return top_10_percentages

    except Exception as e:
        logger.error(f"Error processing CSV file: {e}")
        return []


def process_csv_file():
    """
    Read a CSV file, compute the top 10 states with the most failed banks,
    and save the results to a text file in the 'data_processed' folder.
    """
    input_file = pathlib.Path(fetched_folder_name, "FDIC_failed_bank_list.csv")
    output_file = pathlib.Path("data_processed", "top_10_states_failed_banks.txt")  # Updated output path

    top_10_states = get_top_10_states(input_file)

    with output_file.open('w', encoding='utf-8') as file:
        file.write("Top 10 States with Most Failed Banks:\n")
        file.write("=" * 40 + "\n")
        file.write(f"{'State':<10}{'Count':<10}{'Percentage'}\n")
        file.write("=" * 40 + "\n")

        for state, count, percentage in top_10_states:
            file.write(f"{state:<10}{count:<10}{percentage:.2f}%\n")

    logger.info(f"Processed CSV file: {input_file}, Statistics saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting CSV processing...")
    process_csv_file()
    logger.info("CSV processing complete.")
