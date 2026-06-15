import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Adaptasi Sektor Manufaktur terhadap Energi Bersih",
    page_icon="⚡",
    layout="wide"
)

# =====================================================
# LOAD DATA
# =====================================================

@st.cache_data
def load_data():

    file = "data.xlsx"

    konsumsi = pd.read_excel(
        file,
        sheet_name="Konsumsi energi per sektor"
    )

    bauran = pd.read_excel(
        file,
        sheet_name="Bauran energi primer"
    )

    listrik = pd.read_excel(
        file,
        sheet_name="Konsumsi listrik perkapita"
    )

    gap = pd.read_excel(
        file,
        sheet_name="Gap real & target bauran energi"
    )

    return konsumsi, bauran, listrik, gap


konsumsi, bauran, listrik, gap = load_data()

# =====================================================
# HEADER
# =====================================================

st.title(
    "⚡ Adaptasi Sektor Manufaktur terhadap Penggunaan Energi Bersih"
)

st.markdown(
    """
    Dashboard interaktif untuk mengeksplorasi perkembangan konsumsi energi,
    bauran energi nasional, dan tantangan transisi energi pada sektor manufaktur.
    """
)

# =====================================================
# KPI
# =====================================================

industri_2020 = konsumsi.loc[0, 2020]
industri_2024 = konsumsi.loc[0, 2024]

growth = (
    (industri_2024 - industri_2020)
    / industri_2020
    * 100
)

ebt = bauran.loc[
    bauran["Jenis Energi"].str.contains("EBT"),
    "Porsi (%)"
].values[0]

target = 23

gap_target = target - ebt

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Energi Industri 2024",
    f"{industri_2024:.2f}"
)

c2.metric(
    "Pertumbuhan Industri",
    f"{growth:.1f}%"
)

c3.metric(
    "Bauran EBT",
    f"{ebt:.2f}%"
)

c4.metric(
    "Gap Target 2025",
    f"{gap_target:.2f} ppt"
)

# =====================================================
# TABS
# =====================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📈 Konsumsi Energi",
    "🌱 Bauran Energi",
    "🎯 Gap Target",
    "📖 Storytelling"
])

# =====================================================
# TAB 1
# =====================================================

with tab1:

    st.subheader("Konsumsi Energi per Sektor")

    long_df = konsumsi.melt(
        id_vars="Sektor",
        var_name="Tahun",
        value_name="Konsumsi"
    )

    fig = px.line(
        long_df,
        x="Tahun",
        y="Konsumsi",
        color="Sektor",
        markers=True
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    tahun = st.select_slider(
        "Pilih Tahun",
        options=[2020, 2021, 2022, 2023, 2024],
        value=2024
    )

    fig2 = px.bar(
        konsumsi,
        x="Sektor",
        y=tahun,
        text=tahun
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# =====================================================
# TAB 2
# =====================================================

with tab2:

    col1, col2 = st.columns(2)

    with col1:

        fig3 = px.pie(
            bauran,
            names="Jenis Energi",
            values="Porsi (%)",
            hole=0.5
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    with col2:

        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=float(ebt),
                title={"text": "Progress EBT"},
                gauge={
                    "axis": {"range": [0, 23]}
                }
            )
        )

        st.plotly_chart(
            gauge,
            use_container_width=True
        )

    st.subheader(
        "Konsumsi Listrik per Kapita"
    )

    listrik_clean = listrik.copy()

    listrik_clean["kWh/Kapita"] = pd.to_numeric(
        listrik_clean["kWh/Kapita"],
        errors="coerce"
    )

    fig4 = px.line(
        listrik_clean,
        x="Tahun",
        y="kWh/Kapita",
        markers=True
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# =====================================================
# TAB 3
# =====================================================

with tab3:

    gap_clean = gap.iloc[:3].copy()

    gap_clean["Realisasi (%)"] = pd.to_numeric(
        gap_clean["Realisasi (%)"]
    )

    gap_clean["Target (%)"] = pd.to_numeric(
        gap_clean["Target (%)"]
    )

    fig5 = go.Figure()

    fig5.add_bar(
        name="Realisasi",
        x=gap_clean["Indikator"],
        y=gap_clean["Realisasi (%)"]
    )

    fig5.add_bar(
        name="Target",
        x=gap_clean["Indikator"],
        y=gap_clean["Target (%)"]
    )

    fig5.update_layout(
        barmode="group"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    fig6 = px.line(
        gap_clean,
        x="Indikator",
        y="Gap (ppt)",
        markers=True
    )

    st.plotly_chart(
        fig6,
        use_container_width=True
    )

# =====================================================
# TAB 4
# =====================================================

with tab4:

    st.header(
        "Perjalanan Adaptasi Manufaktur menuju Energi Bersih"
    )

    st.markdown(
        """
        ### 1. Konsumsi Energi Industri Terus Meningkat

        Konsumsi energi sektor industri meningkat dari
        **2.37** menjadi **4.52 juta TJ**
        dalam periode 2020–2024.

        ---
        
        ### 2. Energi Fosil Masih Dominan

        Bauran energi nasional masih didominasi
        batubara, minyak bumi, dan gas bumi.

        ---
        
        ### 3. Target EBT Belum Tercapai

        Realisasi EBT tahun 2023 baru mencapai
        **13.09%**, sementara target nasional
        sebesar **23%** pada tahun 2025.

        ---
        
        ### 4. Strategi Adaptasi

        - PLTS Atap Industri
        - ISO 50001
        - Power Purchase Agreement (PPA)
        - Green Hydrogen
        - Regulasi Emisi Industri
        """
    )