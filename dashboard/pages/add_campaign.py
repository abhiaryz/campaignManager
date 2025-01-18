import streamlit as st
import requests

# API endpoint to add campaign
CAMPAIGNS_API_URL = ADD_CAMPAIGN_API_URL = "http://127.0.0.1:8000/api/campaigns/"
LOCATIONS_API_URL = "http://127.0.0.1:8000/api/location"


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


age_options = ["18-25", "26-35", "36-45", "46-55", "56+"]
device_options = ["Mobile", "Desktop", "Tablet"]
environment_options = ["Web", "App"]
exchange_options = ["GoogleAds", "OpenX", "Others"]
language_options = ["English", "Hindi", "Spanish", "French"]
carrier_options = ["Airtel", "Jio", "Vodafone", "BSNL"]
device_price_options = ["Low", "Mid", "High"]


def upload_file_proximityStore(file, token):
    """
    Uploads a file to the proximityStore API and returns the ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": file}
    response = requests.post(
        "http://127.0.0.1:8000/api/proximityStore/", headers=headers, files=files
    )
    if response.status_code == 201:
        return response.json().get("id")
    else:
        st.error(f"Failed to upload file: {file.name}")
        return None


def upload_file_keyword(file, token):
    """
    Uploads a file to the proximityStore API and returns the ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": file}
    response = requests.post(
        "http://127.0.0.1:8000/api/keywords/", headers=headers, files=files
    )
    if response.status_code == 201:
        return response.json().get("id")
    else:
        st.error(f"Failed to upload file: {file.name}")
        return None


def upload_file_weather(file, token):
    """
    Uploads a file to the proximityStore API and returns the ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": file}
    response = requests.post(
        "http://127.0.0.1:8000/api/weather/", headers=headers, files=files
    )
    if response.status_code == 201:
        return response.json().get("id")
    else:
        st.error(f"Failed to upload file: {file.name}")
        return None


def upload_file_proximity(file, token):
    """
    Uploads a file to the proximityStore API and returns the ID.
    """
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": file}
    response = requests.post(
        "http://127.0.0.1:8000/api/proximity/", headers=headers, files=files
    )
    if response.status_code == 201:
        return response.json().get("id")
    else:
        st.error(f"Failed to upload file: {file.name}")
        return None


def add_campaign_page():
    st.title("Add Campaign")
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
        token = st.session_state.token
        weathers_ids = []
        proximitys_ids = []
        proximity_stores_ids = []
        keyword_ids = []

        for file in uploaded_files:
            file_id = upload_file_keyword(file, token)
            if file_id:
                keyword_ids.append({"id": file_id})

        for file in weathers:
            file_id = upload_file_weather(file, token)
            if file_id:
                weathers_ids.append({"id": file_id})

        for file in proximitys:
            file_id = upload_file_proximity(file, token)
            if file_id:
                proximitys_ids.append({"id": file_id})

        for file in proximity_stores:
            file_id = upload_file_proximityStore(file, token)
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
