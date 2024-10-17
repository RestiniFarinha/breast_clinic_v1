import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# Set filename for the Excel file stored in GitHub or locally
EXCEL_FILE = "patient_data.xlsx"

# Utility function to calculate months between two dates
def calculate_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

# Load existing data from Excel if it exists
if os.path.exists(EXCEL_FILE):
    st.session_state["patient_data"] = pd.read_excel(EXCEL_FILE)
else:
    st.session_state["patient_data"] = pd.DataFrame()

# Title
st.title("Patient Follow-Up Database")

# Patient Information Input Form
with st.form("patient_form"):
    st.subheader("Patient Information")

    mrn = st.text_input("MRN (Medical Record Number)").strip()

    # Allow older dates for Date of Birth
    dob = st.date_input("Date of Birth", min_value=date(1900, 1, 1))
    age = (datetime.now().date() - dob).days // 365  # Calculate age in years
    st.write(f"Age: {age} years")

    last_radiotherapy = st.date_input("Date of Last Radiotherapy", min_value=date(1900, 1, 1))
    followup_date = st.date_input("Follow-up Date", date.today())
    time_since_treatment = calculate_months(last_radiotherapy, followup_date)
    st.write(f"Time since treatment: {time_since_treatment} months")

    radiodermatitis = st.selectbox("Radiodermatitis", ["I", "II", "III", "IV"])
    telangiectasia = st.selectbox("Telangiectasia", ["Yes", "No"])
    breast_pain = st.selectbox("Breast Pain", ["I", "II", "III"])
    cosmetic_outcome = st.selectbox("Cosmetic Outcome", ["Excellent", "Good", "Poor"])
    breast_shrinkage = st.selectbox("Breast Shrinkage", ["Yes", "No"])
    surgery_needed = st.selectbox("Surgery Needed for Cosmetic Issues", ["Yes", "No"])

    # Local Recurrence Handling
    local_recurrence = st.selectbox("Local Recurrence", ["No", "Yes"])
    if local_recurrence == "Yes":
        local_recurrence_date = st.date_input("Date of Local Recurrence", min_value=last_radiotherapy)
        time_to_local_recurrence = calculate_months(last_radiotherapy, local_recurrence_date)
    else:
        local_recurrence_date, time_to_local_recurrence = None, None

    # Regional Recurrence Handling
    regional_recurrence = st.selectbox("Regional Recurrence", ["No", "Yes"])
    if regional_recurrence == "Yes":
        regional_recurrence_date = st.date_input("Date of Regional Recurrence", min_value=last_radiotherapy)
        time_to_regional_recurrence = calculate_months(last_radiotherapy, regional_recurrence_date)
    else:
        regional_recurrence_date, time_to_regional_recurrence = None, None

    # Distant Recurrence Handling
    distant_recurrence = st.selectbox("Distant Recurrence", ["No", "Yes"])
    if distant_recurrence == "Yes":
        distant_recurrence_date = st.date_input("Date of Distant Recurrence", min_value=last_radiotherapy)
        time_to_distant_recurrence = calculate_months(last_radiotherapy, distant_recurrence_date)
    else:
        distant_recurrence_date, time_to_distant_recurrence = None, None

    submitted = st.form_submit_button("Submit")

# Handle form submission
if submitted:
    # Create new data entry
    new_data = {
        "MRN": mrn,
        "Date_of_Birth": dob,
        "Age": age,
        "Date_of_Last_Radiotherapy": last_radiotherapy,
        "Followup_Date": followup_date,
        "Time_since_treatment": time_since_treatment,
        "Radiodermatitis": radiodermatitis,
        "Telangiectasia": telangiectasia,
        "Breast_Pain": breast_pain,
        "Cosmetic_Outcome": cosmetic_outcome,
        "Breast_Shrinkage": breast_shrinkage,
        "Surgery_Needed": surgery_needed,
        "Local_Recurrence": local_recurrence,
        "Date_of_Local_Recurrence": local_recurrence_date,
        "Time_to_Local_Recurrence": time_to_local_recurrence,
        "Regional_Recurrence": regional_recurrence,
        "Date_of_Regional_Recurrence": regional_recurrence_date,
        "Time_to_Regional_Recurrence": time_to_regional_recurrence,
        "Distant_Recurrence": distant_recurrence,
        "Date_of_Distant_Recurrence": distant_recurrence_date,
        "Time_to_Distant_Recurrence": time_to_distant_recurrence
    }

    # Check if MRN exists in the data
    if mrn in st.session_state["patient_data"]["MRN"].values:
        # If it exists, append new follow-up data with a suffix
        followup_number = st.session_state["patient_data"][st.session_state["patient_data"]["MRN"] == mrn].shape[0] + 1
        new_data = {f"{key}#{followup_number}": value for key, value in new_data.items()}

    # Add the new data to the DataFrame
    st.session_state["patient_data"] = pd.concat([st.session_state["patient_data"], pd.DataFrame([new_data])], ignore_index=True)

    # Save the updated DataFrame to Excel
    st.session_state["patient_data"].to_excel(EXCEL_FILE, index=False)
    st.success("Patient data saved successfully!")

# Display the current database
st.subheader("Current Database")
st.write(st.session_state["patient_data"])

# Option to download the data as an Excel file
if not st.session_state["patient_data"].empty:
    @st.cache_data
    def convert_df_to_excel(df):
        return df.to_excel(index=False, engine='xlsxwriter')

    excel_data = convert_df_to_excel(st.session_state["patient_data"])
    st.download_button("Download Excel", data=excel_data, file_name="patient_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
