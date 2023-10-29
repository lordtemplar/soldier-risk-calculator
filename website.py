import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup gspread
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("soldier-risk-calculator-93be17dccbd3.json", scope)
client = gspread.authorize(creds)

# Streamlit UI
st.title("Google Sheets Data Fetcher by Soldier ID")

# Fixed Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sTGeISgyGZgngAkBl86cPcdIzfYKFyotXQUhcslGilw/edit#gid=1050462434"

# Input for Soldier ID
soldier_id = st.text_input("Enter Soldier ID:")

# Fetch and display data using the specified structure
if st.button("Fetch Data"):
    spreadsheet = client.open_by_url(SHEET_URL)
    worksheet = spreadsheet.sheet1
    
    # Get all records
    records = worksheet.get_all_records()
    
    # Filter records by Soldier ID
    matching_records = [record for record in records if record.get("Soldier ID") == soldier_id]
    
    if matching_records:
        for record in matching_records:
            timestamp = record.get("Timestamp", "N/A")
            name = record.get("Name", "N/A")
            surname = record.get("Surname", "N/A")
            height = record.get("Height", "N/A")
            
            # Display the data in Streamlit
            st.write(f"Timestamp: {timestamp}")
            st.write(f"Soldier ID: {soldier_id}")
            st.write(f"Name: {name}")
            st.write(f"Surname: {surname}")
            st.write(f"Height: {height}")
            st.write("---")  # Separator
    else:
        st.warning(f"No data found for Soldier ID: {soldier_id}")
