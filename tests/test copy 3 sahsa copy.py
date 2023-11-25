import threading
import pandas as pd
import time
from openbb_terminal.sdk import openbb
start_time = time.time()
import sqlite3
import concurrent.futures

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
    },
    {
        "LegalName": "20UGS (UCITS) Funds Diversified Opportunity A EUR Acc",
        "SecId": "F00001D90J",
        "PriceCurrency": "EUR",
        "TenforeId": "LU1162455072",
        "CategoryName": "Other Allocation"
    },
    {
        "LegalName": "20UGS (UCITS) Funds Pinestone Global Equity Class A CHF accummulation",
        "SecId": "F00000YC74",
        "PriceCurrency": "CHF",
        "TenforeId": "LU1389832426",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.0144
    },
    {
        "LegalName": "20UGS (UCITS) Funds Pinestone Global Equity Class A EUR accummulation",
        "SecId": "F00000YC76",
        "PriceCurrency": "EUR",
        "TenforeId": "LU1389831881",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.014499999999999999
    },
    {
        "LegalName": "20UGS (UCITS) Funds Pinestone Global Equity Class A GBP accummulation",
        "SecId": "F00000YC72",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1389832186",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.014199999999999999
    },
    {
        "LegalName": "20UGS (UCITS) Funds Pinestone Global Equity Class A USD accummulation",
        "SecId": "F00000YC70",
        "PriceCurrency": "USD",
        "TenforeId": "LU1389831535",
        "CategoryName": "Global Large-Cap Growth Equity",
        "OngoingCostActual": 0.014499999999999999
    },
    {
        "LegalName": "20UGS (UCITS) Funds Pinestone Global Equity Class P EUR distribution",
        "SecId": "F00000YC77",
        "PriceCurrency": "EUR",
        "TenforeId": "LU1389831964",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.0226
    },
    {
        "LegalName": "20UGS (UCITS) Funds Pinestone Global Equity Class P GBP distribution",
        "SecId": "F00000YC73",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1389832269",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.023
    },
    {
        "LegalName": "20UGS (UCITS) Funds Pinestone Global Equity Class P USD distribution",
        "SecId": "F00000YC71",
        "PriceCurrency": "USD",
        "TenforeId": "LU1389831618",
        "CategoryName": "Global Large-Cap Growth Equity",
        "OngoingCostActual": 0.022000000000000002
    },
    {
        "LegalName": "20UGS (UCITS) Funds TCW Unconstrained Plus Bond Strategy A USD",
        "SecId": "F00000UIMR",
        "PriceCurrency": "USD",
        "TenforeId": "LU1002972054",
        "CategoryName": "USD Flexible Bond",
        "OngoingCostActual": 0.0131
    },
    {
        "LegalName": "24 Capital Management SICAV plc - 24 Global Currency Fund Share Class A USD Accumulation",
        "SecId": "F000013BGI",
        "PriceCurrency": "USD",
        "TenforeId": "MT7000022612",
        "CategoryName": "Currency"
    },
    {
        "LegalName": "2Xideas UCITS - Global Mid Cap Library Fund S GBP",
        "SecId": "F0000144J5",
        "PriceCurrency": "GBP",
        "TenforeId": "LU2001262620",
        "CategoryName": "Global Flex-Cap Equity",
        "OngoingCostActual": 0.01
    },
    {
        "LegalName": "2Xideas UCITS - Global Mid Cap Library Fund S USD",
        "SecId": "F000010G52",
        "PriceCurrency": "USD",
        "TenforeId": "LU1785301513",
        "CategoryName": "Global Flex-Cap Equity",
        "OngoingCostActual": 0.01
    },
    {
        "LegalName": "36ONE Global Equity Fund PC Class A USD Accumulation",
        "SecId": "F000013GO6",
        "PriceCurrency": "USD",
        "TenforeId": "GG00BF42WV17",
        "CategoryName": "Global Large-Cap Growth Equity"
    },
    {
        "LegalName": "7IM AAP Adventurous Fund A Acc",
        "SecId": "F000001EZU",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2507",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0125
    },
    {
        "LegalName": "7IM AAP Adventurous Fund A Inc",
        "SecId": "F000001EZV",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2382",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0125
    },
    {
        "LegalName": "7IM AAP Adventurous Fund C Acc",
        "SecId": "F000001EZR",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2C75",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0075
    },
    {
        "LegalName": "7IM AAP Adventurous Fund C Inc",
        "SecId": "F000001EZT",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2B68",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0075
    },
    {
        "LegalName": "7IM AAP Adventurous Fund D Acc",
        "SecId": "F00000216C",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B39LHH08",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0165
    },
    {
        "LegalName": "7IM AAP Adventurous Fund D Inc",
        "SecId": "F00000216B",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B39LMN11",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0165
    },
    {
        "LegalName": "7IM AAP Adventurous Fund S Acc",
        "SecId": "F00000SSTS",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPX070",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.005
    },
    {
        "LegalName": "7IM AAP Adventurous Fund S Inc",
        "SecId": "F00000SSTT",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPX187",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.005
    },
    {
        "LegalName": "7IM AAP Adventurous Fund X Acc",
        "SecId": "F00001GK1V",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMV2BB68",
        "CategoryName": "GBP Allocation 80%+ Equity"
    },
    {
        "LegalName": "7IM AAP Balanced Fund A Acc",
        "SecId": "F000001F00",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2R29",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.011699999999999999
    },
    {
        "LegalName": "7IM AAP Balanced Fund A Inc",
        "SecId": "F000001F01",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2N80",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.011699999999999999
    },
    {
        "LegalName": "7IM AAP Balanced Fund C Acc",
        "SecId": "F000001EZX",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB3794",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0067
    },
    {
        "LegalName": "7IM AAP Balanced Fund C Inc",
        "SecId": "F000001EZZ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2V64",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0067
    },
    {
        "LegalName": "7IM AAP Balanced Fund D Acc",
        "SecId": "F00000216I",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B39L9C92",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.015700000000000002
    },
    {
        "LegalName": "7IM AAP Balanced Fund D Inc",
        "SecId": "F00000216H",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B39L9J61",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.015700000000000002
    },
    {
        "LegalName": "7IM AAP Balanced Fund S Acc",
        "SecId": "F00000SSTO",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWW23",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0042
    },
    {
        "LegalName": "7IM AAP Balanced Fund S Inc",
        "SecId": "F00000SSTP",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWX30",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0042
    },
    {
        "LegalName": "7IM AAP Income Fund A Inc",
        "SecId": "F0GBR04ERL",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033953612",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.018600000000000002
    },
    {
        "LegalName": "7IM AAP Income Fund B Acc",
        "SecId": "F0GBR04FTF",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033953836",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0171
    },
    {
        "LegalName": "7IM AAP Income Fund C Acc",
        "SecId": "F0GBR06OFT",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033954024",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0086
    },
    {
        "LegalName": "7IM AAP Income Fund C Inc",
        "SecId": "F0GBR06OFS",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033953943",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0086
    },
    {
        "LegalName": "7IM AAP Income Fund D Acc",
        "SecId": "F0GBR05WOO",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438L11",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0191
    },
    {
        "LegalName": "7IM AAP Income Fund D Inc",
        "SecId": "F0GBR05WON",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438H74",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0191
    },
    {
        "LegalName": "7IM AAP Income Fund S Acc",
        "SecId": "F00000SSTA",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWF57",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0060999999999999995
    },
    {
        "LegalName": "7IM AAP Income Fund S Inc",
        "SecId": "F00000SSTB",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWG64",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0060999999999999995
    },
    {
        "LegalName": "7IM AAP Moderately Adventurous Fund A Acc",
        "SecId": "F000001F04",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2J45",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.011899999999999999
    },
    {
        "LegalName": "7IM AAP Moderately Adventurous Fund A Inc",
        "SecId": "F000001F05",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2F07",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.011899999999999999
    },
    {
        "LegalName": "7IM AAP Moderately Adventurous Fund C Acc",
        "SecId": "F000001F02",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2M73",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0069
    },
    {
        "LegalName": "7IM AAP Moderately Adventurous Fund C Inc",
        "SecId": "F000001F03",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2K59",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0069
    },
    {
        "LegalName": "7IM AAP Moderately Adventurous Fund D Acc",
        "SecId": "F00000216F",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B39LB902",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0159
    },
    {
        "LegalName": "7IM AAP Moderately Adventurous Fund D Inc",
        "SecId": "F00000216G",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B39LH586",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0159
    },
    {
        "LegalName": "7IM AAP Moderately Adventurous Fund S Acc",
        "SecId": "F00000SSTQ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWY47",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0044
    },
    {
        "LegalName": "7IM AAP Moderately Adventurous Fund S Inc",
        "SecId": "F00000SSTR",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWZ53",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0044
    },
    {
        "LegalName": "7IM AAP Moderately Cautious Fund A Acc",
        "SecId": "F000001EZS",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB1X14",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.011899999999999999
    },
    {
        "LegalName": "7IM AAP Moderately Cautious Fund A Inc",
        "SecId": "F000001EZQ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB1T77",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.011899999999999999
    },
    {
        "LegalName": "7IM AAP Moderately Cautious Fund C Acc",
        "SecId": "F000001EZW",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2168",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0069
    },
    {
        "LegalName": "7IM AAP Moderately Cautious Fund C Inc",
        "SecId": "F000001EZY",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B2PB2051",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0069
    },
    {
        "LegalName": "7IM AAP Moderately Cautious Fund D Acc",
        "SecId": "F00000216D",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B39LMP35",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0159
    },
    {
        "LegalName": "7IM AAP Moderately Cautious Fund D Inc",
        "SecId": "F00000216E",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B39LMT72",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0159
    },
    {
        "LegalName": "7IM AAP Moderately Cautious Fund S Acc",
        "SecId": "F00000SSTM",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWT93",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0044
    },
    {
        "LegalName": "7IM AAP Moderately Cautious Fund S Inc",
        "SecId": "F00000SSTN",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWV16",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0044
    },
    {
        "LegalName": "7IM Adventurous Fund A Acc",
        "SecId": "F0GBR04FR7",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033957142",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0197
    },
    {
        "LegalName": "7IM Adventurous Fund B Acc",
        "SecId": "F0GBR04FTB",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033957472",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0172
    },
    {
        "LegalName": "7IM Adventurous Fund C Acc",
        "SecId": "F0GBR05VCR",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033958009",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0147
    },
    {
        "LegalName": "7IM Adventurous Fund C Inc",
        "SecId": "F0GBR05VCQ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033957704",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0147
    },
    {
        "LegalName": "7IM Adventurous Fund D Acc",
        "SecId": "F0GBR05VLI",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438440",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0197
    },
    {
        "LegalName": "7IM Adventurous Fund S Acc",
        "SecId": "F00000SSTI",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWP55",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.012199999999999999
    },
    {
        "LegalName": "7IM Adventurous Fund S Inc",
        "SecId": "F00000SSTJ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWQ62",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.012199999999999999
    },
    {
        "LegalName": "7IM Balanced Fund A Acc",
        "SecId": "F0GBR04FR9",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033958884",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0181
    },
    {
        "LegalName": "7IM Balanced Fund B Acc",
        "SecId": "F0GBR04FTD",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033959072",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.015600000000000001
    },
    {
        "LegalName": "7IM Balanced Fund C Acc",
        "SecId": "F0GBR05VLG",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033959742",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0131
    },
    {
        "LegalName": "7IM Balanced Fund C Inc",
        "SecId": "F0GBR05VLH",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033959296",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0131
    },
    {
        "LegalName": "7IM Balanced Fund D Acc",
        "SecId": "F0GBR05WOT",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438F50",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0181
    },
    {
        "LegalName": "7IM Balanced Fund D Inc",
        "SecId": "F0GBR05WOS",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438B13",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0181
    },
    {
        "LegalName": "7IM Balanced Fund S Acc",
        "SecId": "F00000SSTE",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWK01",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0106
    },
    {
        "LegalName": "7IM Balanced Fund S Inc",
        "SecId": "F00000SSTF",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWL18",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0106
    },
    {
        "LegalName": "7IM Balanced Fund X Acc",
        "SecId": "F000015SUD",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMHZQ140",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0066
    },
    {
        "LegalName": "7IM Balanced Fund X Inc",
        "SecId": "F000015SUC",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMHZQ256",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0066
    },
    {
        "LegalName": "7IM Cautious Fund C Acc",
        "SecId": "F00000VDJS",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BVYPGT82",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.008
    },
    {
        "LegalName": "7IM Cautious Fund C Inc",
        "SecId": "F00000VDJR",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BVYPGS75",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.008
    },
    {
        "LegalName": "7IM Cautious Fund S Acc",
        "SecId": "F00000VDJU",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BVYPGW12",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0055000000000000005
    },
    {
        "LegalName": "7IM Cautious Fund S Inc",
        "SecId": "F00000VDJT",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BVYPGV05",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0055000000000000005
    },
    {
        "LegalName": "7IM Investment Funds ICVC - 7IM Absolute Return Portfolio B Acc",
        "SecId": "F00000ZXXO",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BF7MD936",
        "CategoryName": "Other",
        "OngoingCostActual": 0.0008
    },
    {
        "LegalName": "7IM Investment Funds ICVC - 7IM Absolute Return Portfolio Net Acc",
        "SecId": "F00000LZ4J",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B4QPB031",
        "CategoryName": "Other",
        "OngoingCostActual": 0.0008
    },
    {
        "LegalName": "7IM Investment Funds ICVC - 7IM Income Portfolio Net Inc",
        "SecId": "F0GBR04VO4",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033879049",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0
    },
    {
        "LegalName": "7IM Investment Funds ICVC - 7IM T Income Portfolio Gross Inc",
        "SecId": "F00000W2NS",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B9L4H242",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0015
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund A Acc",
        "SecId": "F0GBR04FRD",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033955435",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0187
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund B Acc",
        "SecId": "F0GBR04FTL",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033955989",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.016200000000000003
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund C Acc",
        "SecId": "F0GBR05VLK",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033956516",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0137
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund C Inc",
        "SecId": "F0GBR05WOU",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033956391",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0137
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund D Acc",
        "SecId": "F0GBR05WOW",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438P58",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0187
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund D Inc",
        "SecId": "F0GBR05WOV",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438N35",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0187
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund S Acc",
        "SecId": "F00000SSTG",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWM25",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.011200000000000002
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund S Inc",
        "SecId": "F00000SSTH",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWN32",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.011200000000000002
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund X Acc",
        "SecId": "F000015SUF",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMHZQ363",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0072
    },
    {
        "LegalName": "7IM Moderately Adventurous Fund X Inc",
        "SecId": "F000015SUE",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMHZQ470",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0072
    },
    {
        "LegalName": "7IM Moderately Cautious Fund A Acc",
        "SecId": "F0GBR04FRF",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033952978",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.018600000000000002
    },
    {
        "LegalName": "7IM Moderately Cautious Fund B Acc",
        "SecId": "F0GBR04FTN",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033953166",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0161
    },
    {
        "LegalName": "7IM Moderately Cautious Fund C Acc",
        "SecId": "F0GBR05WOQ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033953497",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.013600000000000001
    },
    {
        "LegalName": "7IM Moderately Cautious Fund C Inc",
        "SecId": "F0GBR05WOP",
        "PriceCurrency": "GBP",
        "TenforeId": "GB0033953273",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.013600000000000001
    },
    {
        "LegalName": "7IM Moderately Cautious Fund D Acc",
        "SecId": "F0GBR05VLO",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438T96",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.018600000000000002
    },
    {
        "LegalName": "7IM Moderately Cautious Fund D Inc",
        "SecId": "F0GBR05WOR",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B0438Q65",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.018600000000000002
    },
    {
        "LegalName": "7IM Moderately Cautious Fund S Acc",
        "SecId": "F00000SSTC",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWH71",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0111
    },
    {
        "LegalName": "7IM Moderately Cautious Fund S Inc",
        "SecId": "F00000SSTD",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWJ95",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0111
    },
    {
        "LegalName": "7IM Moderately Cautious Fund X Acc",
        "SecId": "F000015SUB",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMHZQ033",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0070999999999999995
    },
    {
        "LegalName": "7IM Pathbuilder 1 Fund C GBP Acc",
        "SecId": "F00001550G",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMDPBQ86",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0034999999999999996
    },
    {
        "LegalName": "7IM Pathbuilder 1 Fund C GBP Inc",
        "SecId": "F00001550F",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMDPC090",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0034999999999999996
    },
    {
        "LegalName": "7IM Pathbuilder 2 Fund C GBP Acc",
        "SecId": "F00001550K",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMDPC322",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0034999999999999996
    },
    {
        "LegalName": "7IM Pathbuilder 2 Fund C GBP Inc",
        "SecId": "F00001550J",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMDPC439",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0034999999999999996
    },
    {
        "LegalName": "7IM Pathbuilder 3 Fund C GBP Acc",
        "SecId": "F00001550O",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMDPC769",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0034999999999999996
    },
    {
        "LegalName": "7IM Pathbuilder 3 Fund C GBP Inc",
        "SecId": "F00001550N",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMDPC876",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0034999999999999996
    },
    {
        "LegalName": "7IM Pathbuilder 4 Fund C GBP Acc",
        "SecId": "F00001550T",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMDPCC16",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0034000000000000002
    },
    {
        "LegalName": "7IM Pathbuilder 4 Fund C GBP Inc",
        "SecId": "F00001550S",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BMDPCD23",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0034000000000000002
    },
    {
        "LegalName": "7IM Personal Injury Fund C Acc",
        "SecId": "F000005J1Z",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B570T445",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0073
    },
    {
        "LegalName": "7IM Personal Injury Fund C Inc",
        "SecId": "F000005J1Y",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B55W5449",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0073
    },
    {
        "LegalName": "7IM Personal Injury Fund D Acc",
        "SecId": "F000005FOP",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B61K3671",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0163
    },
    {
        "LegalName": "7IM Personal Injury Fund S Acc",
        "SecId": "F00000SSUJ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ7B9N43",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0048
    },
    {
        "LegalName": "7IM Personal Injury Fund S Inc",
        "SecId": "F00000SSUK",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ7B9P66",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0048
    },
    {
        "LegalName": "7IM Real Return Fund C Acc",
        "SecId": "F00000NMM2",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B75MS619",
        "CategoryName": "GBP Flexible Allocation",
        "OngoingCostActual": 0.009399999999999999
    },
    {
        "LegalName": "7IM Real Return Fund D Acc",
        "SecId": "F00000NMM3",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B75MSB62",
        "CategoryName": "GBP Flexible Allocation",
        "OngoingCostActual": 0.0059
    },
    {
        "LegalName": "7IM Real Return Fund S Acc",
        "SecId": "F00000SSUL",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ8S1164",
        "CategoryName": "GBP Flexible Allocation",
        "OngoingCostActual": 0.0084
    },
    {
        "LegalName": "7IM Select Adventurous Fund C GBP Acc",
        "SecId": "F000013PCO",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8L56",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.013600000000000001
    },
    {
        "LegalName": "7IM Select Adventurous Fund C GBP Inc",
        "SecId": "F000013PCN",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8K40",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.013600000000000001
    },
    {
        "LegalName": "7IM Select Adventurous Fund S GBP Acc",
        "SecId": "F000013PCQ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8N70",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0111
    },
    {
        "LegalName": "7IM Select Adventurous Fund S GBP Inc",
        "SecId": "F000013PCP",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8M63",
        "CategoryName": "GBP Allocation 80%+ Equity",
        "OngoingCostActual": 0.0111
    },
    {
        "LegalName": "7IM Select Balanced Fund C GBP Acc",
        "SecId": "F000013PCB",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8B58",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.011699999999999999
    },
    {
        "LegalName": "7IM Select Balanced Fund C GBP Inc",
        "SecId": "F000013PCA",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8934",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.011699999999999999
    },
    {
        "LegalName": "7IM Select Balanced Fund S GBP Acc",
        "SecId": "F000013PCD",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8D72",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0092
    },
    {
        "LegalName": "7IM Select Balanced Fund S GBP Inc",
        "SecId": "F000013PCC",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8C65",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0092
    },
    {
        "LegalName": "7IM Select Moderately Adventurous Fund C GBP Acc",
        "SecId": "F000013PCI",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8G04",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.012199999999999999
    },
    {
        "LegalName": "7IM Select Moderately Adventurous Fund C GBP Inc",
        "SecId": "F000013PCH",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8F96",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.012199999999999999
    },
    {
        "LegalName": "7IM Select Moderately Adventurous Fund S GBP Acc",
        "SecId": "F000013PCK",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8J35",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "7IM Select Moderately Adventurous Fund S GBP Inc",
        "SecId": "F000013PCJ",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8H11",
        "CategoryName": "GBP Allocation 60-80% Equity",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "7IM Select Moderately Cautious Fund C GBP Acc",
        "SecId": "F000013PC5",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8603",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0126
    },
    {
        "LegalName": "7IM Select Moderately Cautious Fund C GBP Inc",
        "SecId": "F000013PC4",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8371",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0126
    },
    {
        "LegalName": "7IM Select Moderately Cautious Fund S GBP Acc",
        "SecId": "F000013PC7",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8827",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0101
    },
    {
        "LegalName": "7IM Select Moderately Cautious Fund S GBP Inc",
        "SecId": "F000013PC6",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJ0C8710",
        "CategoryName": "GBP Allocation 20-40% Equity",
        "OngoingCostActual": 0.0101
    },
    {
        "LegalName": "7IM Sustainable Balance Fund A Acc",
        "SecId": "F0000009K7",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B1LBFW55",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0206
    },
    {
        "LegalName": "7IM Sustainable Balance Fund A Inc",
        "SecId": "F000000664",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B1LBFV49",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0206
    },
    {
        "LegalName": "7IM Sustainable Balance Fund C Acc",
        "SecId": "F0000009K9",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B1LBFZ86",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0131
    },
    {
        "LegalName": "7IM Sustainable Balance Fund C Inc",
        "SecId": "F0000009KA",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00B1LBG003",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0131
    },
    {
        "LegalName": "7IM Sustainable Balance Fund S Acc",
        "SecId": "F00000SSTK",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWR79",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0106
    },
    {
        "LegalName": "7IM Sustainable Balance Fund S Inc",
        "SecId": "F00000SSTL",
        "PriceCurrency": "GBP",
        "TenforeId": "GB00BJBPWS86",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0106
    },
    {
        "LegalName": "AB - All China Equity Portfolio I USD Acc",
        "SecId": "F000010J2O",
        "PriceCurrency": "USD",
        "TenforeId": "LU1808992603",
        "CategoryName": "China Equity",
        "OngoingCostActual": 0.011899999999999999
    },
    {
        "LegalName": "AB - All Market Income Portfolio I USD Acc",
        "SecId": "F00000V558",
        "PriceCurrency": "USD",
        "TenforeId": "LU1127391495",
        "CategoryName": "USD Moderate Allocation",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB - All Market Income Portfolio INN GBP H Inc",
        "SecId": "F000011ARP",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1877326543",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0095
    },
    {
        "LegalName": "AB - All Market Income Portfolio INN USD Inc",
        "SecId": "F000011ARI",
        "PriceCurrency": "USD",
        "TenforeId": "LU1877325735",
        "CategoryName": "USD Moderate Allocation",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB - All Market Income Portfolio S1 GBP H Acc",
        "SecId": "F000011ARB",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1877324688",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0075
    },
    {
        "LegalName": "AB - All Market Income Portfolio S1QG GBP H GInc",
        "SecId": "F000011ARQ",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1877326626",
        "CategoryName": "GBP Allocation 40-60% Equity",
        "OngoingCostActual": 0.0075
    },
    {
        "LegalName": "AB - American Growth Portfolio I Acc",
        "SecId": "F0GBR05XJA",
        "PriceCurrency": "USD",
        "TenforeId": "LU0079475348",
        "CategoryName": "US Large-Cap Growth Equity",
        "OngoingCostActual": 0.0095
    },
    {
        "LegalName": "AB - American Growth Portfolio I GBP Acc",
        "SecId": "F0000146V3",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1877329133",
        "CategoryName": "US Large-Cap Growth Equity",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB - American Growth Portfolio I GBP H Acc",
        "SecId": "F000013ZBT",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1877329059",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.0095
    },
    {
        "LegalName": "AB - American Income Portfolio AT EUR Inc",
        "SecId": "F00001ECZR",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0328307227",
        "CategoryName": "USD Flexible Bond",
        "OngoingCostActual": 0.0132
    },
    {
        "LegalName": "AB - American Income Portfolio AT GBP H Inc",
        "SecId": "F00000NJO8",
        "PriceCurrency": "GBP",
        "TenforeId": "LU0689625878",
        "CategoryName": "Other Bond",
        "OngoingCostActual": 0.0132
    },
    {
        "LegalName": "AB - American Income Portfolio AT Inc",
        "SecId": "F0GBR05XC9",
        "PriceCurrency": "USD",
        "TenforeId": "LU0157308031",
        "CategoryName": "USD Flexible Bond",
        "OngoingCostActual": 0.0132
    },
    {
        "LegalName": "AB - American Income Portfolio I Inc",
        "SecId": "F0GBR04I6A",
        "PriceCurrency": "USD",
        "TenforeId": "LU0079475934",
        "CategoryName": "USD Flexible Bond",
        "OngoingCostActual": 0.0077
    },
    {
        "LegalName": "AB - American Income Portfolio I2 EUR H Acc",
        "SecId": "F00000JUWU",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0539800077",
        "CategoryName": "Other Bond",
        "OngoingCostActual": 0.0077
    },
    {
        "LegalName": "AB American Income Portfolio I2 USD",
        "SecId": "FOGBR05KDV",
        "PriceCurrency": "USD",
        "TenforeId": "LU0249549436",
        "CategoryName": "USD Flexible Bond",
        "OngoingCostActual": 0.0077
    },
    {
        "LegalName": "AB - American Income Portfolio IT EUR H Inc",
        "SecId": "F00000WPX6",
        "PriceCurrency": "EUR",
        "TenforeId": "LU1309713698",
        "CategoryName": "Other Bond",
        "OngoingCostActual": 0.0076
    },
    {
        "LegalName": "AB - American Income Portfolio IT GBP H Inc",
        "SecId": "F00000WPX7",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1309713771",
        "CategoryName": "Other Bond",
        "OngoingCostActual": 0.0076
    },
    {
        "LegalName": "AB American Income Portfolio WT GBP H Inc",
        "SecId": "F000013WDQ",
        "PriceCurrency": "GBP",
        "TenforeId": "LU2000519475",
        "CategoryName": "Other Bond",
        "OngoingCostActual": 0.006
    },
    {
        "LegalName": "AB - Asia Ex-Japan Equity Portfolio I Acc",
        "SecId": "F000005MTH",
        "PriceCurrency": "USD",
        "TenforeId": "LU0469271091",
        "CategoryName": "Asia ex-Japan Equity",
        "OngoingCostActual": 0.012199999999999999
    },
    {
        "LegalName": "AB - Asia Ex-Japan Equity Portfolio I GBP Acc",
        "SecId": "F00000XJCR",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1366339452",
        "CategoryName": "Asia ex-Japan Equity",
        "OngoingCostActual": 0.0121
    },
    {
        "LegalName": "AB - Asia Income Opportunities Portfolio I2 USD Acc",
        "SecId": "F00000XVJG",
        "PriceCurrency": "USD",
        "TenforeId": "LU1467538093",
        "CategoryName": "Asia Bond",
        "OngoingCostActual": 0.0079
    },
    {
        "LegalName": "AB - Concentrated Global Equity Portfolio I EUR Acc",
        "SecId": "F00001402Q",
        "PriceCurrency": "EUR",
        "TenforeId": "LU1877329307",
        "CategoryName": "Global Large-Cap Growth Equity",
        "OngoingCostActual": 0.009899999999999999
    },
    {
        "LegalName": "AB - Concentrated Global Equity Portfolio I GBP Acc",
        "SecId": "F0000144KF",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1877329216",
        "CategoryName": "Global Large-Cap Growth Equity",
        "OngoingCostActual": 0.009899999999999999
    },
    {
        "LegalName": "AB - Concentrated Global Equity Portfolio I GBP H Acc",
        "SecId": "F00000SJ2K",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1011998512",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.009899999999999999
    },
    {
        "LegalName": "AB - Concentrated Global Equity Portfolio I USD Acc",
        "SecId": "F00000SE91",
        "PriceCurrency": "USD",
        "TenforeId": "LU1011997464",
        "CategoryName": "Global Large-Cap Growth Equity",
        "OngoingCostActual": 0.009899999999999999
    },
    {
        "LegalName": "AB - Concentrated Global Equity Portfolio S GBP Acc",
        "SecId": "F00000WCGS",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1174051927",
        "CategoryName": "Global Large-Cap Growth Equity",
        "OngoingCostActual": 0.0011
    },
    {
        "LegalName": "AB - Concentrated Global Equity Portfolio S USD Acc",
        "SecId": "F00000SE93",
        "PriceCurrency": "USD",
        "CategoryName": "Global Large-Cap Growth Equity",
        "OngoingCostActual": 0.0011,
        "TenforeId": ""
    },
    {
        "LegalName": "AB - Concentrated US Equity Portfolio I EUR H Acc",
        "SecId": "F00000SJ2X",
        "PriceCurrency": "EUR",
        "TenforeId": "LU1011999833",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.009399999999999999
    },
    {
        "LegalName": "AB - Concentrated US Equity Portfolio I GBP Acc",
        "SecId": "F0000144QI",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1934454114",
        "CategoryName": "US Large-Cap Growth Equity",
        "OngoingCostActual": 0.009399999999999999
    },
    {
        "LegalName": "AB - Concentrated US Equity Portfolio I GBP H Acc",
        "SecId": "F00000SJ2V",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1011999759",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.009399999999999999
    },
    {
        "LegalName": "AB - Concentrated US Equity Portfolio I USD Acc",
        "SecId": "F00000SE98",
        "PriceCurrency": "USD",
        "TenforeId": "LU1011999676",
        "CategoryName": "US Large-Cap Growth Equity",
        "OngoingCostActual": 0.009399999999999999
    },
    {
        "LegalName": "AB - Concentrated US Equity Portfolio S1 GBP H Acc",
        "SecId": "F00000VP8A",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1207086866",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.008199999999999999
    },
    {
        "LegalName": "AB - Dynamic Diversified Portfolio I EUR H Acc",
        "SecId": "F00000MLEI",
        "PriceCurrency": "EUR",
        "CategoryName": "EUR Flexible Allocation - Global",
        "OngoingCostActual": 0.0125,
        "TenforeId": ""
    },
    {
        "LegalName": "AB - Dynamic Diversified Portfolio S1 EUR H Acc",
        "SecId": "F00000OWNT",
        "PriceCurrency": "EUR",
        "CategoryName": "EUR Flexible Allocation - Global",
        "OngoingCostActual": 0.008,
        "TenforeId": ""
    },
    {
        "LegalName": "AB - Emerging Market Corporate Debt Portfolio I2 USD Acc",
        "SecId": "F00000NS6F",
        "PriceCurrency": "USD",
        "TenforeId": "LU0736563387",
        "CategoryName": "Global Emerging Markets Corporate Bond",
        "OngoingCostActual": 0.0108
    },
    {
        "LegalName": "AB - Emerging Market Local Currency Debt Portfolio I2 USD Acc",
        "SecId": "F00000NS69",
        "PriceCurrency": "USD",
        "TenforeId": "LU0736562066",
        "CategoryName": "Global Emerging Markets Bond - Local Currency",
        "OngoingCostActual": 0.012
    },
    {
        "LegalName": "AB - Emerging Markets Growth Portfolio I Acc",
        "SecId": "F0GBR04TKL",
        "PriceCurrency": "USD",
        "TenforeId": "LU0079455316",
        "CategoryName": "Global Emerging Markets Equity",
        "OngoingCostActual": 0.012199999999999999
    },
    {
        "LegalName": "AB - Emerging Markets Low Volatility Equity Portfolio F EUR H Acc",
        "SecId": "F00000ZW78",
        "PriceCurrency": "EUR",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.0053,
        "TenforeId": ""
    },
    {
        "LegalName": "AB - Emerging Markets Low Volatility Equity Portfolio F USD Acc",
        "SecId": "F00000ZW76",
        "PriceCurrency": "USD",
        "TenforeId": "LU1675840554",
        "CategoryName": "Global Emerging Markets Equity",
        "OngoingCostActual": 0.005600000000000001
    },
    {
        "LegalName": "AB - Emerging Markets Low Volatility Equity Portfolio I GBP H Acc",
        "SecId": "F00000ZW77",
        "PriceCurrency": "GBP",
        "CategoryName": "Other Equity",
        "OngoingCostActual": 0.0108,
        "TenforeId": ""
    },
    {
        "LegalName": "AB - Emerging Markets Low Volatility Equity Portfolio S USD Acc",
        "SecId": "F00000T1CI",
        "PriceCurrency": "USD",
        "CategoryName": "Global Emerging Markets Equity",
        "OngoingCostActual": 0.0012,
        "TenforeId": ""
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio A Acc",
        "SecId": "F00000MLER",
        "PriceCurrency": "USD",
        "TenforeId": "LU0633140560",
        "CategoryName": "Global Emerging Markets Allocation",
        "OngoingCostActual": 0.0177
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio A AUD H Acc",
        "SecId": "F00000QAHW",
        "PriceCurrency": "AUD",
        "TenforeId": "LU0683595465",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0178
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio A CAD H Acc",
        "SecId": "F00000QAHX",
        "PriceCurrency": "CAD",
        "TenforeId": "LU0683595549",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0177
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio A CHF H Acc",
        "SecId": "F00000MR85",
        "PriceCurrency": "CHF",
        "TenforeId": "LU0633142004",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0177
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio A EUR Acc",
        "SecId": "F00001ED1H",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0633140644",
        "CategoryName": "Global Emerging Markets Allocation",
        "OngoingCostActual": 0.0177
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio A EUR H Acc",
        "SecId": "F00000MLEM",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0633142186",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0177
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio A GBP H Acc",
        "SecId": "F00000MLES",
        "PriceCurrency": "GBP",
        "TenforeId": "LU0633142269",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0177
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio AD AUD H Inc",
        "SecId": "F00000PQ4E",
        "PriceCurrency": "AUD",
        "TenforeId": "LU0683595895",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0178
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio AD CAD H Inc",
        "SecId": "F00000PQ4G",
        "PriceCurrency": "CAD",
        "TenforeId": "LU0683596273",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0177
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio AD EUR H Inc",
        "SecId": "F00000PQ4I",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0683596356",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0178
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio AD GBP H Inc",
        "SecId": "F00000PQ4K",
        "PriceCurrency": "GBP",
        "TenforeId": "LU0683596430",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0177
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio I Acc",
        "SecId": "F00000MLEN",
        "PriceCurrency": "USD",
        "TenforeId": "LU0633141378",
        "CategoryName": "Global Emerging Markets Allocation",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio I CHF H Acc",
        "SecId": "F00000MR81",
        "PriceCurrency": "CHF",
        "TenforeId": "LU0633142343",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0096
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio I EUR Acc",
        "SecId": "F00001ED1I",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0633141451",
        "CategoryName": "Global Emerging Markets Allocation",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio I EUR H Acc",
        "SecId": "F00000MLEO",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0633142426",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio I GBP Acc",
        "SecId": "F000014HP3",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1934454205",
        "CategoryName": "Global Emerging Markets Allocation",
        "OngoingCostActual": 0.009399999999999999
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio I GBP H Acc",
        "SecId": "F00000MLEU",
        "PriceCurrency": "GBP",
        "TenforeId": "LU0633142699",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0096
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio ID GBP Inc",
        "SecId": "F00000ZSRR",
        "PriceCurrency": "GBP",
        "TenforeId": "LU1514172565",
        "CategoryName": "Other Allocation",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB - Emerging Markets Multi-Asset Portfolio ID USD Inc",
        "SecId": "F00000OKUH",
        "PriceCurrency": "USD",
        "TenforeId": "LU0633141535",
        "CategoryName": "Global Emerging Markets Allocation",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB - European Income Portfolio A2 Acc",
        "SecId": "F0GBR04TJT",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0095024591",
        "CategoryName": "EUR Flexible Bond",
        "OngoingCostActual": 0.013500000000000002
    },
    {
        "LegalName": "AB - European Income Portfolio AT USD H Inc",
        "SecId": "F00000JUX3",
        "PriceCurrency": "USD",
        "TenforeId": "LU0539802446",
        "CategoryName": "Other Bond",
        "OngoingCostActual": 0.0134
    },
    {
        "LegalName": "AB - Eurozone Equity Portfolio I EUR Acc",
        "SecId": "F00000JUYT",
        "PriceCurrency": "EUR",
        "TenforeId": "LU0528103707",
        "CategoryName": "Eurozone Large-Cap Equity",
        "OngoingCostActual": 0.0101
    },
    {
        "LegalName": "AB FCP I - Global High Yield Portfolio W EUR",
        "SecId": "F00001AH63",
        "PriceCurrency": "EUR",
        "TenforeId": "LU2069290737",
        "CategoryName": "Global High Yield Bond",
        "OngoingCostActual": 0.009399999999999999
    },
    {
        "LegalName": "AB FCP I - Global High Yield Portfolio W USD",
        "SecId": "F000014BZD",
        "PriceCurrency": "USD",
        "TenforeId": "LU2048609395",
        "CategoryName": "Global High Yield Bond",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB FCP I - Global High Yield Portfolio W2 EUR H",
        "SecId": "F000014BZE",
        "PriceCurrency": "EUR",
        "TenforeId": "LU2048609478",
        "CategoryName": "Global High Yield Bond - EUR Hedged",
        "OngoingCostActual": 0.0097
    },
    {
        "LegalName": "AB FCP I - Global High Yield Portfolio WT GBP H",
        "SecId": "F000014BZG",
        "PriceCurrency": "GBP",
        "TenforeId": "LU2048609635",
        "CategoryName": "Global High Yield Bond - GBP Hedged",
        "OngoingCostActual": 0.0097
    },
    ]
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

with concurrent.futures.ThreadPoolExecutor(max_workers=200) as executor:
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
all_historical_data.to_parquet("test_100_old.parquet")

conn = sqlite3.connect("funds_data.db")
all_historical_data.to_sql("funds_historical_data", conn, if_exists='replace', index=False)
conn.close()