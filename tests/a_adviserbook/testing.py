


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
excel_path = '/mnt/data/combined_data.xlsx'
df.to_excel(excel_path, index=False)