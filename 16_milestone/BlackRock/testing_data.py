data = [{"name": "Fixed Income (FI)", "value": "78.53", "rank": 0, }, {"name": "Equity (EQ)", "value": "20.19", "rank": 1, }, {"name": "Alternatives", "value": "3.02", "rank": 2, }, {"name": "Cash and/or Derivatives", "value": "-1.74", "rank": 3, }, {"name": "North America", "value": "44.90", "rank": 0, }, {"name": "Europe", "value": "40.92", "rank": 1, }, {"name": "Asia Pacific", "value": "8.53", "rank": 2, }, {"name": "World", "value": "3.35", "rank": 3, }, {"name": "Latin America", "value": "1.69", "rank": 4, }, {"name": "Africa", "value": "0.59", "rank": 5, }, {"name": "Other", "value": "0.01", "rank": 6, }, {"name": "United Kingdom", "value": "80.95", "rank": 0, "code": "GB", "color": "#719E32", }, {"name": "Canada", "value": "3.64", "rank": 1, "code": "CA", "color": "#A4D165", }, {"name": "Germany", "value": "3.61", "rank": 2, "code": "DE", "color": "#A4D165", }, {
    "name": "China", "value": "3.11", "rank": 3, "code": "CN", "color": "#A4D165", }, {"name": "Supranational", "value": "2.86", "rank": 4, "code": "SP", "color": "#A4D165", }, {"name": "France", "value": "2.05", "rank": 5, "code": "FR", "color": "#A4D165", }, {"name": "Japan", "value": "1.64", "rank": 6, "code": "JP", "color": "#A4D165", }, {"name": "Australia", "value": "1.56", "rank": 7, "code": "AU", "color": "#A4D165", }, {"name": "Net Derivatives", "value": "-1.06", "rank": 8, "code": "XXX", "color": "#CC0000", }, {"name": "European Union", "value": "-5.45", "rank": 9, "code": "XXX", "color": "#CC0000", }, {"name": "United States", "value": "-5.91", "rank": 10, "code": "US", "color": "#CC0000", }, {"name": "Other", "value": "11.16", "rank": 11, "code": "OTHR", "color": "#8DC63F", }, {"name": "Cash", "value": "1.73", "rank": 12, "code": "CASH_C", "color": "#A4D165", }]
other_counter = 0

for item in data:
    if item["name"] == "Other":
        other_counter += 1
        if other_counter == 1:
            item["name"] = "Other Regions"
        elif other_counter == 2:
            item["name"] = "Other Locations"

print(data)