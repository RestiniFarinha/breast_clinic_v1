import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# File path for local storage
excel_file = "I:\Radiation Oncology Clinical Trials - 1\BREAST\Breast Registry\Breast_clinic.xlsx"

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
            "Histology", "Grade", "ER", "PR", "HER2", "Clinical Stage", "Pathological Stage", "Margins", "LVI", "Surgery", "Surgery_date",
            "Neoadjuvant_hormonal_therapy", "Neoadjuvant_systemic_treatment", "Neoadjuvant_systemic_treatment_type",
            "Adjuvant_systemic_treatment", "Adjuvant_systemic_treatment_type",
            "Laterality", "Volume - Left Breast", "Volume - Right Breast", "Fractionation",
            "Radiodermatitis", "Telangiectasia", "Breast_pain", "Cosmetic_outcome", "Breast_shrinkage", "Hyperpigmentation",
            "Lymphedema", "Surgery_for_cosmetics",
            "Breast_edema", "Breast_fibrosis", "Tumor_bed_fibrosis", "Tumor_bed_retraction", 
            "Pneumonitis", "Esophagitis", "Fatigue",
            "Local_recurrence", "Local Recurrence Definition", "Time_to_local_recurrence", "Regional_recurrence", "Regional Recurrence Definition", "Time_to_regional_recurrence",
            "Distant_recurrence", "Distant Recurrence Definition", "Time_to_distant_recurrence", "Cancer Related Death", "Death", "Time_to_death"
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
st.write("To get started, please follow the instructions below:")
st.write("1. Enter the MRN (Medical Record Number) of the patient and press Enter.")
st.write("If the patient was already included in the database, the existing data will be loaded.")
st.write("2. Fill in the required fields and click the 'Calculate' button to calculate the patient's age and treatment times.")
st.write("3. After the calculations are done, click the 'Save Information' button to store the patient data in the database.")
st.write("You must ALWAYS press calculate before saving the information.")
st.write("4. The saved data will be appended to the existing database for future reference.")

# Input for MRN
mrn = st.text_input("Enter MRN (Medical Record Number) and press Enter", key="mrn")

# Fetch existing patient data
patient_data = get_patient_data(mrn) if mrn else None

