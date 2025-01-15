import pandas as pd
import requests
import streamlit as st

# API URLs
LOGIN_API_URL = "http://127.0.0.1:8000/api/token/"
CAMPAIGNS_API_URL = "http://127.0.0.1:8000/api/campaigns/"
LOCATIONS_API_URL = "http://127.0.0.1:8000/api/location"

st.sidebar.page_link("pages/user.py")
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
    </style>
""",
    unsafe_allow_html=True,
)


# Functions
def process_campaigns_data(api_response):
    campaigns = api_response.get("data", [])
    table_data = []
    for campaign in campaigns:
        table_data.append(
            {
                "ID": campaign.get("id"),
                "Name": campaign.get("name", "N/A"),
                "Age": ", ".join(campaign.get("age", []))
                if campaign.get("age")
                else "N/A",
                "Device": ", ".join(campaign.get("device", []))
                if campaign.get("device")
                else "N/A",
                "Environment": ", ".join(campaign.get("environment", []))
                if campaign.get("environment")
                else "N/A",
                "Exchange": ", ".join(campaign.get("exchange", []))
                if campaign.get("exchange")
                else "N/A",
                "Location": ", ".join(map(str, campaign.get("location", [])))
                if campaign.get("location")
                else "N/A",
                "Language": ", ".join(map(str, campaign.get("language", [])))
                if campaign.get("language")
                else "N/A",
                "carrier": ", ".join(map(str, campaign.get("carrier", [])))
                if campaign.get("carrier")
                else "N/A",
                "device_price": ", ".join(map(str, campaign.get("device_price", [])))
                if campaign.get("device_price")
                else "N/A",
                "keywords": ", ".join(map(str, campaign.get("keywords", [])))
                if campaign.get("keywords")
                else "N/A",
                "proximity_store": ", ".join(
                    map(str, campaign.get("proximity_store", []))
                )
                if campaign.get("proximity_store")
                else "N/A",
                "proximity": ", ".join(map(str, campaign.get("proximity", [])))
                if campaign.get("proximity")
                else "N/A",
                "weather": ", ".join(map(str, campaign.get("weather", [])))
                if campaign.get("weather")
                else "N/A",
                "Start Time": campaign.get("start_time", "N/A"),
                "End Time": campaign.get("end_time", "N/A"),
                "Created At": campaign.get("created_at", "N/A"),
                "Updated At": campaign.get("updated_at", "N/A"),
            }
        )
    return pd.DataFrame(table_data)


def login(username, password):
    response = requests.post(
        LOGIN_API_URL, json={"username": username, "password": password}
    )
    if response.status_code == 200:
        try:
            response_data = response.json()
            return response_data.get("data")
        except ValueError:
            return None
    else:
        return None


def get_campaigns(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(CAMPAIGNS_API_URL, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def add_campaign(token, campaign_data):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(CAMPAIGNS_API_URL, json=campaign_data, headers=headers)
    return response.status_code, response.json()


def get_locations():
    """
    Fetches location data from the API and returns a list of tuples (id, display_name).
    """
    response = requests.get(LOCATIONS_API_URL)
    if response.status_code == 200:
        locations = response.json().get("data", [])
        return [
            (
                location["id"],
                f"{location['city']}, {location['state']} ({location['country']})",
            )
            for location in locations
        ]
    else:
        return []


# Persistent Login Setup
if "user" not in st.session_state:
    st.session_state["user"] = None

if "page" not in st.session_state:
    st.session_state["page"] = "login"

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False


def set_page(page_name):
    st.session_state["page"] = page_name


def save_login_data(user_data):
    st.session_state["user"] = user_data
    st.session_state["logged_in"] = True
    st.experimental_set_query_params(logged_in="true")


def load_login_data():
    query_params = st.experimental_get_query_params()
    if query_params.get("logged_in") == ["true"]:
        if not st.session_state["logged_in"]:
            st.session_state["logged_in"] = True


# Load login state on reload
load_login_data()

# Sidebar navigation
if st.session_state["user"]:
    with st.sidebar:
        st.title("Navigation")
        page = st.radio("Go to", ["Home", "Add Campaign", "User"])
        set_page(page)

# Dropdown options
age_options = ["18-25", "26-35", "36-45", "46-55", "56+"]
device_options = ["Mobile", "Desktop", "Tablet"]
environment_options = ["Web", "App"]
exchange_options = ["GoogleAds", "OpenX", "Others"]
language_options = ["English", "Hindi", "Spanish", "French"]
carrier_options = ["Airtel", "Jio", "Vodafone", "BSNL"]
device_price_options = ["Low", "Mid", "High"]


def upload_file(file, token):
    """
    Uploads a file to the proximityStore API and returns the ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": file}
    response = requests.post(
        "http://127.0.0.1:8000/api/proximityStore/", headers=headers, files=files
    )
    if response.status_code == 200:
        return response.json().get("id")
    else:
        st.error(f"Failed to upload file: {file.name}")
        return None


