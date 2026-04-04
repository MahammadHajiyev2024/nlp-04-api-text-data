"""
stage02_validate_case.py
(EDIT YOUR COPY OF THIS FILE)

Source: raw JSON object
Sink: validated JSON object

Purpose

  Inspect JSON structure and validate that the data is usable.

Analytical Questions

- What is the top-level structure of the JSON data?
- What keys are present in each record?
- What data types are associated with each field?
- Does the data meet expectations for transformation?

Notes

Following our process, do NOT edit this _case file directly,
keep it as a working example.

In your custom project, copy this _case.py file and
append with _yourname.py instead.

Then edit your copied Python file to:
- inspect the JSON structure for your API,
- validate required keys and types,
- confirm the data is usable for your analysis.
"""

# ============================================================
# Section 1. Setup and Imports
# ============================================================

import logging
from typing import Any

# ============================================================
# Section 2. Define Run Validate Function
# ============================================================


def run_validate(json_data: Any, LOG: logging.Logger) -> list[dict]:
    """Inspect and validate JSON structure.

    Args:
        json_data (Any): The raw JSON data from the Extract stage.
        LOG (logging.Logger): The logger instance.

    Returns:
        list[dict]: The validated JSON data.
    """
    LOG.info("========================")
    LOG.info("STAGE 02: VALIDATE starting...")
    LOG.info("========================")

    # ============================================================
    # INSPECT JSON STRUCTURE
    # ============================================================

    LOG.info("JSON STRUCTURE INSPECTION:")
    if isinstance(json_data, list):
        LOG.info("Processing as a standard list of records (Original Case).")
        # Keep your original checks here
        if len(json_data) == 0:
            raise ValueError("Expected at least one record in the list.")
        return json_data

    # --- PATH 2: NEW DICTIONARY LOGIC (For Alpha Vantage) ---
    elif isinstance(json_data, dict):
        LOG.info("Processing as an Alpha Vantage dictionary (Hajiyev Case).")

        # Check for API limits first
        if "Note" in json_data:
            raise ValueError(f"API Limit: {json_data['Note']}")

        # Look for the data key
        data_key = "Weekly Time Series"
        if data_key not in json_data:
            raise ValueError(f"Expected '{data_key}' not found in Dictionary.")

        # Convert the dictionary to a list so it matches the original format
        # This makes life easier for Stage 03!
        time_series = json_data[data_key]
        list_of_records = []
        for date, metrics in time_series.items():
            record = {"date": date}
            record.update(metrics)
            list_of_records.append(record)

        LOG.info(f"Successfully converted dictionary into a list of {len(list_of_records)} records.")
        return list_of_records

    else:
        raise ValueError(f"Unsupported data type: {type(json_data).__name__}")
    # Log the type of the top-level JSON structure.
    # Use the built-in type() function to get the type
    # and built-in variable __name__ to log just the type name.
    LOG.info(f"Top-level type: {type(json_data).__name__}")

