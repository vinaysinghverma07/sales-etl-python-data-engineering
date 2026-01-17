# 2nd File

from utils import load_config, setup_logging
config = load_config()
logger = setup_logging(
    config["log_file_path"],
    config["logging"]["level"]
)

logger.info("Logging system initialized successfully")
