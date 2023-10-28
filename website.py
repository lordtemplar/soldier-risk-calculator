import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_first_row_from_sheet():
    # Set up the credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/soldier-risk-calculator-6f1676d0800b.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet using its name
    sheet = client.open("/SoldierRiskCalculator(Responses)").sheet1

    # Get the first row of data
    return sheet.row_values(1)

def main():
    st.title("Streamlit and Google Sheets Connection Test")

    # Button to fetch data
    if st.button("Fetch First Row from Google Sheets"):
        data = get_first_row_from_sheet()
        st.write(data)

if __name__ == "__main__":
    main()
