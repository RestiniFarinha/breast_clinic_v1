pip install gspread oauth2client gdown
pip show gspread

import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Google Sheets configuration
SHEET_ID = "1y-ZVShqCHRMKjdf8_MWChGmGy1iEUaGm"  # Extracted from your link
SHEET_NAME = "Sheet1"  # Ensure this matches the actual name of your sheet

# Setup Google Sheets API access
def connect_to_gsheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

# Load patient data from Google Sheets
def load_data():
    try:
        worksheet = connect_to_gsheet()
        data = pd.DataFrame(worksheet.get_all_records())
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

# Save patient data to Google Sheets
def save_data(data):
    try:
        worksheet = connect_to_gsheet()
        worksheet.clear()  # Clear existing data
        worksheet.update([data.columns.values.tolist()] + data.values.tolist())
        st.success("Data saved successfully!")
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Initialize session state
if "patient_data" not in st.session_state:
    st.session_state["patient_data"] = load_data()

# Function to calculate months between two dates
def calculate_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

st.title("Breast Clinic Patient Management")

# Input Section
mrn = st.text_input("MRN (Medical Record Number)")
dob = st.date_input("Date of Birth", value=datetime(1980, 1, 1))
followup_date = st.date_input("Date of Follow-up", value=datetime.today())

# Calculate Age Button
if st.button("Calculate Age"):
    age = (followup_date - dob).days // 365
    st.write(f"Patient's Age: {age} years")
else:
    age = None

last_radiotherapy_date = st.date_input("Date of Last Radiotherapy", value=datetime(2020, 1, 1))

# Calculate Time Since Treatment Button
if st.button("Calculate Time Since Radiotherapy"):
    time_since_treatment = calculate_months(last_radiotherapy_date, followup_date)
    st.write(f"Time Since Treatment: {time_since_treatment} months")
else:
    time_since_treatment = None

radiodermatitis = st.selectbox("Radiodermatitis", ["None", "I", "II", "III", "IV"])
telangiectasia = st.selectbox("Telangiectasia", ["No", "Yes"])
breast_pain = st.selectbox("Breast Pain", ["None", "I", "II", "III"])
cosmetic_outcome = st.selectbox("Cosmetic Outcome", ["Excellent", "Good", "Poor"])
breast_shrinkage = st.selectbox("Breast Shrinkage", ["No", "Yes"])
surgery_needed = st.selectbox("Surgery Needed for Cosmetic Side Effects", ["No", "Yes"])

# Recurrence Fields
local_recurrence = st.selectbox("Local Recurrence", ["No", "Yes"])
if local_recurrence == "Yes":
    local_recurrence_date = st.date_input("Date of Local Recurrence")
    time_to_local_recurrence = calculate_months(last_radiotherapy_date, local_recurrence_date)
else:
    local_recurrence_date = None
    time_to_local_recurrence = None

regional_recurrence = st.selectbox("Regional Recurrence", ["No", "Yes"])
if regional_recurrence == "Yes":
    regional_recurrence_date = st.date_input("Date of Regional Recurrence")
    time_to_regional_recurrence = calculate_months(last_radiotherapy_date, regional_recurrence_date)
else:
    regional_recurrence_date = None
    time_to_regional_recurrence = None

distant_recurrence = st.selectbox("Distant Recurrence", ["No", "Yes"])
if distant_recurrence == "Yes":
    distant_recurrence_date = st.date_input("Date of Distant Recurrence")
    time_to_distant_recurrence = calculate_months(last_radiotherapy_date, distant_recurrence_date)
else:
    distant_recurrence_date = None
    time_to_distant_recurrence = None

# Save Data Button
if st.button("Save Data"):
    # Check if patient already exists
    if mrn in st.session_state["patient_data"]["MRN"].values:
        followup_count = st.session_state["patient_data"][st.session_state["patient_data"]["MRN"] == mrn].shape[0] + 1
        suffix = f"#{followup_count}"
    else:
        suffix = ""

    new_data = {
        f"MRN{suffix}": mrn,
        f"Date_of_Birth{suffix}": dob,
        f"Age{suffix}": age,
        f"Date_of_Last_Radiotherapy{suffix}": last_radiotherapy_date,
        f"Followup_Date{suffix}": followup_date,
        f"Time_since_treatment{suffix}": time_since_treatment,
        f"Radiodermatitis{suffix}": radiodermatitis,
        f"Telangiectasia{suffix}": telangiectasia,
        f"Breast_Pain{suffix}": breast_pain,
        f"Cosmetic_Outcome{suffix}": cosmetic_outcome,
        f"Breast_Shrinkage{suffix}": breast_shrinkage,
        f"Surgery_Needed{suffix}": surgery_needed,
        f"Local_Recurrence{suffix}": local_recurrence,
        f"Date_of_Local_Recurrence{suffix}": local_recurrence_date,
        f"Time_to_Local_Recurrence{suffix}": time_to_local_recurrence,
        f"Regional_Recurrence{suffix}": regional_recurrence,
        f"Date_of_Regional_Recurrence{suffix}": regional_recurrence_date,
        f"Time_to_Regional_Recurrence{suffix}": time_to_regional_recurrence,
        f"Distant_Recurrence{suffix}": distant_recurrence,
        f"Date_of_Distant_Recurrence{suffix}": distant_recurrence_date,
        f"Time_to_Distant_Recurrence{suffix}": time_to_distant_recurrence,
    }

    # Append new data
    st.session_state["patient_data"] = pd.concat(
        [st.session_state["patient_data"], pd.DataFrame([new_data])]
    )

    # Save to Google Sheets
    save_data(st.session_state["patient_data"])
