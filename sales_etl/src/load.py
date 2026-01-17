# 5th File
""" Loading transformed data into csv
FYI: Argument validation happens BEFORE function execution.
"""

# =========================
# IMPORTS
# =========================

import pandas as pd
from pathlib import Path
from datetime import datetime

# =========================
# LOAD FUNCTION
# =========================


def load_data(df: pd.DataFrame, config: dict, logger) -> None:
    """
    Load transformed data to target destination.

    Args:
        df (pd.DataFrame): Transformed data
        config (dict): Application configuration
        logger (logging.Logger): Shared logger

    Returns:
        None
    """

    logger.info("Starting data load step")

    # =========================
    # VALIDATION
    # =========================

    if df.empty:
        logger.error("Cannot load empty DataFrame")
        raise ValueError("Load step received empty DataFrame")

    required_columns = {
        "order_id", "order_date", "customer_id",
        "product", "quantity", "price", "revenue"
    }

    if not required_columns.issubset(df.columns):
        logger.error("Final schema validation failed before load")
        raise ValueError(
            f"Expected columns {required_columns}, but got {set(df.columns)}"
        )

    logger.info("Final schema validation passed")

    # =========================
    # RESOLVE OUTPUT PATH
    # =========================

    project_root = Path(__file__).resolve().parents[1]
    output_path = project_root / config["processed_data_path"]

    # Ensure directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Resolved output path: {output_path}")

    # =========================
    # WRITE DATA
    # =========================

    try:
        # df.to_csv(output_path, index=False)

        # Ensure output directory exists
        output_dir = Path(output_path)
        output_dir.mkdir(parents=True, exist_ok=True)

        # Create versioned output file
        output_file = output_dir / f"sales_processed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

        df.to_csv(output_file, index=False)

        logger.info(
            f"Data successfully written and loaded to {output_file} with Rows: {df.shape[0]} | Columns: {df.shape[1]}"
        )

        logger.info("Data load step completed successfully")
    except PermissionError:
        logger.exception(f"Permission Denied while loading data to {output_file}")
        raise
    except Exception:
        logger.exception(f"Unexpected error occurred while loading data to {output_file}")
        raise
