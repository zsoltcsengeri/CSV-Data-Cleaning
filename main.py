'''
Docstring for main2
Create a small Python script that does the following:
1.	Read the provided customers.csv file.
2.	Perform cleansing and transformations:

○	Cleanse the customer name field (e.g., trim whitespace, normalize casing, remove duplicated spaces).
○	Parse date fields consistently and handle missing/invalid values.
○	Add derived fields:
■	days_until_next_control
■	control_status with values: OVERDUE, DUE_SOON, OK

3.	Create an output file with the cleansed data.

'''
import pandas as pd # Import the pandas library for data manipulation and analysis.
from datetime import datetime # Import the datetime class from the datetime module to work with date and time data.
# Read the input CSV file using semicolons as separators.
df = pd.read_csv("customers.csv", sep=";") 


df.columns = (
    df.columns.str.strip().str.lower()
) # Standardize column names by stripping whitespace and converting to lowercase for consistency.



# Function to clean customer names
def clean_customer_name(name):
    if pd.isna(name):
        return name
    name = " ".join(
        str(name).strip().split()
    )  # Remove leading/trailing whitespace and reduce multiple spaces to a single space.
    name = (
        name.title()
    )  # Convert the name to title case (first letter of each word capitalized) for standardization.
    # Fix possessive apostrophe
    name = name.replace("'S", "'s")
    return name 

df["src_customer_name"] = df["src_customer_name"].apply(
    clean_customer_name
)  # Clean `src_customer_name` to standardize customer names.

today = pd.Timestamp(datetime.now().date()) # Get today's date as a pandas Timestamp for date calculations.

# Convert the next-control dates to datetimes; invalid or missing dates become empty.
df["src_date_next_control"] = pd.to_datetime(
    df.get("src_date_next_control"), errors="coerce", dayfirst=False
)

# Calculate days until the next control (missing dates become blank).
df["days_until_next_control"] = (df["src_date_next_control"] - today).dt.days


# Derived field: control_status
# based on days_until_next_control with the following logic:
def control_status(days):
    if pd.isna(days):  # If the days value is missing,
        return "UNKNOWN"  # Return 'UNKNOWN' when we can't tell the control status.
    if days < 0:
        return "OVERDUE"
    if days <= 14:
        return "DUE_SOON"
    return "OK"

# Use `control_status` to set the status from the days-until value.
df["control_status"] = df["days_until_next_control"].apply(control_status) 

# Write the output to a new CSV file,
# ensuring that the index is not included in the output.
df.to_csv("output_customers.csv", index=False)
