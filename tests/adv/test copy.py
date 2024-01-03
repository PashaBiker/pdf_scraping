import pandas as pd
import time
from openbb_terminal.sdk import openbb
start_time = time.time()
import sqlite3

# List of fund IDs
data = [
    {
        "LegalName": "1OAK Multi Asset 80 UCITS Fund A GBP Acc",
        "SecId": "f0gbr04s1g",
        "PriceCurrency": "GBP",
        "TenforeId": "IE00BMW4T172",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0095
    },]


# Initialize an empty DataFrame to store all historical data
all_historical_data = pd.DataFrame()

# Iterate over each fund ID
for item in data:
    try:
        # Load the fund data
        fund_id = item["SecId"]
        f = openbb.funds.load(fund_id, 'gb')
        
        # Retrieve historical data for the fund
        historical_data = openbb.funds.historical(f, "1980-11-10", "2023-11-20")
        
        # Add a column to identify the fund
        historical_data['Fund ID'] = fund_id
        
        # Append the historical data of this fund to the all_historical_data DataFrame
        all_historical_data = pd.concat([all_historical_data, historical_data])
    except:
        continue

# Save the concatenated data to an Excel file
all_historical_data.to_excel("f0gbr04s1g.xlsx")
conn = sqlite3.connect("f0gbr04s1g.db")

# Save the data
all_historical_data.to_sql("funds_historical_data", conn, if_exists='replace', index=False)

# Close the connection to the database
conn.close()
end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
