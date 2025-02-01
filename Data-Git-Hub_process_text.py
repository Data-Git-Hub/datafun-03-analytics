"""
Process a text file to count the top 50 occurrences in the United States Constitution 
while excluding the first 128 lines and stopping at line 666.
"""

#####################################
# Import Modules
#####################################

# Import from Python Standard Library
import pathlib
import collections
import re

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

def count_top_words(file_path: pathlib.Path, top_n: int = 50, skip_lines: int = 128, stop_line: int = 666) -> list:
    """
    Count word occurrences in a text file, analyzing only lines from skip_lines to stop_line.
    
    Args:
        file_path (pathlib.Path): Path to the text file.
        top_n (int): Number of top words to retrieve.
        skip_lines (int): Number of initial lines to exclude from counting.
        stop_line (int): Line number to stop processing.

    Returns:
        list: List of tuples containing word and its count.
    """
    try:
        word_counts = collections.Counter()

        with file_path.open('r', encoding="utf-8") as file:
            lines = file.readlines()

        # Ensure we are within valid line range
        if len(lines) < skip_lines:
            logger.error(f"File has fewer than {skip_lines} lines. Adjust the skip_lines value.")
            return []

        content = " ".join(lines[skip_lines:stop_line])  # Get only the required section of text

        # Normalize text by removing punctuation and converting to lowercase
        words = re.findall(r'\b[a-zA-Z]+\b', content.lower())

        # Count occurrences
        word_counts.update(words)

        return word_counts.most_common(top_n)

    except Exception as e:
        logger.error(f"Error processing text file: {e}")
        return []

def process_text_file():
    """Read a text file, count the top 50 occurrences within a specific line range, and save the result."""
    input_file = pathlib.Path(fetched_folder_name, "usconstitution.txt")
    output_file = pathlib.Path(processed_folder_name, "top_50_words.txt")

    # Get top 50 words from the valid line range
    top_words = count_top_words(input_file, top_n=50, skip_lines=128, stop_line=666)

    # Ensure output folder exists
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Save results
    with output_file.open('w', encoding="utf-8") as file:
        file.write("Top 50 Most Frequent Words (Lines 128-666):\n")
        file.write("=" * 50 + "\n")
        file.write(f"{'Word':<15}{'Count'}\n")
        file.write("=" * 50 + "\n")

        for word, count in top_words:
            file.write(f"{word:<15}{count}\n")

    logger.info(f"Processed text file: {input_file}, Word counts saved to: {output_file}")

#####################################
# Main Execution
#####################################

if __name__ == "__main__":
    logger.info("Starting text processing...")
    process_text_file()
    logger.info("Text processing complete.")
