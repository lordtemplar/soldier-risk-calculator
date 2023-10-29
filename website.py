import streamlit as st
import gspread

def get_first_row_from_sheet():
    # Use gspread to authenticate using your personal credentials
    gc = gspread.service_account(filename=None)  # If you have no service account, it will use your personal credentials

    # Open the Google Sheet using its ID
    sheet = gc.open_by_key("1050462434").sheet1

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