# Start the form
with st.form("patient_form", clear_on_submit=False):
    st.subheader("Patient Details")

    date_of_birth = st.date_input("Date of Birth",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Birth", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today(), min_value=datetime(1900, 1, 1).date(), max_value=datetime.today().date()
    )

    mrn = st.text_input("MRN (Medical Record Number)", value=mrn)

    last_radiotherapy_date = st.date_input("Date of Last Radiotherapy",
        value=datetime.strptime(safe_get(patient_data, "Date_of_Last_Radiotherapy", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    follow_up_date = st.date_input("Date of Follow-up",
        value=datetime.strptime(safe_get(patient_data, "Follow_up_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    Histology = st.multiselect("Histology", ["IDC", "ILC", "DCIS", "LCIS", "Other"],
       default=safe_get_list(patient_data, "Histology") if patient_data else []
    )

    ER = st.radio("ER", ["Negative", "Positive"], #unkown
        index=["Negative", "Positive"].index(safe_get(patient_data, "ER", "Negative")) if patient_data else 0
    )

    PR = st.radio("PR", ["Negative", "Positive"],
        index=["Negative", "Positive"].index(safe_get(patient_data, "PR", "Negative")) if patient_data else 0
    )

    HER2 = st.multiselect("HER 2",["Negative", "FISH Positive", "1+", "2+", "3+", "FISH Negative", "Other"],
        default=safe_get_list(patient_data, "HER2") if patient_data else []
    )


    Grade = st.selectbox("Grade", ["I", "II", "III"],
        index=["I", "II", "III"].index(safe_get(patient_data, "Grade", "I")) if patient_data else 0
    )

    Clinical_Stage = st.multiselect("Clinical Stage", ["cTx", "cTis", "cT1a", "cT1b", "cT1c", "cT2", "cT3", "cT4a","cT4b", "cT4c", "cT4d", "cN0", "cN1a", "cN1b", "cN1c", "cN2a", "cN2b", "cN3a", "cN3b", "cN3c", "M0", "M1"],
        default=safe_get_list(patient_data, "Clinical Stage") if patient_data else [] #Check if we can use selectbox instead of multiselect
    )

    Pathological_Stage = st.multiselect("Pathological Stage", ["pTx", "pTis", "pT1a", "pT1b", "pT1c", "pT2", "pT3", "pT4a","pT4b", "pT4c", "pT4d","pN0", "pN1a", "pN1b", "pN1c", "pN2a", "pN2b", "pN3a", "pN3b", "pN3c", "M0", "M1"],
        default=safe_get_list(patient_data, "Pathological Stage") if patient_data else [] 
    )

    Margins = st.multiselect("Margins", ["Negative", "Positive", "<1mm", "1mm", "2mm", ">2mm", "Other"],
        default=safe_get_list(patient_data, "Margins") if patient_data else []
    )

    LVI = st.radio("LVI", ["Negative", "Positive", "Unknown"],
        index=["Negative", "Positive"].index(safe_get(patient_data, "PR", "Negative")) if patient_data else 0
    )

    Surgery = st.multiselect("Surgery", ["Total Mastectomy", "Partial mastectomy", "Skin sparing mastectomy", "Nipple sparing mastectomy", "Lumpectomy", "SLNB", "ALND", "Targeted axillary dissection", "Other"],
        default=safe_get_list(patient_data, "Surgery") if patient_data else []
    )

    Surgery_date = st.date_input("Date of Surgery",
        value=datetime.strptime(safe_get(patient_data, "Surgery_date", "1900-01-01"), "%Y-%m-%d").date() if patient_data else date.today()
    )

    # Systemic Treatment Change for Systemic treatment
    st.subheader("Systemic Treatment")
    Neoadjuvant_hormonal_therapy = st.radio("Neoadjuvant Hormonal Therapy", ["No", "Yes"],
        index=["No", "Yes"].index(safe_get(patient_data, "Neoadjuvant_hormonal_therapy", "No")) if patient_data else 0
    )

    Neoadjuvant_systemic_treatment_type = st.multiselect("Neoadjuvant Systemic Treatment type", 
        ["None", "Chemotherapy", "CDK4/6 inhibitors", "Endocrine therapy", "Immunotherapy", "ADC", "Targeted Therapy", "PARP inhibitors", "Radioligand", "Other"],
        default=safe_get_list(patient_data, "Neoadjuvant_systemic_treatment_type") if patient_data else []
    )

    Adjuvant_systemic_treatment_type = st.multiselect("Adjuvant Systemic Treatment type", 
        ["None", "Chemotherapy", "CDK4/6 inhibitors", "Endocrine therapy", "Immunotherapy", "ADC", "Targeted Therapy", "PARP inhibitors", "Radioligand", "Other"],
        default=safe_get_list(patient_data, "Adjuvant_systemic_treatment_type") if patient_data else []
    )

    # Treatment Details - Separate Section according to laterallity and volume (volumne / boost - dosimetry)
    st.subheader("Treatment Details")
    Laterallity = st.selectbox("Laterality", ["Left", "Right", "Bilateral"],
        index=["Left", "Right", "Bilateral"].index(safe_get(patient_data, "Laterality", "Left")) if patient_data else 0
    )
    st.warning(" If bilateral please fill in the details for both breasts separately.")
    Volume_left = st.selectbox(
        "Volume - Left Breast",
        ["Whole Breast", "Partial Breast", "Locorregional Breast", "Chest wall", "Locorregional chest wall","Not treated"],
        index=["Whole Breast", "Partial Breast", "Locorregional Breast", "Chest wall", "Locorregional chest wall"].index(
            safe_get(patient_data, "Volume_left", "Whole Breast")) if patient_data else 0
    )
    Volume_right = st.selectbox(
        "Volume - Right Breast",
        ["Whole Breast", "Partial Breast", "Locorregional Breast", "Chest wall", "Locorregional chest wall","Not treated"],
        index=["Whole Breast", "Partial Breast", "Locorregional Breast", "Chest wall", "Locorregional chest wall"].index(
            safe_get(patient_data, "Volume_right", "Whole Breast")) if patient_data else 0
    )

    Fractionation = st.multiselect("Fractionation", 
        ["26Gy", "30Gy SIB", "27Gy SIB", "28Gy SIB", "31Gy SIB", "40Gy", "10Gy sequential boost", "5.2Gy sequential boost", "27.5Gy/28.5Gy weekly", "Other"],
        default=safe_get_list(patient_data, "Fractionation") if patient_data else []
    )

    #Include the Dose and Fractionation

    st.markdown("<hr style='border:3px solid gray'>", unsafe_allow_html=True)

    # Side effects - Cosmesis - EORTC or CTCAE and version
    st.subheader("Side Effects - Cosmesis")
    radiodermatitis = st.radio("Radiodermatitis (EORTC)", ["None", "I", "II", "III", "IV"])
    with st.expander("Radiodermatitis Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Faint erythema or dry desquamation")
        st.write("Grade II: Moderate to brisk erythema; patchy moist desquamation, moderate edema")
        st.write("Grade III: Confluent, moist desquamation other than skin folds, pitting edema")
        st.write("Grade IV: Ulceration, hemorrhage, necrosis")

    telangiectasia = st.radio("Telangiectasia (EORTC)", ["None", "I", "II", "III"])
    with st.expander("Telangiectasia Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Few scattered Telangiectasia")
        st.write("Grade II: Moderate Telangiectasia")
        st.write("Grade III: Many confluent Telangiectasia")

    Hyperpigmentation = st.radio("Hyperpigmentation (CTCAE v5)", ["None", "I", "II"])
    with st.expander("Hyperpigmentation Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: <10 percent of treated skin area and without psychosocial impact")
        st.write("Grade II: >10 percent of treated skin area or with psychosocial impact")
 

    Lymphedema = st.radio("Lymphedema (CTCAE v5)", ["None", "I", "II", "III"])
    with st.expander("Lymphedema Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: trace thickening")
        st.write("Grade II: Marked discoloration; leathery skin texture; papillary formation; limiting instrumental ADL")
        st.write("Grade III: Severe symptoms; limiting self care ADL")


    # Side effects - Breast and Tumor Bed
    st.subheader("Side Effects - Breast and Tumor Bed")
    breast_shrinkage = st.radio("Breast Shrinkage", ["No", "Yes"])

    breast_pain = st.radio("Breast Pain (EORTC)", ["None", "I", "II", "III"])
    with st.expander("Breast Pain Classification"):
        st.write("Grade 0: No pain")
        st.write("Grade I: Mild pain; non-narcotic analgesics indicated")
        st.write("Grade II: Moderate pain; narcotic analgesics indicated")
        st.write("Grade III: Severe pain; limiting self care ADL")   

    Breast_edema = st.radio("Breast Edema (EORTC)", ["None", "I", "II", "III"])
    with st.expander("Breast Edema Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Minimal edema")
        st.write("Grade II: Moderate edema with peau d'orange appearance")
        st.write("Grade III: Severe edema of breast and nipple")

    Breast_fibrosis = st.radio("Breast Fibrosis (EORTC)", ["None", "I", "II", "III"])
    with st.expander("Breast Fibrosis Classification"):
        st.write("Grade 0: No change")  
        st.write("Grade I: Increased density in palpation")
        st.write("Grade II: Moderate impairment of function but not limiting self care ADL")
        st.write("Grade III: Severe fibrosis with interference with self care ADL and marked density")

    Tumor_bed_fibrosis = st.radio("Tumor Bed Fibrosis (EORTC)", ["None", "I", "II", "III"])
    with st.expander("Tumor Bed Fibrosis Classification"):
        st.write("Grade 0: No change")  
        st.write("Grade I: Increased density in palpation")
        st.write("Grade II: Moderate impairment of function but not limiting self care ADL")
        st.write("Grade III: Severe fibrosis with interference with self care ADL and marked density")

    Tumor_bed_retraction = st.radio("Tumor Bed Retraction", ["No", "Yes"])

    surgery_for_cosmetics = st.radio("Surgery for Cosmetic Correction", ["No", "Yes"])
    cosmetic_outcome = st.radio("Cosmetic Outcome", ["Excellent", "Good", "Fair", "Poor"])

    # Side effects - Others
    st.subheader("Side Effects - Other")
    Pneumonitis = st.radio("Pneumonitis (EORTC)", ["None", "I", "II", "III", "IV", "V"])
    with st.expander("Pneumonitis Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; medical intervention indicated but not limiting instrumental ADL")
        st.write("Grade III: Severe symptoms; limiting self care ADL, O2 indicated")
        st.write("Grade IV: Life-threatening respiratory compromise; urgent intervention indicated")
        st.write("Grade V: Death")

    Esophagitis = st.radio("Esophagitis (CTCAE v5)", ["None", "I", "II", "III", "IV", "V"])
    with st.expander("Esophagitis Classification"):
        st.write("Grade 0: No change")
        st.write("Grade I: Asymptomatic; clinical or diagnostic observations only; intervention not indicated")
        st.write("Grade II: Symptomatic; altered eating/swallowing; oral supplements indicated ")
        st.write("Grade III: Severely altered eating/swallowing; tube feeding, TPN, or hospitalization indicated")
        st.write("Grade IV: Life-threatening consequences; urgent operative intervention indicated")
        st.write("Grade V: Death")

    Fatigue = st.radio("Fatigue (EORTC)", ["None", "I", "II", "III"])
    with st.expander("Fatigue Classification"):
        st.write("Grade 0: No fatigue")
        st.write("Grade I: Mild fatigue; no change in activity")
        st.write("Grade II: Moderate fatigue; limiting instrumental ADL")
        st.write("Grade III: Severe fatigue; limiting self care ADL")

    # Recurrence details
    st.subheader("Recurrence Details")
    local_recurrence = st.radio("Local Recurrence", ["No", "Yes"])
    regional_recurrence = st.radio("Regional Recurrence", ["No", "Yes"])
    distant_recurrence = st.radio("Distant Recurrence", ["No", "Yes"])
    death = st.radio("Death", ["No", "Yes"])

    time_to_local_recurrence = None
    if local_recurrence == "Yes":
        local_recurrence_definition = st.multiselect("Local Recurrence Definition", ["Tumor Bed Recurrence", "Another Quadrant", "Same Quadrant", "Chest wall"])
        time_to_local_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Local Recurrence"))

    time_to_regional_recurrence = None 
    if regional_recurrence == "Yes":
        regional_recurrence_definition = st.multiselect("Regional Recurrence Definition", ["Axillary", "Supraclavicular", "Internal mammary"])
        time_to_regional_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Regional Recurrence"))

    time_to_distant_recurrence = None 
    if distant_recurrence == "Yes":
        distant_recurrence_definition = st.multiselect("Distant Recurrence Definition", ["Bone", "Liver", "Lung", "Brain", "Other"])
        time_to_distant_recurrence = calculate_months(last_radiotherapy_date, st.date_input("Date of Distant Recurrence"))

    death_date = None
    if death == "Yes":
        Cancer_related_death = st.radio("Cancer Related Death", ["No", "Yes"])
        time_to_death = calculate_months(last_radiotherapy_date, st.date_input("Date of Death"))

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
        st.session_state.time_to_death = time_to_death if death == "Yes" else "N/A"

        st.subheader("Calculated Results:")
        st.write(f"**Calculated Age**: {st.session_state.age} years")
        st.write(f"**Time since last radiotherapy**: {st.session_state.time_since_treatment} months")
        if local_recurrence == "Yes":
            st.write(f"**Time to local recurrence**: {st.session_state.time_to_local_recurrence} months")
        if regional_recurrence == "Yes":
            st.write(f"**Time to regional recurrence**: {st.session_state.time_to_regional_recurrence} months")
        if distant_recurrence == "Yes":
            st.write(f"**Time to distant recurrence**: {st.session_state.time_to_distant_recurrence} months")
        if death == "Yes":
            st.write(f"**Time to death**: {st.session_state.time_to_death} months")

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
            "Clinical Stage": Clinical_Stage,
            "Pathological Stage": Pathological_Stage,
            "Margins": Margins,
            "LVI": LVI,
            # Surgery
            "Surgery": Surgery,
            "Surgery_date": Surgery_date.strftime("%Y-%m-%d"),
            # Systemic Treatment
            "Neoadjuvant_hormonal_therapy": Neoadjuvant_hormonal_therapy,
            "Neoadjuvant_systemic_treatment_type": Neoadjuvant_systemic_treatment_type,
            "Adjuvant_systemic_treatment_type": Adjuvant_systemic_treatment_type,
            # Treatment Details
            "Laterality": Laterallity,
            "Volume - Left Breast": Volume_left,
            "Volume - Right Breast": Volume_right,
            "Fractionation": Fractionation,
            # Side Effects - Cosmesis
            "Radiodermatitis": radiodermatitis,
            "Telangiectasia": telangiectasia,
            "Hyperpigmentation": Hyperpigmentation,
            "Lymphedema": Lymphedema,
            # Side Effects - Breast and Tumor Bed
            "Breast_shrinkage": breast_shrinkage,
            "Breast_pain": breast_pain,
            "Breast_edema": Breast_edema,
            "Breast_fibrosis": Breast_fibrosis,
            "Tumor_bed_fibrosis": Tumor_bed_fibrosis,
            "Tumor_bed_retraction": Tumor_bed_retraction,
            "Surgery_for_cosmetics": surgery_for_cosmetics,
            "Cosmetic_outcome": cosmetic_outcome,
            # Side Effects - Others
            "Pneumonitis": Pneumonitis,
            "Esophagitis": Esophagitis,
            "Fatigue": Fatigue,
            # Recurrence Details
            "Local_recurrence": local_recurrence,
            "Local Recurrence Definition": local_recurrence_definition if local_recurrence == "Yes" else "N/A",
            "Time_to_local_recurrence": st.session_state.time_to_local_recurrence if local_recurrence == "Yes" else "N/A",
            "Regional_recurrence": regional_recurrence,
            "Regional Recurrence Definition": regional_recurrence_definition if regional_recurrence == "Yes" else "N/A",
            "Time_to_regional_recurrence": st.session_state.time_to_regional_recurrence if regional_recurrence == "Yes" else "N/A",
            "Distant_recurrence": distant_recurrence,
            "Distant Recurrence Definition": distant_recurrence_definition if distant_recurrence == "Yes" else "N/A",
            "Time_to_distant_recurrence": st.session_state.time_to_distant_recurrence if distant_recurrence == "Yes" else "N/A",
            "Cancer Related Death": Cancer_related_death if death == "Yes" else "N/A",
            "Death": death,
            "time_to_death": st.session_state.time_to_death if death == "Yes" else "N/A",
        }
        save_data(data)
        st.success("Patient data has been successfully saved!")
