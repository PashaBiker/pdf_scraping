import threading
import pandas as pd
import time
from openbb_terminal.sdk import openbb
start_time = time.time()
import sqlite3

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
    },]

all_historical_data = pd.DataFrame()
data_lock = threading.Lock()

def fetch_and_append_data(item):
    try:
        fund_id = item["SecId"]
        f = openbb.funds.load(fund_id, 'gb')
        historical_data = openbb.funds.historical(f, "1980-11-10", "2023-11-20")
        historical_data['Fund ID'] = fund_id

        with data_lock:
            global all_historical_data
            all_historical_data = pd.concat([all_historical_data, historical_data])
    except Exception as e:
        print(f"Error processing {fund_id}: {e}")

# Create and start threads
threads = []
for item in data:
    thread = threading.Thread(target=fetch_and_append_data, args=(item,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Save to Excel and Database
all_historical_data.to_excel("test_100_old.xlsx")
conn = sqlite3.connect("funds_data.db")
all_historical_data.to_sql("funds_historical_data", conn, if_exists='replace', index=False)
conn.close()

end_time = time.time()
print(f"Processing time: {end_time - start_time} seconds")