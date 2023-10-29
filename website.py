import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup gspread
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("soldier-risk-calculator-93be17dccbd3.json", scope)
client = gspread.authorize(creds)

# Streamlit UI
st.title("Google Sheets Data Fetcher by Soldier ID")

# Initialize session state variables
if 'fetched' not in st.session_state:
    st.session_state.fetched = False
    st.session_state.record = {}

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
    else:
        # Filter records by Soldier_ID (ensure both are treated as strings)
        matching_records = [record for record in records if str(record.get("Soldier_ID")) == str(soldier_id)]
        
        if matching_records:
            st.session_state.fetched = True
            st.session_state.record = matching_records[0]  # Assuming one unique Soldier_ID, get the first matching record
        else:
            st.warning(f"No data found for Soldier_ID: {soldier_id}")

if st.session_state.fetched:
    # Display the fetched data
    st.write(f"Timestamp: {st.session_state.record.get('Timestamp', 'N/A')}")
    st.write(f"Soldier_ID: {soldier_id}")
    st.write(f"Name: {st.session_state.record.get('Name', 'N/A')}")
    st.write(f"Surname: {st.session_state.record.get('Surname', 'N/A')}")
    st.write(f"Height: {st.session_state.record.get('Height', 'N/A')}")
    st.write(f"Weight: {st.session_state.record.get('Weight', 'N/A')}")
    st.write("---")  # Separator

    # Additional Input Fields after fetching data
    st.subheader("Input Additional Data for Risk Calculation")
    body_temperature = st.number_input("Body_Temperature (Celsius)", min_value=30.0, max_value=42.0)
    body_water = st.number_input("Body_Water (%)", min_value=0.0, max_value=100.0)
    new_weight = st.number_input("New_Weight (Kg.)", min_value=30.0, max_value=200.0)
    urine_color = st.selectbox("Urine_Color", options=[0, 1, 2, 3, 4])

    # Calculate Button
    if st.button("Calculate Risk"):
        height = float(st.session_state.record.get("Height", 1))
        bmi = new_weight / ((height / 100) * (height / 100))
        bmi_risk = "RED" if bmi > 30 else "ORANGE" if 25 < bmi < 30 else "GREEN"
        body_temperature_risk = "RED" if body_temperature > 37.2 else "YELLOW" if 36.8 < body_temperature <= 37.2 else "GREEN"
        body_water_risk = "RED" if body_water < 55 else "YELLOW" if 55 <= body_water < 65 else "GREEN"
        urine_color_risk = ["GREEN", "GREEN", "YELLOW", "ORANGE", "RED"][urine_color]

        # Display colored boxes for risks
        color_mapping = {
            "RED": "#FF0000",
            "ORANGE": "#FFA500",
            "YELLOW": "#FFFF00",
            "GREEN": "#008000"
        }

        box_size = "40px"  # Adjust this value for a bigger or smaller box

        st.markdown(f"BMI Risk: <div style='display: inline-block; width: {box_size}; height: {box_size}; background-color: {color_mapping[bmi_risk]}'></div>", unsafe_allow_html=True)
        st.markdown(f"Body Temperature Risk: <div style='display: inline-block; width: {box_size}; height: {box_size}; background-color: {color_mapping[body_temperature_risk]}'></div>", unsafe_allow_html=True)
        st.markdown(f"Body Water Risk: <div style='display: inline-block; width: {box_size}; height: {box_size}; background-color: {color_mapping[body_water_risk]}'></div>", unsafe_allow_html=True)
        st.markdown(f"Urine Color Risk: <div style='display: inline-block; width: {box_size}; height: {box_size}; background-color: {color_mapping[urine_color_risk]}'></div>", unsafe_allow_html=True)

    # Reset button
    if st.button("Reset"):
        st.session_state.fetched = False
        st.session_state.record = {}
        st.experimental_rerun()  # Refresh the page
