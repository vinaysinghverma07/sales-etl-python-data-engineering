# 3rd File

# =========================
# IMPORTS
# =========================

import pandas as pd
# pandas is a third-party library used for data manipulation and analysis
# pd.read_csv() will be used to read CSV files into DataFrames

from pathlib import Path
# pathlib is a STANDARD PYTHON LIBRARY
# Path is used for safe and OS-independent file path handling

from src.utils import get_project_root, load_config, setup_logging
from typing import Dict

# load_config -> our custom function from utils.py
# setup_logging -> our custom logging setup function


# =========================
# EXTRACT FUNCTION
# =========================

def extract_data(config: dict, logger) -> pd.DataFrame:
    """
    The below green part is known as DocString of a function, which provides the clarity for the purpose & usage of it.

    pd.dataframe is a return type of this function which is a part of pandas (third party library for python DA)

    Extract raw sales data from CSV file.

    Returns:
        pandas.DataFrame: Raw sales data
    """

    # Commented below lines since logging needs to initialized once only
    # Load configuration from config/config.yaml
    # load_config() is defined in utils.py
    # config = load_config()
    #
    # # Setup logging using values from config
    # # logging library is used internally by setup_logging()
    # logger = setup_logging(
    #     config["log_file_path"],
    #     config["logging"]["level"]
    # )

    logger.info("Starting data extraction step")

    # Get project root directory using pathlib.Path
    # Path comes from pathlib (standard library)
    # project_root = Path(__file__).resolve().parent.parent

    project_root = get_project_root()

    # Build full path to raw data file
    # config["raw_data_path"] is a RELATIVE path from config.yaml

    raw_data_path = project_root / config["raw_data_path"]

    logger.info(f"Raw data path resolved to: {raw_data_path}")

    # =========================
    # FILE EXISTENCE CHECK
    # =========================

    # Path.exists() is a method from pathlib.Path
    if not raw_data_path.exists():
        logger.error(f"Raw data file does not exist: {raw_data_path}")
        raise FileNotFoundError(f"Raw data file not found: {raw_data_path}")

    # =========================
    # READ CSV FILE
    # =========================

    try:
        # pd.read_csv() is from pandas library
        # It reads CSV file and returns a DataFrame
        # Added seperator since we saw an error where csv was reading in different format or was saved in different
        # format

        df = pd.read_csv(raw_data_path, sep=None, engine="python", encoding="utf-8-sig")

        # =========================
        # HEADER NORMALIZATION
        # =========================

        # Case: Entire row is packed into first column (Excel corruption)
        if len(df.columns) <= 2 and "," in df.columns[0]:
            logger.warning(
                "Detected malformed CSV structure. Normalizing columns and data."
            )

            # Extract correct column names
            corrected_columns = df.columns[0].split(",")

            # Split the single column into multiple columns
            df = df[df.columns[0]].str.split(",", expand=True)

            # Assign corrected column names
            df.columns = corrected_columns

            logger.info(f"Corrected columns after normalization: {df.columns.tolist()}")

            # Log schema for debugging
            logger.info(f"Extracted columns: {list(df.columns)}")
            logger.info(
                f"Successfully extracted data | Rows: {df.shape[0]} | Columns: {df.shape[1]}"
            )

        # Schema validation (production mindset)
        expected_columns = {
            "order_id", "order_date", "customer_id",
            "product", "quantity", "price"
        }

        # Cross Validating expected columns with columns that got fetched from file
        if not expected_columns.issubset(df.columns):
            logger.error("CSV schema mismatch detected")
            raise ValueError(
                f"Expected columns {expected_columns}, but got {set(df.columns)}"
            )

        return df

    except pd.errors.EmptyDataError:
        # pandas raises EmptyDataError if file exists but is empty
        logger.error("Raw data file is empty")
        raise

    except Exception as e:
        # Catch any unexpected error
        logger.error(f"Unexpected error during data extraction: {e}")
        raise
