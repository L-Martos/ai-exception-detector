import pandas as pd
import streamlit as st

st.set_page_config(page_title="AI Exception Detector", layout="wide")
st.title("AI Exception Detector")
st.write("Upload a CSV file to analyze.")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

def detect_issues(df: pd.DataFrame) -> list[str]:
    issues: list[str] = []

    # 1) Missing values
    if df.isnull().any().any():
        missing_count = int(df.isnull().sum().sum())
        issues.append(f"⚠️ Missing values detected ({missing_count} total empty cells)")

    # 2) Duplicate encounter/claim id (if column exists)
    for id_col in ["encounter_id", "claim_id"]:
        if id_col in df.columns:
            dupes = int(df[id_col].duplicated().sum())
            if dupes > 0:
                issues.append(f"⚠️ {dupes} duplicate values found in '{id_col}'")

    # 3) Future dates check (try common date column names)
    date_candidates = ["charge_date", "claim_date", "date", "service_date"]
    date_col = next((c for c in date_candidates if c in df.columns), None)

    if date_col:
        parsed = pd.to_datetime(df[date_col], errors="coerce")
        bad_dates = int(parsed.isna().sum())
        if bad_dates > 0:
            issues.append(f"⚠️ {bad_dates} invalid dates found in '{date_col}' (could not parse)")

        future_dates = int((parsed > pd.Timestamp.today()).sum())
        if future_dates > 0:
            issues.append(f"⚠️ {future_dates} future '{date_col}' values detected")

    return issues

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("Preview of Data")
    st.dataframe(df.head(50), use_container_width=True)

    st.subheader("Detected Issues")
    issues = detect_issues(df)

    if issues:
        for issue in issues:
            st.warning(issue)
    else:
        st.success("✅ No obvious issues detected")
