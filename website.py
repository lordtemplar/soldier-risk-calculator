import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def get_data_from_sheet(soldier_id):
    # Set up the credentials
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("soldier-risk-calculator
/soldier-risk-calculator-6f1676d0800b.json", scope)
    client = gspread.authorize(creds)

    # Open the Google Sheet using its name
    sheet = client.open("/soldier-risk-calculator/Soldier Risk Calculator (Responses)").sheet1

    # Search for the soldier ID and retrieve data
    try:
        cell = sheet.find(soldier_id)
        row_values = sheet.row_values(cell.row)
        # Assuming the columns are in the order: Soldier ID, Name, Surname, Height
        return {"Name": row_values[1], "Surname": row_values[2], "Height": row_values[3]}
    except gspread.exceptions.CellNotFound:
        return None

def main():
    st.title("Health Data Input Interface")

    # Input fields
    soldier_id = st.text_input("Enter Soldier ID")
    weight = st.number_input("Enter Weight (kg)", min_value=0.0)
    body_temp = st.number_input("Enter Body Temperature (°C)", min_value=0.0)
    body_water = st.number_input("Enter Body Water (%)", min_value=0.0)
    urine_color = st.selectbox("Select Urine Color", ["Clear", "Light Yellow", "Yellow", "Dark Yellow", "Amber", "Brown"])

    # Calculate button
    if st.button("Calculate"):
        st.write(f"Soldier ID: {soldier_id}")
        st.write(f"Weight: {weight} kg")
        st.write(f"Body Temperature: {body_temp} °C")
        st.write(f"Body Water: {body_water} %")
        st.write(f"Urine Color: {urine_color}")

        # Retrieve data from Google Sheets
        data = get_data_from_sheet(soldier_id)
        if data:
            st.write(f"Name: {data['Name']}")
            st.write(f"Surname: {data['Surname']}")
            st.write(f"Height: {data['Height']}")
        else:
            st.error("Soldier ID not found in the database.")

if __name__ == "__main__":
    main()
