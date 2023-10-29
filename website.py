import streamlit as st
import gspread
from gspread_dataframe import get_as_dataframe

def get_first_row_from_sheet():
    # Use gspread to authenticate anonymously
    gc = gspread.client.Client()

    # Open the Google Sheet using its URL
    sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1sTGeISgyGZgngAkBl86cPcdIzfYKFyotXQUhcslGilw/edit?usp=drive_link").sheet1

    # Get the first row of data using gspread_dataframe
    df = get_as_dataframe(sheet, header=None, usecols=[0, 1, 2], nrows=1)  # Adjust usecols as needed
    return df.iloc[0].tolist()

def main():
    st.title("Streamlit and Google Sheets Connection Test")

    # Button to fetch data
    if st.button("Fetch First Row from Google Sheets"):
        data = get_first_row_from_sheet()
        st.write(data)

if __name__ == "__main__":
    main()
