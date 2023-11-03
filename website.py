import streamlit as st
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def send_line_notification(token, message):
    url = "https://notify-api.line.me/api/notify"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"message": message}
    response = requests.post(url, headers=headers, data=data)
    return response.status_code

def append_to_new_sheet(soldier_id, name, surname, height, weight, body_temperature, body_water, new_weight, urine_color, bmi_risk, body_temperature_risk, body_water_risk, urine_color_risk):
    NEW_SHEET_URL = "https://docs.google.com/spreadsheets/d/12p8ohDnd5ZyO9H6nU6bjlND0_1pyE-cPguhcewape88/edit?usp=drive_web&ouid=108880626923731848508"
    spreadsheet = client.open_by_url(NEW_SHEET_URL)
    worksheet = spreadsheet.sheet1

    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Setup gspread
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("soldier-risk-calculator-93be17dccbd3.json", scope)
client = gspread.authorize(creds)

# Streamlit UI
st.title("โปรแกรมคำนวนความเสี่ยงต่อโรคลมร้อน สำหรับทหารใหม่")

# Initialize session state variables
if 'fetched' not in st.session_state:
    st.session_state.fetched = False
    st.session_state.record = {}

# Fixed Google Sheet URL
SHEET_URL = "https://docs.google.com/spreadsheets/d/18GA8Phnh7UOrySlzZMiOAHIPmoYJAvGYXm2aXhATpvc/edit?resourcekey#gid=164699372"

# Input for Soldier ID
soldier_id = st.text_input("รหัสประจำตัวทหารใหม่ (ใส่ 0 เพื่อแสดงรหัสทั้งหมด)")

# Fetch and display data using the specified structure
if st.button("ค้นหาข้อมูล"):
    spreadsheet = client.open_by_url(SHEET_URL)
    worksheet = spreadsheet.sheet1
    
    # Get all records
    records = worksheet.get_all_records()

    if soldier_id == "0":
        all_soldier_ids = [record.get("Soldier_ID") for record in records]
        st.write("รหัสประจำตัวทหารใหม่ทั้งหมด:")
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
    st.write(f"บันทึกเมื่อ: {st.session_state.record.get('Timestamp', 'N/A')}")
    st.write(f"รหัสประจำตัวทหารใหม่: {soldier_id}")
    st.write(f"ชื่อ: {st.session_state.record.get('Name', 'N/A')}")
    st.write(f"นามสกุล: {st.session_state.record.get('Surname', 'N/A')}")
    st.write(f"ความสูง: {st.session_state.record.get('Height', 'N/A')}")
    st.write(f"น้ำหนัก: {st.session_state.record.get('Weight', 'N/A')}")
    st.write("---")  # Separator

    # Additional Input Fields after fetching data
    st.subheader("กรอกข้อมูลเพิ่มเติมสำหรับการประเมินความเสี่ยง")
    body_temperature = st.number_input("อุณหภูมิร่างกาย", min_value=30.0, max_value=42.0)
    body_water = st.number_input("ปริมาณน้ำในร่างกาย", min_value=0.0, max_value=100.0)
    new_weight = st.number_input("น้ำหนักปัจจุบัน", min_value=30.0, max_value=200.0)
    urine_color = st.selectbox("สีปัสสาวะ", options=[0, 1, 2, 3, 4])

    # Calculate Button
    if st.button("คำนวนความเสี่ยง"):
        height = float(st.session_state.record.get("Height", 1))
        bmi = new_weight / ((height / 100) * (height / 100))
        bmi_risk = "RED" if bmi > 30 else "ORANGE" if 25 < bmi < 30 else "GREEN"
        body_temperature_risk = "RED" if body_temperature > 37.2 else "YELLOW" if 36.8 < body_temperature <= 37.2 else "GREEN"
        body_water_risk = "RED" if body_water < 50 else "YELLOW" if 50 <= body_water < 55 else "GREEN"
        urine_color_risk = ["GREEN", "GREEN", "YELLOW", "ORANGE", "RED"][urine_color]
    
        # Display colored boxes for risks
        color_mapping = {
            "RED": "#FF0000",
            "ORANGE": "#FFA500",
            "YELLOW": "#FFFF00",
            "GREEN": "#008000"
        }
    
        box_size = "40px"  # Adjust this value for a bigger or smaller box
    
        st.markdown(f"ความเสี่ยงจาก BMI: <div style='display: inline-block; width: {box_size}; height: {box_size}; background-color: {color_mapping[bmi_risk]}'></div>", unsafe_allow_html=True)
        st.markdown(f"ความเสี่ยงจาก อุณภูมิร่างกาย: <div style='display: inline-block; width: {box_size}; height: {box_size}; background-color: {color_mapping[body_temperature_risk]}'></div>", unsafe_allow_html=True)
        st.markdown(f"ความเสี่ยงจาก ปริมาณน้ำในร่างกาย: <div style='display: inline-block; width: {box_size}; height: {box_size}; background-color: {color_mapping[body_water_risk]}'></div>", unsafe_allow_html=True)
        st.markdown(f"ความเสี่ยงจาก สีปัสสาวะ: <div style='display: inline-block; width: {box_size}; height: {box_size}; background-color: {color_mapping[urine_color_risk]}'></div>", unsafe_allow_html=True)

        # Emoji mapping for risks
        emoji_mapping = {
            "RED": "🟥",
            "ORANGE": "🟧",
            "YELLOW": "🟨",
            "GREEN": "🟩"
        }
        
        # Format the message with emojis
        # Check if any of the risks are YELLOW, ORANGE, or RED
        if any(risk in ["YELLOW", "ORANGE", "RED"] for risk in [bmi_risk, body_temperature_risk, body_water_risk, urine_color_risk]):
            # Format the message with emojis
            message = f"""
            
--- ข้อมูลทหารใหม่ ---
รหัสประจำตัว: {soldier_id}
ชื่อ: {st.session_state.record.get('Name', 'N/A')} {st.session_state.record.get('Surname', 'N/A')}

----- ความเสี่ยง -----
BMI: {emoji_mapping[bmi_risk]}
อุณภูมิร่างกาย: {emoji_mapping[body_temperature_risk]}
ปริมาณน้ำในร่างกาย: {emoji_mapping[body_water_risk]}
สีปัสสาวะ: {emoji_mapping[urine_color_risk]}"""
    
            # Send the notification
            token = "S0zdZC7JLAu6l5vnHFublLHgeK3htiNWizef2aw6a4D"  # Your LINE Notify token
            send_line_notification(token, message)

        # Append the data along with the timestamp
        data = [timestamp, soldier_id, name, surname, height, weight, body_temperature, body_water, new_weight, urine_color, bmi_risk, body_temperature_risk, body_water_risk, urine_color_risk]
        worksheet.append_row(data)
    
    # Reset button
    if st.button("รีเซ็ต"):
        st.session_state.fetched = False
        st.session_state.record = {}
        st.experimental_rerun()  # Refresh the page 
