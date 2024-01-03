import json
import threading
import pandas as pd
import time
from openbb_terminal.sdk import openbb
start_time = time.time()
import sqlite3
import concurrent.futures

# List of fund IDs
with open('tests/data.json') as f:
   data = json.load(f)
# Initialize an empty DataFrame to store all historical data
# Initialize a list to store dataframes
dataframes = []
data_lock = threading.Lock()

def fetch_data(item):
    try:
        fund_id = item["SecId"]
        f = openbb.funds.load(fund_id, 'gb')
        historical_data = openbb.funds.historical(f, "1980-11-10", "2023-11-20")
        historical_data['Fund ID'] = fund_id
        return historical_data
    except Exception as e:
        print(f"Error processing {fund_id}: {e}")
        return None

with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
    futures = [executor.submit(fetch_data, item) for item in data]
    for future in concurrent.futures.as_completed(futures):
        result = future.result()
        if result is not None:
            with data_lock:
                dataframes.append(result)

# Concatenate all dataframes
all_historical_data = pd.concat(dataframes)

end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")

# Save to Parquet and Database
all_historical_data.to_parquet("test_500_old.parquet")

conn = sqlite3.connect("500funds_data.db")
all_historical_data.to_sql("funds_historical_data", conn, if_exists='replace', index=False)
conn.close()

'''

Error: HTTPSConnectionPool(host='www.us-api.morningstar.com', port=443): Max retries exceeded with url: /QS-markets/chartservice/v2/timeseries?query=F00000U7BE:nav,totalReturn&frequency=d&startDate=1980-11-10&endDate=2023-11-20&trackMarketData=3.6.3&instid=MSERP (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection object at 0x00000168EFAE6740>, 'Connection to 
www.us-api.morningstar.com timed out. (connect timeout=None)'))

Error: HTTPSConnectionPool(host='www.morningstar.com', port=443): Max retries exceeded with url: /funds/xnas/afozx/chart (Caused by ConnectTimeoutError(<urllib3.connection.HTTPSConnection 
object at 0x000001690ABEFE50>, 'Connection to www.morningstar.com timed out. (connect timeout=None)'))

'''