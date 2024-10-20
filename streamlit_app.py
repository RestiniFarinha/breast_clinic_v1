import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Helper function to calculate time in months
def calculate_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

# Google Sheets connection setup
def connect_to_gsheets(json_keyfile):
    scope = ["https://spreadsheets.google.com/feeds", 
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(json_keyfile, scope)
    client = gspread.authorize(creds)
    return client

# Provide the path to your JSON keyfile (ensure it's placed in the right directory)
json_keyfile = ".streamlit/breast-clinic-439001-eaffe3c758c0.json"
client = connect_to_gsheets(json_keyfile)
worksheet = client.open("Breast_clinic_v2").sheet1

# Streamlit app layout
st.title("Patient Information Database")

# Session state for tracking recurrence dates
if 'local_recurrence_date' not in st.session_state:
    st.session_state.local_recurrence_date = None
if 'regional_recurrence_date' not in st.session_state:
    st.session_state.regional_recurrence_date = None
if 'distant_recurrence_date' not in st.session_state:
    st.session_state.distant_recurrence_date = None

# User input form
with st.form("patient_form", clear_on_submit=False):
    # Input fields
    date_of_birth = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1), max_value=datetime.today())
    mrn = st.text_input("MRN (Medical Record Number)")
    last_radiotherapy_date = st.date_input("Date of Last Radiotherapy")
    follow_up_date = st.date_input("Date of Follow-up", value=datetime.today())

    # Optional fields
    st.write("**Side Effects**")
    radiodermatitis = st.selectbox("Radiodermatitis", ["None", "I", "II", "III", "IV"])
    telangiectasia = st.radio("Telangiectasia", ["No", "Yes"])
    breast_pain = st.selectbox("Breast Pain", ["None", "I", "II", "III"])
    cosmetic_outcome = st.selectbox("Cosmetic Outcome", ["Excellent", "Good", "Poor"])
    breast_shrinkage = st.radio("Breast Shrinkage", ["No", "Yes"])
    surgery_for_cosmetics = st.radio("Surgery for Cosmetic Correction", ["No", "Yes"])

    # Recurrence information
    st.write("**Recurrence Details**")

    local_recurrence = st.radio("Local Recurrence", ["No", "Yes"])
    if local_recurrence == "Yes":
        st.session_state.local_recurrence_date = st.date_input("Date of Local Recurrence", max_value=datetime.today())
    
    regional_recurrence = st.radio("Regional Recurrence", ["No", "Yes"])
    if regional_recurrence == "Yes":
        st.session_state.regional_recurrence_date = st.date_input("Date of Regional Recurrence", max_value=datetime.today())
    
    distant_recurrence = st.radio("Distant Recurrence", ["No", "Yes"])
    if distant_recurrence == "Yes":
        st.session_state.distant_recurrence_date = st.date_input("Date of Distant Recurrence", max_value=datetime.today())

    # Button to calculate values (age, time intervals, etc.)
    calculate_button = st.form_submit_button("Calculate")

    if calculate_button:
        # Calculate age
        age = datetime.today().year - date_of_birth.year - (
            (datetime.today().month, datetime.today().day) < (date_of_birth.month, date_of_birth.day)
        )
        # Calculate time since radiotherapy
        time_since_treatment = calculate_months(last_radiotherapy_date, follow_up_date)

        # Calculate recurrence times (if applicable)
        time_to_local_recurrence = (
            calculate_months(last_radiotherapy_date, st.session_state.local_recurrence_date)
            if local_recurrence == "Yes" else None
        )
        time_to_regional_recurrence = (
            calculate_months(last_radiotherapy_date, st.session_state.regional_recurrence_date)
            if regional_recurrence == "Yes" else None
        )
        time_to_distant_recurrence = (
            calculate_months(last_radiotherapy_date, st.session_state.distant_recurrence_date)
            if distant_recurrence == "Yes" else None
        )

        # Store calculated values in session state for later use
        st.session_state['age'] = age
        st.session_state['time_since_treatment'] = time_since_treatment
        st.session_state['time_to_local_recurrence'] = time_to_local_recurrence
        st.session_state['time_to_regional_recurrence'] = time_to_regional_recurrence
        st.session_state['time_to_distant_recurrence'] = time_to_distant_recurrence

        # Display calculated values for preview
        st.write(f"**Calculated Age**: {age} years")
        st.write(f"**Time since last radiotherapy**: {time_since_treatment} months")
        if time_to_local_recurrence is not None:
            st.write(f"**Time to local recurrence**: {time_to_local_recurrence} months")
        if time_to_regional_recurrence is not None:
            st.write(f"**Time to regional recurrence**: {time_to_regional_recurrence} months")
        if time_to_distant_recurrence is not None:
            st.write(f"**Time to distant recurrence**: {time_to_distant_recurrence} months")

# Save button (outside the form) to ensure the user reviews and inputs recurrence dates before saving
if st.button("Save Information"):
    # Retrieve values from session state
    age = st.session_state.get('age', None)
    time_since_treatment = st.session_state.get('time_since_treatment', None)
    time_to_local_recurrence = st.session_state.get('time_to_local_recurrence', None)
    time_to_regional_recurrence = st.session_state.get('time_to_regional_recurrence', None)
    time_to_distant_recurrence = st.session_state.get('time_to_distant_recurrence', None)

    if age is None or time_since_treatment is None:
        st.error("Please calculate the age and treatment times before saving.")
    else:
        # Collect data to be saved
        data = {
            "MRN": mrn,
            "Age": age,
            "Time_since_treatment": time_since_treatment,
            "Radiodermatitis": radiodermatitis,
            "Telangiectasia": telangiectasia,
            "Breast_pain": breast_pain,
            "Cosmetic_outcome": cosmetic_outcome,
            "Breast_shrinkage": breast_shrinkage,
            "Surgery_for_cosmetics": surgery_for_cosmetics,
            "Local_recurrence": local_recurrence,
            "Time_to_local_recurrence": time_to_local_recurrence,
            "Regional_recurrence": regional_recurrence,
            "Time_to_regional_recurrence": time_to_regional_recurrence,
            "Distant_recurrence": distant_recurrence,
            "Time_to_distant_recurrence": time_to_distant_recurrence,
        }

        # Append to Google Sheets
        worksheet.append_row(list(data.values()))

        st.success("Patient data has been successfully saved!")
