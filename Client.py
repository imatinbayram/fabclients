# streamlit_app.py
import calendar
import streamlit as st
import pandas as pd
import warnings
from datetime import date, datetime, timedelta

import requests

warnings.simplefilter("ignore")

st.set_page_config(
    page_title='FAB Clients',
    page_icon='logo.png',
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# FAB Clients \n Bu hesabat FAB şirkətlər qrupu üçün hazırlanmışdır."
    }
)

st.header("FAB Clients", divider='rainbow')

months_az = {
    1: "Yanvar",
    2: "Fevral",
    3: "Mart",
    4: "Aprel",
    5: "May",
    6: "İyun",
    7: "İyul",
    8: "Avqust",
    9: "Sentyabr",
    10: "Oktyabr",
    11: "Noyabr",
    12: "Dekabr"
}

# -----------------------------
# Query helpers
# -----------------------------

def run_query(query: str) -> pd.DataFrame:
    url = "http://81.17.83.210:1999/api/Metin/GetQueryTable"
    
    payload = {
        "Query": query,
        "Kod": "QVERTY"  # st.secrets["Kod"]
    }

    try:
        response = requests.get(url, json=payload, verify=False)

        if response.status_code != 200:
            st.error(f"HTTP Error: {response.status_code}")
            return pd.DataFrame()

        api_data = response.json()

        if api_data.get("Code") != 0:
            st.error(api_data.get("Message", "API error"))
            return pd.DataFrame()

        return pd.DataFrame(api_data.get("Data", []))

    except Exception as e:
        st.error(f"Connection error: {str(e)}")
        return pd.DataFrame()
    
def musteriler():
    with open("Musteriler.sql", encoding="utf-8") as f:
        query = f.read().lstrip('\ufeff')

    return run_query(query)
    
