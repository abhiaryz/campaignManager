import streamlit as st
import requests

# API endpoint to fetch user info (for example)
USER_API_URL = "http://127.0.0.1:8000/api/user/"


def user_page():
    st.title("User Page")

    if st.session_state.token:
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        response = requests.get(USER_API_URL, headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            st.write(f"Username: {user_data['username']}")
            st.write(f"Email: {user_data['email']}")
            st.write(f"First Name: {user_data['first_name']}")
            st.write(f"Last Name: {user_data['last_name']}")
        else:
            st.error("Failed to fetch user data.")
    else:
        st.error("You must be logged in to view this page.")
