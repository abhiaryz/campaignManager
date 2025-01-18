import streamlit as st
import login
import register
from pages import user, list_campaigns, add_campaign, fetch_campaign_by_id

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "token" not in st.session_state:
    st.session_state.token = None


# Home page with login and register options
def main_page():
    if st.session_state.logged_in:
        # Display sidebar and content if logged in
        st.sidebar.title("Navigation")
        page = st.sidebar.selectbox(
            "Select a page", ["User", "List Campaigns", "Add Campaign"]
        )

        if page == "User":
            user.user_page()
        elif page == "List Campaigns":
            list_campaigns.list_campaigns_page()
        elif page == "Add Campaign":
            add_campaign.add_campaign_page()
    else:
        # If not logged in, show login or register
        page = st.selectbox("Select Action", ["Login", "Register"])

        if page == "Login":
            login.login_page()
        elif page == "Register":
            register.register_page()


if __name__ == "__main__":
    main_page()
