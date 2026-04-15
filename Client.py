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


st.header("FAB Clients", divider='rainbow', anchor=False)

today = date.today()
cari_ay_ilk_gun = today.replace(day=1).isoformat()
cari_ay_bugun = today.isoformat()

kecen_il_cari_ay_ilk_gun = date(today.year-1, today.month, 1).isoformat()
kecen_il_cari_ay_sonu = date(today.year-1, today.month, calendar.monthrange(today.year-1, today.month)[1]).isoformat()

cari_il_ilk_gun = date(today.year, 1, 1).isoformat()

kecen_ay_sonu = (today.replace(day=1) - timedelta(days=1)).isoformat()

kecen_il_ilk_gun = date(date.today().year - 1, 1, 1).isoformat()
kecen_il_sonu  = date(date.today().year - 1, 12, 31).isoformat()

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

def musteriselect():
    with open("Musteriselect.sql", encoding="utf-8") as f:
        query = f.read().lstrip('\ufeff')

    return run_query(query)

def borc_cari_ay(anacari):
    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')
    query = f"""
        DECLARE @tarix1 DATE = '{cari_ay_ilk_gun}';
        DECLARE @tarix2 DATE = '{cari_ay_bugun}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def borc_cari_ay_2025(anacari):
    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')
    query = f"""
        DECLARE @tarix1 DATE = '{kecen_il_cari_ay_ilk_gun}';
        DECLARE @tarix2 DATE = '{kecen_il_cari_ay_sonu}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def borc_2026_medaxil(anacari):
    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')
    query = f"""
        DECLARE @tarix1 DATE = '{cari_il_ilk_gun}';
        DECLARE @tarix2 DATE = '{cari_ay_bugun}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def borc_2026_kecen_ay(anacari):
    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '{cari_il_ilk_gun}';
        DECLARE @tarix2 DATE = '{kecen_ay_sonu}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def borc_2025(anacari):
    with open("Borc.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '{kecen_il_ilk_gun}';
        DECLARE @tarix2 DATE = '{kecen_il_sonu}';
        DECLARE @anacari NVARCHAR(50) = '{anacari}';
        {query_text}
    """

    return run_query(query)

