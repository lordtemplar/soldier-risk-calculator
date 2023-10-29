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
soldier_id = st.text_input("Enter Soldier_ID:")

# Fetch and display data using the specified structure
if st.button("Fetch Data"):
    spreadsheet = client.open_by_url(SHEET_URL)
    worksheet = spreadsheet.sheet1
    
    # Get all records
    records = worksheet.get_all_records()

    if soldier_id == "0":
        all_soldier_ids = [record.get("Soldier_ID") for record in records]
        st.write("All Soldier_IDs:")
        for sid in all_soldier_ids:
            st.write(sid)
    # Filter records by Soldier_ID (ensure both are treated as strings)
    else:
        matching_records = [record for record in records if str(record.get("Soldier_ID")) == str(soldier_id)]
        
        if matching_records:
            for record in matching_records:
                timestamp = record.get("Timestamp", "N/A")
                name = record.get("Name", "N/A")
                surname = record.get("Surname", "N/A")
                height = record.get("Height", "N/A")
                weight = record.get("Weight", "N/A")
                
                # Display the data in Streamlit
                st.write(f"Timestamp: {timestamp}")
                st.write(f"Soldier_ID: {soldier_id}")
                st.write(f"Name: {name}")
                st.write(f"Surname: {surname}")
                st.write(f"Height: {height}")
                st.write(f"Weight: {weight}")
                st.write("---")  # Separator
        else:
            st.warning(f"No data found for Soldier_ID: {soldier_id}")

# Additional Input Fields
st.subheader("Input Additional Data for Risk Calculation")
body_temperature = st.number_input("Body_Temperature (Celsius)", min_value=30.0, max_value=42.0)
body_water = st.slider("Body_Water (%)", min_value=0, max_value=100)
new_weight = st.number_input("New_Weight (Kg.)", min_value=30.0, max_value=200.0)
urine_color = st.selectbox("Urine_Color", options=[0, 1, 2, 3, 4])

# Calculate Button
if st.button("Calculate Risk"):
    # Calculation Process
    height = float(record.get("Height", 1))  # Fetch height from the previously fetched record
    bmi = new_weight / ((height / 100) ** 2)

    # Output after calculation
    bmi_risk = "RED" if bmi > 30 else "ORANGE" if 25 < bmi < 30 else "GREEN"
    body_temperature_risk = "RED" if body_temperature > 37.2 else "YELLOW" if 36.8 < body_temperature <= 37.2 else "GREEN"
    body_water_risk = "RED" if body_water < 55 else "YELLOW" if 55 <= body_water < 65 else "GREEN"
    urine_color_risk = ["GREEN", "GREEN", "YELLOW", "ORANGE", "RED"][urine_color]

    # Display the results
    st.write(f"BMI: {bmi:.2f}")
    st.write(f"BMI Risk: {bmi_risk}")
    st.write(f"Body Temperature Risk: {body_temperature_risk}")
    st.write(f"Body Water Risk: {body_water_risk}")
    st.write(f"Urine Color Risk: {urine_color_risk}")
