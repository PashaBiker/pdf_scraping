import pandas as pd
import time
from openbb_terminal.sdk import openbb
start_time = time.time()

# List of fund IDs
data = [
    {
        "LegalName": "1OAK Multi Asset 80 UCITS Fund A GBP Acc",
        "SecId": "F000015O6T",
        "PriceCurrency": "GBP",
        "TenforeId": "IE00BMW4T172",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0095
    },
    {
        "LegalName": "1OAK Multi Asset 80 UCITS Fund B GBP Acc",
        "SecId": "F000015O6W",
        "PriceCurrency": "GBP",
        "TenforeId": "IE00BMW4T404",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.017
    },
    {
        "LegalName": "1OAK Multi Asset 80 UCITS Fund B USD Hedged Acc",
        "SecId": "F000015O6X",
        "PriceCurrency": "USD",
        "TenforeId": "IE00BMW4T511",
        "CategoryName": "USD Aggressive Allocation",
        "OngoingCostActual": 0.017
    },
    {
        "LegalName": "1OAK Multi Asset 80 UCITS Fund D2 GBP Inc",
        "SecId": "F000015O6Z",
        "PriceCurrency": "GBP",
        "TenforeId": "IE00BMW4T735",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.017
    },
    {
        "LegalName": "1OAK Multi Asset 80 UCITS Fund D2 USD Inc",
        "SecId": "F000015TPE",
        "PriceCurrency": "USD",
        "TenforeId": "IE00BN7JDN44",
        "CategoryName": "USD Aggressive Allocation",
        "OngoingCostActual": 0.017
    },
    {
        "LegalName": "20UGS (UCITS) Funds Diversified Opportunity A CHF Acc",
        "SecId": "F00001D90K",
        "PriceCurrency": "CHF",
        "TenforeId": "LU1162455403",
        "CategoryName": "Other Allocation"
    },]


# Initialize an empty DataFrame to store all historical data
all_historical_data = pd.DataFrame()

# Iterate over each fund ID
for fund_id in data:
    try:
        # Load the fund data
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
all_historical_data.to_excel("test_100_old.xlsx")

end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")
