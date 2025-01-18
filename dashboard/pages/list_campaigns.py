import streamlit as st
import requests
import pandas as pd

# API endpoint base URL for campaigns
CAMPAIGN_API_URL = "http://127.0.0.1:8000/api/campaigns/"


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
                "Carrier": ", ".join(map(str, campaign.get("carrier", [])))
                if campaign.get("carrier")
                else "N/A",
                "Device Price": ", ".join(map(str, campaign.get("device_price", [])))
                if campaign.get("device_price")
                else "N/A",
                "Keywords": ", ".join(map(str, campaign.get("keywords", [])))
                if campaign.get("keywords")
                else "N/A",
                "Proximity Store": ", ".join(
                    map(str, campaign.get("proximity_store", []))
                )
                if campaign.get("proximity_store")
                else "N/A",
                "Proximity": ", ".join(map(str, campaign.get("proximity", [])))
                if campaign.get("proximity")
                else "N/A",
                "Weather": ", ".join(map(str, campaign.get("weather", [])))
                if campaign.get("weather")
                else "N/A",
                "Start Time": campaign.get("start_time", "N/A"),
                "End Time": campaign.get("end_time", "N/A"),
                "Created At": campaign.get("created_at", "N/A"),
                "Updated At": campaign.get("updated_at", "N/A"),
            }
        )
    return pd.DataFrame(table_data)


def list_campaigns_page():
    st.title("List of Campaigns")

    # Custom CSS for styling the table
    st.markdown(
        """
    <style>
    table {
        width: 100%;
        border-collapse: collapse;
        font-family: Arial, sans-serif;
    }
    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }
    th {
        background-color: #04AA6D;
        color: white;
    }
    tr:nth-child(even) {background-color: #f2f2f2;}
    tr:hover {background-color: #ddd;}
    a {
        color: #1f77b4;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

    if not st.session_state.get("token"):
        st.error("You must be logged in to view campaigns.")
        return

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    query_params = st.experimental_get_query_params()

    # Check if a specific campaign is requested via query parameter
    print(query_params)
    if "campaign_id" in query_params:
        campaign_id = query_params["campaign_id"][0]
        st.subheader(f"Details for Campaign ID: {campaign_id}")

        # Fetch details for the selected campaign
        detail_url = f"{CAMPAIGN_API_URL}{campaign_id}/"
        print(detail_url)
        print(headers)
        response = requests.get(detail_url, headers=headers)
        # Uncomment the next line to debug response data:
        print(response.json())
        if response.status_code == 200:
            campaign_detail = response.json()
            # Display campaign details
            st.json(campaign_detail)
        else:
            st.error("Failed to fetch campaign details.")
    else:
        # No specific campaign requested, display list of campaigns
        response = requests.get(CAMPAIGN_API_URL, headers=headers)
        if response.status_code == 200:
            campaigns = response.json()
            df = process_campaigns_data(campaigns)

            # Convert the ID column into clickable links
            df["ID"] = df["ID"].apply(
                lambda id_val: f'<a href="list_campaigns?campaign_id={id_val}" target="_self">{id_val}</a>'
            )

            # Convert DataFrame to HTML and render it with styling
            html_table = df.to_html(escape=False, index=False)
            st.markdown(html_table, unsafe_allow_html=True)
        else:
            st.error("Failed to fetch campaigns.")
