import streamlit as st
import requests
import json

# API endpoint for registration
REGISTER_API_URL = "http://127.0.0.1:8000/api/register/"


def register_page():
    st.title("Register Page")

    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        if password == confirm_password:
            if first_name and last_name and email and password:
                # Send register request
                payload = {
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email,
                    "password": password,
                }
                headers = {"Content-Type": "application/json"}
                response = requests.post(
                    REGISTER_API_URL, headers=headers, data=json.dumps(payload)
                )

                if response.status_code == 201:
                    st.success(f"User {email} registered successfully!")
                else:
                    st.error("Registration failed. Please try again.")
            else:
                st.error("Please fill all the fields.")
        else:
            st.error("Passwords do not match.")
