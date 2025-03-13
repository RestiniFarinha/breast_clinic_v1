import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# File path for local storage
excel_file = "G:/breast_clinic_v1/Breast_clinic.xlsx"

# Helper function to calculate time in months
def calculate_months(start_date, end_date):
    return (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)

# Load existing data or create a new DataFrame
def load_data():
    if os.path.exists(excel_file):
        return pd.read_excel(excel_file)
    else:
        return pd.DataFrame(columns=[
            "MRN", "Date_of_Birth", "Age", "Date_of_Last_Radiotherapy", "Follow_up_date", "Follow_up_time",
            "Histology", "Grade", "ER", "PR", "HER2", "TNM", "Surgery", "Surgery_date",
            "Neoadjuvant_hormonal_therapy", "Neoadjuvant_chemotherapy", "Neoadjuvant_chemotherapy_type",
            "Adjuvant_chemotherapy", "Adjuvant_chemotherapy_type",
            "Laterality", "Volume",
            "Radiodermatitis", "Telangiectasia", "Breast_pain", "Cosmetic_outcome", "Breast_shrinkage", "Hyperpigmentation",
            "Lymphedema", "Surgery_for_cosmetics",
            "Breast_edema", "Breast_fibrosis", "Breast_retraction", "Breast_necrosis", "Breast_hematoma", "Breast_infection",
            "Breast_seroma", "Tumor_bed_fibrosis", "Tumor_bed_retraction", "Tumor_bed_necrosis", "Tumor_bed_hematoma",
            "Tumor_bed_infection", "Tumor_bed_seroma",
            "Pneumonitis", "Esophagitis", "Neuropathy", "Fatigue",
            "Local_recurrence", "Time_to_local_recurrence", "Regional_recurrence", "Time_to_regional_recurrence",
            "Distant_recurrence", "Time_to_distant_recurrence"
        ])

# Function to safely retrieve data, handling NaN values
def safe_get(data, key, default=""):
    value = data.get(key, default)
    return value if pd.notna(value) else default

# Function to safely retrieve a list from stored string values
def safe_get_list(data, key):
    value = data.get(key, "")
    if pd.isna(value) or not isinstance(value, str):
        return []
    return [item.strip() for item in value.replace("[", "").replace("]", "").replace("'", "").split(",") if item]


# Function to fetch existing patient data by MRN
def get_patient_data(mrn):
    df = load_data()
    df["MRN"] = df["MRN"].astype(str).str.strip()
    mrn = str(mrn).strip()
    if mrn in df["MRN"].values:
        return df[df["MRN"] == mrn].iloc[0].to_dict()
    return None

# Function to save patient data (Appending Instead of Overwriting)
def save_data(data):
    df = load_data()
    df["MRN"] = df["MRN"].astype(str).str.strip()
    data["MRN"] = str(data["MRN"]).strip()

    # Append new data as a separate row instead of replacing the existing one
    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    # Save the updated DataFrame
    df.to_excel(excel_file, index=False)


# Streamlit app layout
st.title("Patient Information Database - Breast 30Gy SIB Clinic")

# Input for MRN
mrn = st.text_input("Enter MRN (Medical Record Number) and press Enter", key="mrn")

# Fetch existing patient data
patient_data = get_patient_data(mrn) if mrn else None

