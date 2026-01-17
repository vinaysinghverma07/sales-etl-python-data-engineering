import pandas as pd

from src.extract import extract_data
from src.transform import transform_data
from src.utils import load_config, setup_logging
from src.load import load_data
import pandas as pd

# Load config once
config = load_config()

# Setup logging ONCE
logger = setup_logging(
    config["log_file_path"],
    config["logging"]["level"]
)

df_raw = extract_data(config, logger)
df_clean = transform_data(df_raw, logger)
empty_df = pd.DataFrame
# df_load = load_data(df_clean, config, logger)
df_load = load_data(df_clean, config, logger)

# print(df_raw.columns)
# print(df_raw.head())


print(df_clean)