def qirmizi(anacari):
    with open("Qirmizi.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @Kod NVARCHAR(50) = '{anacari}';
        DECLARE @TarixOlmaz DATE = '{cari_ay_bugun}'
        {query_text}
    """

    return run_query(query)

def kateqoriya(anacari):
    with open("Kateqoriya.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = f"""
        DECLARE @tarix1 DATE = '{kecen_il_ilk_gun}'
        DECLARE @tarix2 DATE = '{cari_ay_bugun}'
        DECLARE @anacari NVARCHAR(50) = '{anacari}'

        {query_text}
    """

    return run_query(query)

def kateqoriyalar():
    with open("Kateqoriyalar.sql", encoding="utf-8") as f:
        query_text = f.read().lstrip('\ufeff')

    query = query_text

    return run_query(query)

def stok_satis(tarix1 = None, tarix2 = None, anacari = None):
    tarix_1 = tarix1 if tarix1 else kecen_il_ilk_gun
    tarix_2 = tarix2 if tarix2 else cari_ay_bugun

    query = f"""
        DECLARE @tarix1 DATE = '{tarix_1}'
        DECLARE @tarix2 DATE = '{tarix_2}'
        DECLARE @anacari NVARCHAR(50) = '{anacari}'
        SELECT * FROM [MikroDB_V16_05].[dbo].[BazarlamaSatishCariStok_MB_Cari]('2025-01-01','2026-12-31','120.R.1879')
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

def format_numeric_align(df: pd.DataFrame):
    numeric_cols = df.select_dtypes(include=["number"]).columns

    return (
        df.style
        .format({col: "{:,.0f}".format for col in numeric_cols})
        .set_properties(subset=numeric_cols, **{"text-align": "right"})
        .set_properties(subset=[c for c in df.columns if c not in numeric_cols],
                        **{"text-align": "left"})
    )

def add_total_row(df: pd.DataFrame, label="CƏM"):
    df = df.copy()

    numeric_cols = df.select_dtypes(include=["number"]).columns

    total = df[numeric_cols].sum(numeric_only=True)
    total_row = {col: "" for col in df.columns}
    total_row.update(total.to_dict())

    # index label row
    df.loc[label] = total_row

    return df

musteriselect_table = musteriselect()

filial_col, musteri_col, button_col = st.columns(3, vertical_alignment="bottom")

selected_filial = filial_col.selectbox(
    "Filial seçin",
    options=musteriselect_table["Filial"].dropna().unique(),
    key="filial"
)

filtered_df = musteriselect_table[musteriselect_table["Filial"] == selected_filial]

select_musteri = musteri_col.selectbox(
    "Müştəri seçin",
    options=(filtered_df["Ana"].astype(str) + " -- " + filtered_df["Ad"].astype(str)).dropna().unique(),
    key="musteri"
)

selected_musteri = select_musteri


show_button = button_col.button(
    "Göstər",
    use_container_width=True
)


if show_button:
    st.subheader(selected_filial + " -- " + selected_musteri, divider="gray", anchor=False)
    selected_kod = selected_musteri.split(" -- ")[0]
    selected_ad = selected_musteri.split(" -- ")[1]
    
    with st.spinner("Müştəri məlumatları yüklənir..."):
        musteriler_table = musteriler()

    base = musteriler_table[musteriler_table["Ana"] == selected_kod].copy()

    row = base.iloc[0]  # əsas məlumat

    # 🔷 DETAIL GRID
    d1 = st.expander("🗂️ Məlumat", expanded=False, key=None, icon=None, width="stretch")
    d2 = st.expander("🌐 Ünvan", expanded=False, key=None, icon=None, width="stretch")

    with d1:

        cols = st.columns(len(base))
        for col, (_, irow) in zip(cols, base.iterrows()):
            with col:
                qol_container = st.container(border=True, width="stretch", height="content", horizontal=False, horizontal_alignment="left", vertical_alignment="top", gap="small")
                qol_container.markdown(f"""
                <b>Kod:</b> {irow['Kod']}<br>
                <b>Təmsilçi kodu:</b> {irow['cari_temsilci_kodu']}<br>
                <b>Təmsilçi:</b><br>{irow['cari_per_adi']}<br>
                <b>Qol:</b> {irow['cari_sektor_kodu']}<br>
                <b>RUT Günü:</b> {int(irow['rut'])}
                """, unsafe_allow_html=True)

    # 🔷 MAP
    with d2:
        if row["adr_gps_enlem"] != 0 and row["adr_gps_boylam"] != 0:
            map_df = {
                "lat": [row["adr_gps_boylam"]],
                "lon": [row["adr_gps_enlem"]]
            }
            st.map(map_df, zoom=13, use_container_width=True)
        else:
            st.warning("GPS məlumatı yoxdur")

    st.subheader("Satış Məlumatları", divider="gray", anchor=False)
    with st.spinner("Məlumat yüklənir..."):
        try:
            # =========================
            # BORC_CARI_AY
            # =========================
            borc_ay = borc_cari_ay(selected_kod)[["CariKod", "Satis", "Son_Borc", "Medaxil"]]
            month_name = months_az[date.today().month]
            borc_ay = borc_ay.rename(columns={"Satis": f"2026 {month_name} Satış", "Son_Borc": f"{cari_ay_bugun} Borc", "Medaxil": f"2026 {month_name} Ödəniş"})

            base = base.merge(borc_ay, how="left", left_on="Kod", right_on="CariKod")
            base = base.drop(columns=["CariKod"])


            # =========================
            # BORC_CARI_AY_2025
            # =========================
            borc_2025_ay = borc_cari_ay_2025(selected_kod)[["CariKod", "Satis"]]
            borc_2025_ay = borc_2025_ay.rename(columns={"Satis": f"2025 {month_name} Satış"})

            base = base.merge(borc_2025_ay, how="left", left_on="Kod", right_on="CariKod")
            base = base.drop(columns=["CariKod"])


            # =========================
            # BORC_2025
            # =========================
            borc_2025_df = borc_2025(selected_kod)[["CariKod", "Satis", "Son_Borc"]]

            borc_2025_df = borc_2025_df.rename(columns={
                "Satis": "2025 Satış",
                "Son_Borc": f"{kecen_il_sonu} Borc"
            })

            base = base.merge(borc_2025_df, how="left", left_on="Kod", right_on="CariKod")
            base = base.drop(columns=["CariKod"])


            # =========================
            # BORC_2026
            # =========================
            borc_2026_df = borc_2026_kecen_ay(selected_kod)[["CariKod", "Satis", "Medaxil"]]
            month = date.today().month

            prev_month = 12 if month == 1 else month - 1
            borc_2026_df = borc_2026_df.rename(columns={"Satis": f"2026 {prev_month} ay Satış", "Medaxil": f"2026 {prev_month} ay Ödəniş"})

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
            base = base.rename(columns={
                "Alt": "Alt limit",
                "Ust": "Üst limit",
                "Qirmizi": "Qırmızı"
            })
            ordered_cols = [
                "Kod",
                "Alt limit",
                "Üst limit",
                f"{kecen_il_sonu} Borc",
                "2025 Satış",
                f"2025 {month_name} Satış",
                f"2026 {prev_month} ay Satış",
                f"2026 {prev_month} ay Ödəniş",
                f"2026 {month_name} Satış",
                f"2026 {month_name} Ödəniş",
                f"{cari_ay_bugun} Borc",
                "Qırmızı"
            ]

            base = base[[c for c in ordered_cols if c in base.columns]]
            base = base.set_index("Kod")
        except Exception as e:
            st.error(f"Xəta: {e}")
    
    base = add_total_row(base, "CƏM")
    st.table(format_numeric_align(base))

    st.subheader("Kateqoriya Satışları", divider="gray", anchor=False)
    with st.spinner("Məlumat yüklənir..."):
        try:    
            kateqoriya_satis = kateqoriya(selected_kod)
            kateqoriya_satis = kateqoriya_satis.set_index("MikroID")
        except Exception as e:
            st.error(f"Xəta: {e}")

    kateqoriya_satis = add_total_row(kateqoriya_satis, "CƏM")
    st.table(format_numeric_align(kateqoriya_satis))

else:
    pass