import streamlit as st

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

if __name__ == "__main__":
    main()
