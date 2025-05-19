import csv
from datetime import datetime
import pandas as pd
import re

# Input and output file paths
input_file = '_data/tax_return_data/_reports/2024 Form 1099 B.csv'
output_file = '_data/tax_return_data/2024 olt_tax_return.xlsx'

# Function to validate and format dates
def format_date(date_str):
    if date_str.lower() in ["various", "inherit"]:
        return date_str.capitalize()
    try:
        return datetime.strptime(date_str, "%m/%d/%Y").strftime("%m/%d/%Y")
    except ValueError:
        return ""

# Read the input CSV
with open(input_file, 'r') as infile:
    reader = csv.DictReader(infile)
    rows = list(reader)

# Define the output headers
output_headers = [
    "Description of capital asset",
    "Date acquired",
    "Date sold",
    "Proceeds or Sales Price ($)",
    "Cost or other basis ($)",
    "Code(s)","Adjustments to gain or loss ($)",
    "Accrued market discount ($)",
    "Wash sale loss disallowed ($)",
    "Long Term/Short Term/Ordinary",
    "Collectibles/QOF",
    "Federal Income Tax Withheld ($)",
    "Noncovered Security",
    "Reported to IRS",
    "Loss not allowed based on amount in 1d",
    "Basis Reported to IRS","Bartering",
    "Applicable Checkbox on Form 8949",
    "Whose Capital Assets",
    "Payer Name","Payer TIN","Foreign Address?",
    "Payer Address line 1",
    "Payer Address line 2",
    "Payer City",
    "Payer State",
    "Payer Zip",
    "Payer Country Code",
    "Form Type",
]

# Map input to output
mapped_rows = []
for row in rows:
    mapped_row = {
        "Description of capital asset": re.sub(r'\s+', ' ', row["Description of property (Example 100 sh. XYZ Co.)"].replace("\t", "").strip()),
        "Date acquired": format_date(row["Date acquired"]),
        "Date sold": format_date(row["Date sold or disposed"]),
        "Cost or other basis ($)": row["Cost or other basis"] if row["Cost or other basis"].replace('.', '', 1).isdigit() else "0",
        "Proceeds or Sales Price ($)": row["Proceeds"] if row["Proceeds"].replace('.', '', 1).replace('\'', '', 1).isdigit() else "0",
        "Code(s)": row["Form 8949 Code"],
        "Adjustments to gain or loss ($)": float(row["Wash sale loss disallowed"].replace("$", "")) + float(row["Accrued market discount"].replace("$", "")),  # Adjustments to gain/loss (can be numeric if provided)
        "Accrued market discount ($)": row["Accrued market discount"].replace("$", ""),
        "Wash sale loss disallowed ($)": row["Wash sale loss disallowed"].replace("$", ""),
        "Long Term/Short Term/Ordinary": row["Short-Term gain loss Long-term gain or loss Ordinary"].split()[0].capitalize(),
        "Collectibles/QOF": "Collectibles" if row["Check if proceeds from collectibles QOF"] else "No",
        "Federal Income Tax Withheld ($)": row["Federal income tax withheld"],
        "Noncovered Security": "Yes" if row["Check if noncovered security"] == "Noncovered" else "No",
        "Reported to IRS": row["Reported to IRS: Gross proceeds Net proceeds"].upper() if row["Reported to IRS: Gross proceeds Net proceeds"] else "NONE",
        "Loss not allowed based on amount in 1d": "Yes" if row["Check if loss is not allowed based on amount in 1d"] else "No",
        "Basis Reported to IRS": "Yes" if row["Check if basis reported to IRS"] == "Yes" else "No",
        "Bartering": row["Bartering"].replace("$", ""),
        "Applicable Checkbox on Form 8949": row["Form 8949 Code"],
        "Whose Capital Assets": "P",  # Assuming "P" for Primary; adjust if necessary
        "Payer Name": "",  # Payer Name (if available)
        "Payer TIN": "",  # Payer TIN (if available)
        "Foreign Address?": "No",  # Assuming no Foreign Address
        "Payer Address line 1": "",
        "Payer Address line 2": "",
        "Payer City": "",
        "Payer State": "",
        "Payer Zip": "",
        "Payer Country Code": "",
        "Form Type": "1099B"  # Assuming Form Type as 1099B; adjust if necessary
    }
    #print(mapped_row)
    mapped_rows.append(mapped_row)

# Write the output CSV
'''
with open(output_file, 'w', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=output_headers)
    writer.writeheader()
    writer.writerows(mapped_rows)
'''

# Convert mapped rows to a DataFrame and write to an Excel file
df = pd.DataFrame(mapped_rows, columns=output_headers)
df.to_excel(output_file, index=False)
    
print(f"Formatted CSV data written to {output_file}")