# Sales Data ETL Pipeline using Python ###

## 📌 Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline using Python, following production-grade data engineering best practices.

## The pipeline:
1. Extracts raw sales data from CSV.
2. Validates and cleans the data.
3. Applies business transformations.
4. Loads the processed data into a structured output folder.
5. Implements centralized logging, configuration management, and error handling.


This project is designed to simulate real-world data engineering workflows, not just scripting.

## 🏗️ Architecture Overview:

    Raw CSV
    │
    ▼
    Extract Module
    │
    ▼
    Transform Module
    │
    ▼
    Load Module
    │
    ▼
    Processed CSV + Logs

## Key architectural principles:
  1. Config-driven design
  2. Centralized logging
  3. Modular codebase
  4. Production-safe validations

## 📂 Project Structure:

    sales_etl/
    │
    ├── config/
    │   └── config.yaml          # Configuration file (paths, logging)
    │
    ├── data/
    │   ├── raw/
    │   │   └── sales_data.csv   # Input raw data
    │   └── processed/
    │       └── sales_processed_<timestamp>.csv
    │
    ├── logs/
    │   └── etl.log              # Centralized ETL logs
    │
    ├── src/
    │   ├── __init__.py          # Marks src as a Python package
    │   ├── utils.py             # Config loading & logging setup
    │   ├── extract.py           # Data extraction & schema validation
    │   ├── transform.py         # Data cleaning & transformations
    │   ├── load.py              # Data loading logic
    │   └── testig.py            # Entry point for pipeline execution
    │
    └── README.md


## ⚙️ Technologies & Libraries Used

| # | Library | Purpose |
|---|--------|---------|
| 1 | `pandas` | Data manipulation and transformation |
| 2 | `yaml` (PyYAML) | Reading configuration files |
| 3 | `logging` | Application-level logging |
| 4 | `pathlib` | OS-independent path handling |
| 5 | `datetime` | Timestamped outputs |
| 6 | Python 3.10+ | Language runtime |

## 🔧 Configuration Management (config/config.yaml):
  All runtime configurations are externalized:
    
    raw_data_path: data/raw/sales_data.csv
    processed_data_path: data/processed
    log_file_path: logs/etl.log

    logging:
      level: INFO


### Why configuration files?:
  
  1. No hardcoded paths
  2. Easy environment changes
  3. Production best practice

## 🧰 Module Breakdown

### 🔹 `utils.py` – Shared Utilities

**Purpose**
- Load configuration from YAML
- Setup centralized logging
- Resolve project root dynamically

**Key Functions**

- **`load_config()`**
  - Reads `config.yaml`
  - Returns configuration as a Python dictionary

- **`setup_logging(log_file_path, level)`**
  - Creates log directory if missing
  - Logs to both file & console
  - Returns a reusable logger instance

📌 *Used by all ETL modules*

---

### 🔹 `extract.py` – Data Extraction

**Purpose**
- Read raw CSV safely
- Normalize malformed CSV structures
- Validate schema before processing

**Key Responsibilities**
- Detect incorrect delimiters
- Fix malformed headers
- Validate required columns
- Log extraction metrics (rows, columns, schema issues)

**Key Libraries Used**
- `pandas.read_csv`
- `pathlib.Path`

---

### 🔹 `transform.py` – Data Transformation

**Purpose**
- Clean and standardize raw data
- Apply business logic transformations

**Transformations Implemented**

| Issue | Fix |
|----|----|
| Missing quantity | Filled with `1` |
| Duplicate `order_id` | Removed |
| String dates | Converted to `datetime` |
| String numbers | Converted to numeric |
| Missing revenue | Derived column |

**Key Concepts Used**
- `pandas.to_numeric`
- `pandas.to_datetime`
- Vectorized operations
- Defensive programming

---

### 🔹 `load.py` – Data Loading

**Purpose**
- Persist processed data safely
- Prevent overwrites
- Support auditability

**Key Features**
- Auto-create output directory
- Timestamped output files
- Final schema validation
- Exception logging

**Example Output**
    sales_processed_20260112_175609.csv


---

### 🔹 `testig.py` – Pipeline Entry Point

**Purpose**
- Orchestrate the ETL pipeline
- Centralized error handling
- Single execution point

**Key Pattern Used**
```python
try:
    extract → transform → load
except Exception:
    log error + fail pipeline
```
📌 This mimics Airflow / Databricks driver behavior

---
## 🪵 Logging Strategy

**Logs written to**
- Console (real-time)
- `logs/etl.log` (persistent)

**Logging Characteristics**
- Uses `logger.exception()` for full stack traces
- Centralized logging setup (configured once per run)

**Sample Log Entry**
``` 2026-01-12 17:56:09 - INFO - Starting data extraction step ```


---

## ❗ Error Handling Strategy

| Scenario | Handling |
|--------|----------|
| Missing file | Logged + raised |
| Schema mismatch | Logged + pipeline stopped |
| Empty DataFrame | Logged + prevented load |
| Permission issues | Logged with stack trace |

📌 Errors are logged at the **entry point**, not swallowed inside individual functions.

---

## 🚀 How to Run the Project

```bash
python src/testig.py
```

**Ensure**
- Python 3.10+
- Required libraries installed
- config.yaml paths are correct

📈 What This Project Demonstrates

✅ Real-world ETL design
✅ Production logging patterns
✅ Config-driven pipelines
✅ Defensive data engineering
✅ GitHub-ready project structure

## 🧭 Next Enhancements (Planned)
- Incremental load logic
- PostgreSQL & MS SQL loads
- Pytest unit tests
- Data quality checks
- Airflow / ADF orchestration
- Databricks PySpark migration
