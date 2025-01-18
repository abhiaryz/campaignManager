import streamlit as st
import requests

# API endpoint for login
LOGIN_API_URL = "http://127.0.0.1:8000/api/token/"


def login_page():
    st.title("Login Page")

    username = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username and password:
            # Send login request using JSON payload
            payload = {"username": username, "password": password}
            response = requests.post(LOGIN_API_URL, json=payload)

            # Attempt to parse the response JSON
            try:
                result = response.json()
            except Exception as e:
                st.error(f"Error parsing response: {e}")
                return

            # Check if response is successful and contains expected data
            if response.status_code == 200 and result.get("status") == 200:
                data = result.get("data", {})
                token = data.get("access")

                if token:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.token = token
                    st.success("Logged in successfully!")
                    st.rerun()  # Refresh the app to update UI
                else:
                    st.error("Login failed: No access token found.")
            else:
                st.error("Invalid credentials or error from server. Please try again.")
        else:
            st.error("Please enter both username and password.")
