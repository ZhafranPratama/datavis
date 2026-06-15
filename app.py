import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Adaptasi Sektor Manufaktur terhadap Energi Bersih",
    page_icon="⚡",
    layout="wide"
)

# =====================================
# LOAD EXCEL
# =====================================
EXCEL_FILE = "infografis_energi_manufaktur.xlsx"

@st.cache_data
def load_excel():
    return pd.read_excel(
        EXCEL_FILE,
        sheet_name=None
    )

excel_data = load_excel()

# Melihat sheet yang tersedia
sheet_names = list(excel_data.keys())

st.sidebar.title("Navigasi")

selected_sheet = st.sidebar.selectbox(
    "Pilih Dataset",
    sheet_names
)

st.title("⚡ Adaptasi Sektor Manufaktur terhadap Energi Bersih")

# =====================================
# OVERVIEW
# =====================================

st.subheader("Preview Dataset")

df = excel_data[selected_sheet]

st.dataframe(df, use_container_width=True)

st.markdown("---")

# =====================================
# VISUALISASI DINAMIS
# =====================================

numeric_cols = df.select_dtypes(include="number").columns.tolist()

all_cols = df.columns.tolist()

if len(numeric_cols) > 0:

    st.subheader("Visualisasi Interaktif")

    x_col = st.selectbox(
        "Kolom X",
        all_cols
    )

    y_col = st.selectbox(
        "Kolom Y",
        numeric_cols
    )

    chart_type = st.radio(
        "Jenis Grafik",
        [
            "Line",
            "Bar",
            "Scatter"
        ],
        horizontal=True
    )

    if chart_type == "Line":
        fig = px.line(
            df,
            x=x_col,
            y=y_col,
            markers=True
        )

    elif chart_type == "Bar":
        fig = px.bar(
            df,
            x=x_col,
            y=y_col
        )

    else:
        fig = px.scatter(
            df,
            x=x_col,
            y=y_col
        )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================
# TAB KHUSUS
# =====================================

tab1, tab2, tab3, tab4 = st.tabs([
    "Konsumsi Energi",
    "EBT",
    "Gap Target",
    "Storytelling"
])

with tab1:
    st.write("Visualisasi konsumsi energi sektor manufaktur")

with tab2:
    st.write("Visualisasi bauran energi dan EBT")

with tab3:
    st.write("Visualisasi gap target EBT")

with tab4:
    st.write("Storytelling transisi energi sektor manufaktur")