if st.session_state["page"] == "Home" and st.session_state["user"]:
    st.title("Home - Campaigns Data")
    token = st.session_state["user"]["access"]
    campaigns_data = get_campaigns(token)
    if campaigns_data:
        df = process_campaigns_data(campaigns_data)
        st.dataframe(df)
    else:
        st.error("Failed to fetch campaigns data.")

elif st.session_state["page"] == "Add Campaign" and st.session_state["user"]:
    st.title("Add Campaign")

    # Fetch locations dynamically
    locations = get_locations()
    location_ids = [loc[0] for loc in locations]
    location_names = [loc[1] for loc in locations]

    with st.form("add_campaign_form"):
        campaign_name = st.text_input("Name")
        selected_age = st.multiselect("Select Age Group", options=age_options)
        selected_device = st.multiselect("Select Device", options=device_options)
        selected_environment = st.multiselect(
            "Select Environment", options=environment_options
        )
        selected_exchange = st.multiselect("Select Exchange", options=exchange_options)
        selected_language = st.multiselect("Select Language", options=language_options)
        selected_carrier = st.multiselect("Select Carrier", options=carrier_options)
        selected_device_price = st.multiselect(
            "Select Device Price", options=device_price_options
        )
        selected_locations = st.multiselect(
            "Select Location(s)",
            options=location_names,
            format_func=lambda x: x,
        )
        # Map selected names back to IDs
        selected_location_ids = [
            location_ids[location_names.index(name)] for name in selected_locations
        ]

        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time")

        uploaded_files = st.file_uploader(
            "Choose Keywords files", accept_multiple_files=True
        )
        weathers = st.file_uploader("Choose Weather files", accept_multiple_files=True)
        proximitys = st.file_uploader(
            "Choose Proximity files", accept_multiple_files=True
        )
        proximity_stores = st.file_uploader(
            "Choose Proximity Store files", accept_multiple_files=True
        )

        submit = st.form_submit_button("Submit")

    if submit:
        token = st.session_state["user"]["access"]
        keyword_ids = []
        for file in uploaded_files:
            file_id = upload_file(file, token)
            if file_id:
                keyword_ids.append({"id": file_id})
        weathers_ids = []
        proximitys_ids = []
        proximity_stores_ids = []

        for file in weathers:
            file_id = upload_file(file, token)
            if file_id:
                weathers_ids.append({"id": file_id})

        for file in proximitys:
            file_id = upload_file(file, token)
            if file_id:
                proximitys_ids.append({"id": file_id})

        for file in proximity_stores:
            file_id = upload_file(file, token)
            if file_id:
                proximity_stores_ids.append({"id": file_id})

        campaign_data = {
            "name": campaign_name,
            "age": selected_age,
            "device": selected_device,
            "environment": selected_environment,
            "exchange": selected_exchange,
            "language": selected_language,
            "carrier": selected_carrier,
            "device_price": selected_device_price,
            "start_time": start_time.strftime("%H:%M") if start_time else None,
            "end_time": end_time.strftime("%H:%M") if end_time else None,
            "location": selected_location_ids,
            "keywords": keyword_ids,
            "weather": weathers_ids,
            "proximity": proximitys_ids,
            "proximity_store": proximity_stores_ids,
        }
        status, response = add_campaign(token, campaign_data)
        if status == 200:
            st.success("Campaign added successfully!")
        else:
            st.error(f"Failed to add campaign: {response}")

elif st.session_state["page"] == "User" and st.session_state["user"]:
    st.title("User")

elif st.session_state["page"] == "login":
    st.title("Login Page")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            user_data = login(username, password)
            if user_data and "access" in user_data:
                save_login_data(user_data)
                set_page("Home")
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter both username and password.")
