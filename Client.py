# streamlit_app.py
import streamlit as st
import pandas as pd
import warnings
from datetime import date
import requests

warnings.simplefilter("ignore")

# -----------------------------
# Query helpers
# -----------------------------
def hesabat_satis_gunluk():
    today = date.today()
    #tarix_1 = today.replace(day=1).isoformat()
    tarix_2 = today.isoformat()
    with open("Hesabat - Satis - Gunluk.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')
    query = f"""
        DECLARE @tarix1 DATE = '{tarix_2}';
        DECLARE @tarix2 DATE = '{tarix_2}';
        {query_text}
    """
    url = "http://81.17.83.210:1999/api/Metin/GetQueryTable"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    html_json = {
    "Query": query,
    "Kod": st.secrets["Kod"]
    }
    response = requests.get(url, json=html_json, headers=headers, verify=False)

    if response.status_code == 200:
        api_data = response.json()
        if api_data["Code"] == 0:
            df = api_data["Data"]
        else:
            print("API Error:", api_data["Message"])
    else:
        print("Error:", response.status_code, response.text)
        
    return pd.DataFrame(df)
