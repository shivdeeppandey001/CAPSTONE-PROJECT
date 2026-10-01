import streamlit as st
import os
from utils.data_processing import load_data
from utils.risk_engine import add_risk_analysis
from utils.recommendations import generate_recommendations

st.set_page_config(page_title="Student Details", layout="wide")

# Determine dataset to use: prefer session_state value set in main app, else list data files
data_files = sorted([f for f in os.listdir("data") if f.lower().endswith('.csv')])
dataset = st.session_state.get('dataset') if 'dataset' in st.session_state else None
if dataset not in data_files:
	dataset = st.selectbox("Select dataset", data_files, index=0)
else:
	st.write(f"Using dataset: {dataset}")

df = add_risk_analysis(load_data(os.path.join("data", dataset)))

st.title("👨‍🎓 Student Performance Details")
search = st.text_input("Search student by name (partial)")
names = df['Name'].sort_values().unique()
if search:
	names = [n for n in names if search.lower() in n.lower()]
student = st.selectbox("Select student", names)
row = df[df['Name'] == student].iloc[0]
st.metric("Marks", f"{row['Marks']}/100")
st.metric("Attendance(%)", f"{row['Attendance(%)']}%")
st.metric("Logins", int(row['Logins']))
st.metric("Risk Score", f"{row['RiskScore']} ({row['RiskLevel']})")
st.subheader("Recommendations")
st.write(generate_recommendations(row))
