"""
Process a JSON file to find the top 10 states with the most disability compensation recipients
and calculate the percentage of those recipients with an SCD rating of 100%.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import json
import pandas as pd
from utils_logger import logger

#####################################
# Declare Global Variables
#####################################

fetched_folder_name: str = "data"
processed_folder_name: str = "data_processed"

#####################################
# Define Functions
#####################################

def get_top_10_states(file_path: pathlib.Path):
    """Find the top 10 states with the most 'Total: Disability Compensation Recipients' and
    calculate the percentage of 'SCD rating: 100%' in those states."""
    try:
        with file_path.open('r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Load data into DataFrame
        df = pd.DataFrame(data["data"])
        
        # Extract column names from metadata
        headers = [col["name"] for col in data["meta"]["view"]["columns"]]
        df.columns = headers
        
        # Convert necessary columns to numeric values
        df["Total: Disability Compensation Recipients"] = pd.to_numeric(df["Total: Disability Compensation Recipients"], errors='coerce')
        df["SCD rating: 100%"] = pd.to_numeric(df["SCD rating: 100%"], errors='coerce')
        
        # Group by state and sum the relevant columns
        state_totals = df.groupby("State")[
            ["Total: Disability Compensation Recipients", "SCD rating: 100%"]
        ].sum()
        
        # Identify top 10 states by total recipients
        top_10_states = state_totals.nlargest(10, "Total: Disability Compensation Recipients")
        
        # Calculate the percentage of 100% SCD ratings in these states
        top_10_states["Percentage SCD 100%"] = (
            top_10_states["SCD rating: 100%"] / top_10_states["Total: Disability Compensation Recipients"] * 100
        )
        
        return top_10_states
    except Exception as e:
        logger.error(f"Error processing JSON file: {e}")
        return None

def process_json_file():
    """Process the JSON file and save the results to a text file."""
    input_file = pathlib.Path(fetched_folder_name, "usvet_cp_state_county.json")
    output_file = pathlib.Path(processed_folder_name, "top_10_states_scd_100_percentage.txt")
    
    top_10_states = get_top_10_states(input_file)
    if top_10_states is None:
        logger.error("No valid data found to process.")
        return
    
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with output_file.open('w', encoding='utf-8') as file:
        file.write("Top 10 States with Most Disability Compensation Recipients:\n")
        file.write("=" * 60 + "\n")
        file.write(f"{'State':<20}{'Total Recipients':<20}{'SCD 100% Percentage'}\n")
        file.write("=" * 60 + "\n")
        
        for state, row in top_10_states.iterrows():
            file.write(f"{state:<20}{int(row['Total: Disability Compensation Recipients']):<20}{row['Percentage SCD 100%']:.2f}%\n")
    
    logger.info(f"Processed JSON file: {input_file}, Results saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting JSON processing...")
    process_json_file()
    logger.info("JSON processing complete.")

