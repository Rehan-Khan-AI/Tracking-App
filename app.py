import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import json

# Streamlit UI
st.title("Smart Shipment Tracker: Real-Time Delivery Status (Google Sheets)")

# Google Sheet URL (replace with yours)
sheet_url = "https://docs.google.com/spreadsheets/d/1rb6pCr2kWg4SiRYQ4YX19q9xpUwfwRs2bokfp4jrM44/edit#gid=0"

# Path to the service account credentials file
credentials_file = 'rehan-project-425405-d063e7ff9308.json'  # Replace with your actual path

# Function to create Google credentials object
def get_credentials(credentials_file):
    with open(credentials_file, 'r') as f:
        credentials_info = json.load(f)
    # Define the required scopes
    scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    return credentials

# Function to get data from Google Sheets
def get_sheet_data(credentials, spreadsheet_id, range_name):
    service = build('sheets', 'v4', credentials=credentials)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=range_name).execute()
    values = result.get('values', [])
    return values

# Main function to load data and handle user input
def main():
    try:
        # Get credentials
        credentials = get_credentials(credentials_file)
        
        # Get spreadsheet ID from the URL
        spreadsheet_id = sheet_url.split('/')[5]
        
        # Range name (worksheet and range to read)
        range_name = 'Sheet1'  # Adjust as necessary
        
        # Get data from Google Sheets
        values = get_sheet_data(credentials, spreadsheet_id, range_name)
        
        # Convert to DataFrame
        if values:
            columns = values[0]  # First row as columns
            data = values[1:]  # Data starts from second row
            df = pd.DataFrame(data, columns=columns)
        else:
            st.error("No data found in the Google Sheet.")
            return
        
        # Input field for single tracking number
        tracking_id_input = st.text_input("Enter Tracking ID (Optional):")
        
        if tracking_id_input:
            # Check if the tracking ID exists in the DataFrame
            if tracking_id_input in df['Tracking Number'].tolist():
                # Tracking ID found, retrieve corresponding status
                status = df[df['Tracking Number'] == tracking_id_input]['Status'].values[0]
                st.write(f"**Tracking ID:** {tracking_id_input}")
                st.write(f"**Status:** {status}")
            else:
                st.error(f"Tracking ID '{tracking_id_input}' not found in your Google Sheet.")
        else:
            st.write("Enter a tracking ID in the field above to check its status, or the available tracking numbers are listed below:")
            st.write(df)  # Display the data from the Google Sheet

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Run the main function
if __name__ == "__main__":
    main()
