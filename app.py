import streamlit as st
import pandas as pd

st.title("AI Exception Detector")
st.write("Upload a CSV file to analyze.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ✅ Preview section (this is what you’re missing right now)
    st.subheader("Preview of Data")
    st.dataframe(df.head())

    # ✅ Detect issues
    st.subheader("Detected Issues")
    issues = []

    # Missing values check
    if df.isnull().any().any():
        issues.append("⚠️ Missing values detected")

    # Duplicate encounter check
    if "encounter_id" in df.columns:
        duplicates = df["encounter_id"].duplicated().sum()
        if duplicates > 0:
            issues.append(f"⚠️ {duplicates} duplicate encounters found")

    # Future date check (works for charge_date OR claim_date)
    date_col = None
    if "charge_date" in df.columns:
        date_col = "charge_date"
    elif "claim_date" in df.columns:
        date_col = "claim_date"

    if date_col:
        df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
        future_dates = (df[date_col] > pd.Timestamp.today()).sum()
        if future_dates > 0:
            issues.append(f"⚠️ {future_dates} future {date_col} values detected")

    # Show results
    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("✅ No obvious issues detected")
