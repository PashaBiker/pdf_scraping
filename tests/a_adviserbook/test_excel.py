import pandas as pd
import json

# Sample JSON data
data = {
    "B3TmDgoqMFz": {
        "firm": {
            "fca_num": "193600",
            "name": "Mansion House Capital",
            "website": "www.mhcapital.co.uk",
            "email": "davidstone@mhcapital.co.uk",
            "linkedin": "company/mansion-house-capital/",
            "advisers": [
                {
                    "title": "mr",
                    "firstname": "David",
                    "surname": "Stone",
                    "phone_number": "02075625870",
                    "email": "davidstone@mhcapital.co.uk",
                    "linkedin": "in/davidstone/",
                },
                {
                    "title": "mrs",
                    "firstname": "Nathalie",
                    "surname": "Stone",
                    "phone_number": "02075625870",
                    "email": "nathaliestone@mhcapital.co.uk",
                    "linkedin": "in/nathaliestone/",
                }
            ],
            "offices": [
                {
                    "address_line2": "85 Queen Victoria Street",
                    "phone_number": "02075625870",
                    "postcode": "EC4V 4AB",
                }
            ]
        },
        "advisers_fca": [
            {
                "salutation": "Mr",
                "firstname": "David",
                "surname": "Stone",
                "phone_number": "02075625870",
                "email": "davidstone@mhcapital.co.uk",
                "linkedin": "in/davidstone/",
            },
            {
                "salutation": "Mrs",
                "firstname": "Nathalie",
                "surname": "Stone",
                "phone_number": "02075625870",
                "email": "nathaliestone@mhcapital.co.uk",
                "linkedin": "in/nathaliestone/",
            }
        ]
    },
    "z7z2ctsNH8R": {
        "firm": {
            "fca_num": "602217",
            "name": "3 Sixti Ltd",
            "alternative_name": "I C Wealth",
            "website": "www.3sixti.co.uk",
            "email": "arun@3sixti.co.uk",
            "offices": [
                {
                    "address_line2": "Queen Victoria St",
                    "phone_number": "02038656195",
                    "postcode": "EC4V 4AB",
                }
            ]
        },
        "advisers_fca": [
            {
                "salutation": "Mr",
                "firstname": "Arun",
                "surname": "Ram",
                "phone_number": "02038656195",
                "email": "arun@3sixti.co.uk",
            }
        ]
    }
}

# Initialize an empty DataFrame
df = pd.DataFrame()

# Extracting and combining data from JSON
for key in data.keys():
    firm_info = data[key]['firm']
    firm_data = {
        "Firm FCA Number": firm_info.get("fca_num", ""),
        "Firm Name": firm_info.get("name", ""),
        "Firm Alternative Name": firm_info.get("alternative_name", ""),
        "Firm Website": firm_info.get("website", ""),
        "Firm Email": firm_info.get("email", ""),
        "Firm LinkedIn": firm_info.get("linkedin", "")
    }

    # Advisers data
    advisers = firm_info.get("advisers", [])
    advisers_fca = data[key].get("advisers_fca", [])
    offices = firm_info.get("offices", [])

    # Combine all advisers and offices data
    for adviser in advisers + advisers_fca + offices:
        combined_data = {**firm_data, **adviser}
        df = df.append(combined_data, ignore_index=True)

# Selecting and renaming columns as per requirement
columns = [
    "Firm FCA Number", "Firm Name", "Firm Alternative Name", "Firm Website", 
    "Firm Email", "Firm LinkedIn", "title", "firstname", "surname", 
    "phone_number", "email", "linkedin", "address_line2", "postcode", "salutation"
]
df = df[columns]
df.columns = [
    "Firm FCA Number", "Firm Name", "Alternative Name", "Website", 
    "Email", "LinkedIn", "Title", "First Name", "Surname", 
    "Phone Number", "Email", "LinkedIn", "Address Line 2", "Postcode", "Salutation/Title"
]

# Export to Excel
excel_path = 'combined_data.xlsx'
df.to_excel(excel_path, index=False)

excel_path