# Start the form
with st.form("patient_form", clear_on_submit=False):
    st.subheader("Patient Details")

    date_of_birth = st.date_input("Date of Birth",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Birth", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    mrn = st.text_input("MRN (Medical Record Number)", value=mrn)

    last_radiotherapy_date = st.date_input("Date of Last Radiotherapy",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Last_Radiotherapy", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    follow_up_date = st.date_input("Date of Follow-up",
        value=datetime.strptime(safe_get(patient_data, "Follow_up_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    Histology = st.selectbox("Histology", ["IDC", "ILC", "DCIS", "LCIS", "IDC+DCIS", "IDC+LCIS", "IDC+DCIS+LCIS", "Others"],
        index=["IDC", "ILC", "DCIS", "LCIS", "IDC+DCIS", "IDC+LCIS", "IDC+DCIS+LCIS", "Others"].index(safe_get(patient_data, "Histology", "IDC")) if patient_data else 0
    )

    ER = st.radio("ER", ["Negative", "Positive"],
        index=["Negative", "Positive"].index(safe_get(patient_data, "ER", "Negative")) if patient_data else 0
    )

    PR = st.radio("PR", ["Negative", "Positive"],
        index=["Negative", "Positive"].index(safe_get(patient_data, "PR", "Negative")) if patient_data else 0
    )

    HER2 = st.radio("HER 2", ["Negative", "Positive"],
        index=["Negative", "Positive"].index(safe_get(patient_data, "HER2", "Negative")) if patient_data else 0
    )


    Grade = st.selectbox("Grade", ["I", "II", "III"],
        index=["I", "II", "III"].index(safe_get(patient_data, "Grade", "I")) if patient_data else 0
    )

    TNM = st.multiselect("TNM", ["T1", "T2", "T3", "T4", "N0", "N1", "N2", "N3", "M0", "M1"],
        default=safe_get_list(patient_data, "TNM") if patient_data else []
    )

    Surgery = st.multiselect("Surgery", ["Mastectomy", "Lumpectomy", "SLNB", "ALND", "Others"],
        default=safe_get_list(patient_data, "Surgery") if patient_data else []
    )

    Surgery_date = st.date_input("Date of Surgery",
        value=datetime.strptime(safe_get(patient_data, "Surgery_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    # Systemic Treatment
    st.subheader("Systemic Treatment")
    Neoadjuvant_hormonal_therapy = st.radio("Neoadjuvant Hormonal Therapy", ["No", "Yes"],
        index=["No", "Yes"].index(safe_get(patient_data, "Neoadjuvant_hormonal_therapy", "No")) if patient_data else 0
    )

    Neoadjuvant_chemotherapy_type = st.multiselect("Neoadjuvant Chemotherapy", 
        ["None", "AC → TC", "FEC → T", "TC", "CDK4/6", "Pembro", "AC → THP", "TDXD", "TDM1", "Durvalumab","TROP2", "Others"],
        default=safe_get_list(patient_data, "Neoadjuvant_chemotherapy_type") if patient_data else []
    )

    Adjuvant_chemotherapy_type = st.multiselect("Adjuvant Chemotherapy", 
        ["None","AC → TC", "FEC → T", "TC", "CDK4/6", "Pembro", "AC → THP", "TDXD", "TDM1", "Durvalumab", "Capecitabine", "Hormones", "TROP2", "Others"],
        default=safe_get_list(patient_data, "Adjuvant_chemotherapy_type") if patient_data else []
    )

    # Treatment Details
    st.subheader("Treatment Details")
    Laterallity = st.selectbox("Laterality", ["Left", "Right", "Bilateral"],
        index=["Left", "Right", "Bilateral"].index(safe_get(patient_data, "Laterality", "Left")) if patient_data else 0
    )
    Volume = st.selectbox("Volume", ["Whole Breast", "Partial Breast", "Locorregional Breast", "Chestwall", "Locorregional Chestwall"],
        index=["Whole Breast", "Partial Breast", "Locorregional Breast", "Chestwall", "Locorregional Chestwall"].index(safe_get(patient_data, "Volume", "Whole Breast")) if patient_data else 0
    )

    # Side effects - Cosmesis
    st.subheader("Side Effects - Cosmesis")
    radiodermatitis = st.selectbox("Radiodermatitis", ["None", "I", "II", "III", "IV"])
    telangiectasia = st.radio("Telangiectasia", ["None", "I", "II"])
    cosmetic_outcome = st.selectbox("Cosmetic Outcome", ["Excellent", "Good", "Poor"])
    Hyperpigmentation = st.radio("Hyperpigmentation", ["None", "I", "II", "III"])
    Lymphedema = st.radio("Lymphedema", ["None", "I", "II", "III"])
    surgery_for_cosmetics = st.radio("Surgery for Cosmetic Correction", ["No", "Yes"])

    # Side effects - Breast and Tumor Bed
    st.subheader("Side Effects - Breast and Tumor Bed")
    breast_shrinkage = st.radio("Breast Shrinkage", ["No", "Yes"])
    breast_pain = st.selectbox("Breast Pain", ["None", "I", "II", "III"])
    Breast_edema = st.radio("Breast Edema", ["No", "Yes"])
    Breast_fibrosis = st.radio("Breast Fibrosis", ["None", "I", "II", "III"])
    Breast_retraction = st.radio("Breast Retraction", ["No", "Yes"])
    Breast_necrosis = st.radio("Breast Necrosis", ["No", "Yes"])
    Breast_hematoma = st.radio("Breast Hematoma", ["No", "Yes"])
    Breast_infection = st.radio("Breast Infection", ["No", "Yes"])
    Breast_seroma = st.radio("Breast Seroma", ["No", "Yes"])
    Tumor_bed_fibrosis = st.radio("Tumor Bed Fibrosis", ["None", "I", "II", "III"])
    Tumor_bed_retraction = st.radio("Tumor Bed Retraction", ["No", "Yes"])
    Tumor_bed_necrosis = st.radio("Tumor Bed Necrosis", ["No", "Yes"])
    Tumor_bed_hematoma = st.radio("Tumor Bed Hematoma", ["No", "Yes"])
    Tumor_bed_infection = st.radio("Tumor Bed Infection", ["No", "Yes"])
    Tumor_bed_seroma = st.radio("Tumor Bed Seroma", ["No", "Yes"])


    # Side effects - Others
    st.subheader("Side Effects - Others")
    Pneumonitis = st.radio("Pneumonitis", ["None", "I", "II", "III", "IV", "V"])
    Esophagitis = st.radio("Esophagitis", ["None", "I", "II", "III", "IV", "V"])
    Neuropathy = st.radio("Neuropathy", ["None", "I", "II", "III"])
    Fatigue = st.radio("Fatigue", ["None", "I", "II", "III"])

    # Recurrence details
    st.subheader("Recurrence Details")
    local_recurrence = st.radio("Local Recurrence", ["No", "Yes"])
    regional_recurrence = st.radio("Regional Recurrence", ["No", "Yes"])
    distant_recurrence = st.radio("Distant Recurrence", ["No", "Yes"])

    time_to_local_recurrence = None
    if local_recurrence == "Yes":
        time_to_local_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Local Recurrence"))

    time_to_regional_recurrence = None
    if regional_recurrence == "Yes":
        time_to_regional_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Regional Recurrence"))

    time_to_distant_recurrence = None
    if distant_recurrence == "Yes":
        time_to_distant_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Distant Recurrence"))

    # Submit button to trigger calculation
    submitted = st.form_submit_button("Calculate")

    if submitted:
        st.session_state.age = datetime.today().year - date_of_birth.year - (
            (datetime.today().month, datetime.today().day) < (date_of_birth.month, date_of_birth.day)
        )
        st.session_state.time_since_treatment = calculate_months(last_radiotherapy_date, follow_up_date)
        st.session_state.time_to_local_recurrence = time_to_local_recurrence if local_recurrence == "Yes" else "N/A"
        st.session_state.time_to_regional_recurrence = time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A"
        st.session_state.time_to_distant_recurrence = time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A"

        st.subheader("Calculated Results:")
        st.write(f"**Calculated Age**: {st.session_state.age} years")
        st.write(f"**Time since last radiotherapy**: {st.session_state.time_since_treatment} months")
        if local_recurrence == "Yes":
            st.write(f"**Time to local recurrence**: {st.session_state.time_to_local_recurrence} months")
        if regional_recurrence == "Yes":
            st.write(f"**Time to regional recurrence**: {st.session_state.time_to_regional_recurrence} months")
        if distant_recurrence == "Yes":
            st.write(f"**Time to distant recurrence**: {st.session_state.time_to_distant_recurrence} months")

# Save button is placed outside the form so it persists after submission
if st.button("Save Information"):
    if st.session_state.age is None or st.session_state.time_since_treatment is None:
        st.error("Please calculate the age and treatment times before saving.")
    else:
        data = {
            # Patient details
            "MRN": mrn if mrn else "N/A",
            "Date_of_Birth": date_of_birth.strftime("%Y-%m-%d"),
            "Age": st.session_state.age,
            "Date_of_Last_Radiotherapy": last_radiotherapy_date.strftime("%Y-%m-%d"),
            "Follow_up_date": follow_up_date.strftime("%Y-%m-%d"),
            "Follow_up_time": st.session_state.time_since_treatment,
            "Histology": Histology,
            "Grade": Grade,
            "ER": ER,
            "PR": PR,
            "HER2": HER2,
            "TNM": TNM,
            "Surgery": Surgery,
            "Surgery_date": Surgery_date.strftime("%Y-%m-%d"),
            # Systemic Treatment
            "Neoadjuvant_hormonal_therapy": Neoadjuvant_hormonal_therapy,
            "Neoadjuvant_chemotherapy_type": Neoadjuvant_chemotherapy_type,
            "Adjuvant_chemotherapy_type": Adjuvant_chemotherapy_type,
            # Treatment Details
            "Laterality": Laterallity,
            "Volume": Volume,
            # Side Effects - Cosmesis
            "Radiodermatitis": radiodermatitis,
            "Telangiectasia": telangiectasia,
            "Cosmetic_outcome": cosmetic_outcome,
            "Hyperpigmentation": Hyperpigmentation,
            "Lymphedema": Lymphedema,
            "Surgery_for_cosmetics": surgery_for_cosmetics,
            # Side Effects - Breast and Tumor Bed
            "Breast_shrinkage": breast_shrinkage,
            "Breast_pain": breast_pain,
            "Breast_edema": Breast_edema,
            "Breast_fibrosis": Breast_fibrosis,
            "Breast_retraction": Breast_retraction,
            "Breast_necrosis": Breast_necrosis,
            "Breast_hematoma": Breast_hematoma,
            "Breast_infection": Breast_infection,
            "Breast_seroma": Breast_seroma,
            "Tumor_bed_fibrosis": Tumor_bed_fibrosis,
            "Tumor_bed_retraction": Tumor_bed_retraction,
            "Tumor_bed_necrosis": Tumor_bed_necrosis,
            "Tumor_bed_hematoma": Tumor_bed_hematoma,
            "Tumor_bed_infection": Tumor_bed_infection,
            "Tumor_bed_seroma": Tumor_bed_seroma,
            # Side Effects - Others
            "Pneumonitis": Pneumonitis,
            "Esophagitis": Esophagitis,
            "Neuropathy": Neuropathy,
            "Fatigue": Fatigue,
            # Recurrence Details
            "Local_recurrence": local_recurrence,
            "Time_to_local_recurrence": st.session_state.time_to_local_recurrence if local_recurrence == "Yes" else "N/A",
            "Regional_recurrence": regional_recurrence,
            "Time_to_regional_recurrence": st.session_state.time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A",
            "Distant_recurrence": distant_recurrence,
            "Time_to_distant_recurrence": st.session_state.time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A",
        }
        save_data(data)
        st.success("Patient data has been successfully saved!")
