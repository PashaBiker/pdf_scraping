import pandas as pd
import time
from openbb_terminal.sdk import openbb
start_time = time.time()

# List of fund IDs
fund_ids = ['F00000YC76', 
            'F00000MJSF',
            'F000015O6T',
            'F000015O6W',
            'F000015O6X',
            'F000015O6Z',
            'F000015TPE',
            'F00001D90K',
            'F00001D90J',
            'F00000YC74',
            'F00000YC76',
            'F00000YC72',
            'F00000YC70',
            'F00000YC77',
            'F00000YC73',
            'F00000YC71',
            'F00000UIMR',
            'F000013BGI',
            'F0000144J5',
            'F000010G52',
            'F000013GO6',
            'F000001EZU',
            'F000001EZV',
            'F000001EZR',
            'F000001EZT',
            'F00000216C',
            'F00000216B',
            'F00000SSTS',
            'F00000SSTT',
            'F00001GK1V',
            'F000001F00',
            'F000001F01',
            'F000001EZX',
            'F000001EZZ',
            'F00000216I',
            'F00000216H',
            'F00000SSTO',
            'F00000SSTP',
            'F0GBR04ERL',
            'F0GBR04FTF',
            'F0GBR06OFT',
            'F0GBR06OFS',
            'F0GBR05WOO',
            'F0GBR05WON',
            'F00000SSTA',
            'F00000SSTB',
            'F000001F04',
            'F000001F05',
            'F000001F02',
            'F000001F03',
            'F00000216F',
            'F00000216G',
            'F00000SSTQ',
            'F00000SSTR',
            'F000001EZS',
            'F000001EZQ',
            'F000001EZW',
            'F000001EZY',
            'F00000216D',
            'F00000216E',
            'F00000SSTM',
            'F00000SSTN',
            'F0GBR04FR7',
            'F0GBR04FTB',
            'F0GBR05VCR',
            'F0GBR05VCQ',
            'F0GBR05VLI',
            'F00000SSTI',
            'F00000SSTJ',
            'F0GBR04FR9',
            'F0GBR04FTD',
            'F0GBR05VLG',
            'F0GBR05VLH',
            'F0GBR05WOT',
            'F0GBR05WOS',
            'F00000SSTE',
            'F00000SSTF',
            'F000015SUD',
            'F000015SUC',
            'F00000VDJS',
            'F00000VDJR',
            'F00000VDJU',
            'F00000VDJT',
            'F00000ZXXO',
            'F00000LZ4J',
            'F0GBR04VO4',
            'F00000W2NS',
            'F0GBR04FRD',
            'F0GBR04FTL',
            'F0GBR05VLK',
            'F0GBR05WOU',
            'F0GBR05WOW',
            'F0GBR05WOV',
            'F00000SSTG',
            'F00000SSTH',
            'F000015SUF',
            'F000015SUE',
            'F0GBR04FRF',
            'F0GBR04FTN',
            'F0GBR05WOQ',
            'F0GBR05WOP',
            'F0GBR05VLO',]


# Initialize an empty DataFrame to store all historical data
all_historical_data = pd.DataFrame()

# Iterate over each fund ID
for fund_id in fund_ids:
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
