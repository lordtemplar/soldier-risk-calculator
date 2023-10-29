import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup gspread
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("soldier-risk-calculator-93be17dccbd3.json", scope)
client = gspread.authorize(creds)

# Streamlit UI
st.title("Google Sheets CRUD App")

sheet_url = st.text_input("Enter Google Sheet URL", "https://docs.google.com/spreadsheets/d/1sTGeISgyGZgngAkBl86cPcdIzfYKFyotXQUhcslGilw/edit#gid=1050462434")

# Read
if st.button("Read Data"):
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_records()
    st.write(data)

# Write
new_data = st.text_input("Enter new data (comma separated)", "")
if st.button("Write Data"):
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.sheet1
    new_row = new_data.split(",")
    worksheet.append_row(new_row)

# Update
row_number = st.number_input("Enter the row number to update", min_value=1, value=1)
updated_data = st.text_input("Enter updated data (comma separated)", "")
if st.button("Update Data"):
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.sheet1
    new_row = updated_data.split(",")
    worksheet.update(f"A{row_number}", [new_row])

# Delete
row_number_to_delete = st.number_input("Enter the row number to delete", min_value=1, value=1)
if st.button("Delete Data"):
    spreadsheet = client.open_by_url(sheet_url)
    worksheet = spreadsheet.sheet1
    worksheet.delete_rows(row_number_to_delete)
