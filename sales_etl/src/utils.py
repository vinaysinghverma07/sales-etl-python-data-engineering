# 1st File


import logging
import yaml
import os
from pathlib import Path

"""
If your python version doesn't have the above mentioned library installed in it then first you have to first install 
it in your existing version so that it can create virtual environment for the same as well for running the package
"""


def get_project_root() -> Path:
    """
    The below green part is known as DocString of a function, which provides the clarity for the purpose & usage of it.

    Path is a return type of this function.

    Get project root directory.
    Assumes this file is located at: project_root/src/utils.py
    """
    return Path(__file__).resolve().parent.parent


def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    The below green part is known as DocString of a function, which provides the clarity, purpose & usage of function.

    In above line "config_path" is a parameter name, when the person/module will call the function then it will provide
    the values/argument to the function parameters as strings and "->dict" is a return means the final return output
    will be available in a dictionary datatype. However, default value is already given.

    Load YAML configuration file.

    Args:
        config_path (str): Path to config file default value

    Returns:
        dict: Configuration dictionary
    """
    project_root = get_project_root()
    full_config_path = project_root / config_path

    try:
        with open(full_config_path, "r") as file:
            config = yaml.safe_load(file)
            return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found at {full_config_path}")
    # except yaml.YAMLError as e:
    #     raise Exception(f"Error parsing YAML file: {e}")


def setup_logging(log_file_path: str, level: str = "INFO") -> logging.Logger:
    """
    The below green part is known as DocString of a function, which provides the clarity for the purpose & usage of it.

    In this function "log_file_path" is a argument with a datatype string and "level" is also a string datatype
    parameter default value is already given incase no value is being passed, and return type of "logger" which is
    a class of library logging.

    Setup logging configuration.
    Setup logging configuration ONCE for the application/run.

    Args:
        log_file_path (str): Path to log file
        level (str): Logging level

    Returns:
        logging.Logger: Configured logger
    """

    project_root = get_project_root()
    full_log_path = project_root / log_file_path

    # Ensure logs directory exists
    full_log_path.parent.mkdir(parents=True, exist_ok=True)

    # Commented out this code since logging is being used in different module and the error was not getting stored
    # because of the basic logging configuration
    # logging.basicConfig(
    #     level=getattr(logging, level),
    #     format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    #     handlers=[
    #         logging.FileHandler(full_log_path),
    #         logging.StreamHandler()
    #     ]
    # )
    # logger = logging.getLogger("SalesETL")

    # Get root logger
    logger = logging.getLogger()
    logger.setLevel(getattr(logging, level))

    # Avoid duplicate handlers
    if logger.handlers:
        return

    # Create log formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

    # File handler (writes logs to file)
    file_handler = logging.FileHandler(full_log_path)
    file_handler.setFormatter(formatter)

    # Console handler (prints logs to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # Attach handlers to root logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