def borc_cari_ay(anacari):
    today = date.today()
    tarix_1 = today.replace(day=1).isoformat()
    tarix_2 = today.isoformat()

    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '{tarix_1}';
        DECLARE @tarix2 DATE = '{tarix_2}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def borc_cari_ay_2025(anacari):
    today = date.today()
    tarix_1 = date(today.year-1, today.month, 1).isoformat()
    tarix_2 = date(today.year-1, today.month, calendar.monthrange(today.year-1, today.month)[1]).isoformat()

    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '{tarix_1}';
        DECLARE @tarix2 DATE = '{tarix_2}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def borc_2026_medaxil(anacari):
    today = date.today()
    tarix_1 = '2026-01-01'
    tarix_2 = today.isoformat()

    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '{tarix_1}';
        DECLARE @tarix2 DATE = '{tarix_2}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def borc_2026(anacari):
    today = date.today()
    tarix_1 = '2026-01-01'
    tarix_2 = (today.replace(day=1) - timedelta(days=1)).isoformat()

    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '{tarix_1}';
        DECLARE @tarix2 DATE = '{tarix_2}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def borc_2025(anacari):
    today = date.today()
    tarix_1 = today.replace(day=1).isoformat()
    tarix_2 = today.isoformat()

    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '2025-01-01';
        DECLARE @tarix2 DATE = '2025-12-31';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def qirmizi(anacari):
    today = date.today()
    tarix_2 = today.isoformat()

    with open("Qirmizi.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @Kod NVARCHAR(50) = '{anacari}';
        DECLARE @TarixOlmaz DATE = '{tarix_2}'
        {query_text}
    """

    return run_query(query)

def kateqoriya(anacari):
    today = date.today()
    tarix_1 = '2026-01-01'
    tarix_2 = today.isoformat()

    with open("Kateqoriya.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '2025-01-01'
        DECLARE @tarix2 DATE = '{tarix_2}'
        DECLARE @anacari NVARCHAR(50) = '{anacari}'

        {query_text}
    """

    return run_query(query)

def format_as_int_table(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    #df = df.reset_index(drop=True)

    def fmt(x):
        if pd.isna(x):
            return ""

        if isinstance(x, (int, float)):
            val = round(x)  # 🔥 əsas hissə

            return f"{val:,}".replace(",", " ")

        return x

    for col in df.columns:
        if col != "cari_kod":
            df[col] = df[col].apply(fmt)

    return df

musteriler_table = musteriler()

selected_filial = st.selectbox(
    "Filial seçin",
    options=musteriler_table["Filial"].dropna().unique()
)

filtered_df = musteriler_table[musteriler_table["Filial"] == selected_filial]

if filtered_df.empty:
    st.warning("Müştəri tapılmadı")
else:
    selected_musteri = st.selectbox(
        "Müştəri seçin",
        options=(
            filtered_df["Ana"].astype(str) + " -- " + filtered_df["Ad"].astype(str)
            ).dropna().unique()
    )
    

    if selected_musteri:
        selected_kod = selected_musteri.split(" -- ")[0]
        selected_ad = selected_musteri.split(" -- ")[1]
        
        base = musteriler_table[musteriler_table["Ana"] == selected_kod].copy()


        # =========================
        # BORC_CARI_AY
        # =========================
        borc_ay = borc_cari_ay(selected_kod)[["CariKod", "Satis", "Son_Borc", "Medaxil"]]
        month_name = months_az[date.today().month]
        borc_ay = borc_ay.rename(columns={"Satis": f"2026 {month_name} Satis", "Son_Borc": f"2026 {month_name} Borc", "Medaxil": f"2026 {month_name} Medaxil"})

        base = base.merge(borc_ay, how="left", left_on="Kod", right_on="CariKod")
        base = base.drop(columns=["CariKod"])


        # =========================
        # BORC_CARI_AY_2025
        # =========================
        borc_2025_ay = borc_cari_ay_2025(selected_kod)[["CariKod", "Satis"]]
        borc_2025_ay = borc_2025_ay.rename(columns={"Satis": f"2025 {month_name} Satis"})

        base = base.merge(borc_2025_ay, how="left", left_on="Kod", right_on="CariKod")
        base = base.drop(columns=["CariKod"])


        # =========================
        # BORC_2025
        # =========================
        borc_2025_df = borc_2025(selected_kod)[["CariKod", "Satis", "Son_Borc"]]

        borc_2025_df = borc_2025_df.rename(columns={
            "Satis": "2025 Satis",
            "Son_Borc": "2025 Borc"
        })

        base = base.merge(borc_2025_df, how="left", left_on="Kod", right_on="CariKod")
        base = base.drop(columns=["CariKod"])


        # =========================
        # BORC_2026
        # =========================
        borc_2026_df = borc_2026(selected_kod)[["CariKod", "Satis"]]
        month = date.today().month

        prev_month = 12 if month == 1 else month - 1
        borc_2026_df = borc_2026_df.rename(columns={"Satis": f"2026 {prev_month} ay Satis"})

        base = base.merge(borc_2026_df, how="left", left_on="Kod", right_on="CariKod")
        base = base.drop(columns=["CariKod"])


        # =========================
        # QIRMIZI
        # =========================
        qirmizi_df = qirmizi(selected_kod)

        if qirmizi_df is None or qirmizi_df.empty:
            base["Qirmizi"] = 0
        else:
            qirmizi_df = qirmizi_df.rename(columns={"Q_Kod": "CariKod"})

            base = base.merge(
                qirmizi_df[["CariKod", "Qirmizi"]],
                how="left",
                left_on="Kod",
                right_on="CariKod"
            ).drop(columns=["CariKod"])

            base["Qirmizi"] = base["Qirmizi"].fillna(0)


        # =========================
        # OUTPUT
        # =========================
        ordered_cols = [
            "Kod",
            "2025 Borc",
            "2025 Satis",
            f"2025 {month_name} Satis",
            f"2026 {prev_month} ay Satis",
            f"2026 {month_name} Satis",
            f"2026 {month_name} Medaxil",
            f"2026 {month_name} Borc",
            "Qirmizi"
        ]

        # keep only existing columns safely
        base = base[[c for c in ordered_cols if c in base.columns]]
        base = base.set_index("Kod")         
        st.table(format_as_int_table(base))

        kateqoriya_satis = kateqoriya(selected_kod).set_index("MikroID")
        st.table(format_as_int_table(kateqoriya_satis))