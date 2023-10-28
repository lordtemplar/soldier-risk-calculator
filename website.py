import streamlit as st

def main():
    st.title("ID No. Input Interface")

    # Input textbox for ID No.
    id_no = st.text_input("Enter ID No.")

    # Submit button
    if st.button("Submit"):
        st.write(f"You have submitted ID No.: {id_no}")

if __name__ == "__main__":
    main()
