# Customer Data Cleansing & Control Status Script

## Overview
This script reads a `customers.csv` file, performs basic data cleansing and transformations, derives control-related fields, and writes the result to a new output file.

The goal is to demonstrate practical data quality handling, safe date parsing, and clear business rule implementation.

---

# Customer Data Cleansing & Control Status Script

## Overview
This script reads `customers.csv`, performs cleansing and transformations, derives control-related fields, and writes the result to `output_customers.csv`.

## How to run

1. Create and activate a virtual environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install pandas
```

3. Place `customers.csv` next to `main.py` and run:

```bash
python main.py
```

The script writes `output_customers.csv` to the same directory.

## Assumptions

- The input file is named `customers.csv` and is semicolon-separated (`;`).
- The script expects a `src_customer_name` column to cleanse customer names.
- The script expects a `src_date_next_control` column for next-control dates.
- Date parsing currently assumes month-first format (MM/DD/YYYY) based on the sample data; invalid or missing dates are coerced to `NaT` and yield `UNKNOWN` for `control_status`.

## Derived fields and business rules

- `days_until_next_control`: integer days from script run date to `src_date_next_control` (NaN for missing dates).
- `control_status`: derived as
	- `OVERDUE` if `days_until_next_control` < 0
	- `DUE_SOON` if 0 <= `days_until_next_control` <= 14
	- `OK` if `days_until_next_control` > 14
	- `UNKNOWN` when `days_until_next_control` is missing

