
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Adaptasi Sektor Manufaktur terhadap Energi Bersih",
    page_icon="⚡",
    layout="wide"
)

# =========================
# DATA
# =========================
energy_df = pd.DataFrame({
    "Sektor": [
        "Industri, Konstruksi & Pertambangan",
        "Rumah Tangga",
        "Transportasi"
    ],
    2020: [2.37, 1.53, 0.87],
    2021: [2.69, 1.58, 0.89],
    2022: [3.84, 1.55, 0.95],
    2023: [4.16, 1.61, 1.01],
    2024: [4.52, 1.66, 1.05]
})

bauran_df = pd.DataFrame({
    "Jenis Energi": ["Batubara","Minyak Bumi","Gas Bumi","Energi Baru Terbarukan (EBT)"],
    "Porsi": [40.46,30.18,16.28,13.09]
})

listrik_df = pd.DataFrame({
    "Tahun":[2019,2020,2022,2023,2024],
    "kWh":[1084,1089,1173,1337,1411]
})

gap_df = pd.DataFrame({
    "Tahun":["2022","2023","2024"],
    "Realisasi":[12.3,13.09,13.8],
    "Target":[15.7,17.87,19.5],
    "Gap":[3.4,4.78,5.7]
})

rekom_df = pd.DataFrame({
    "Rekomendasi":[
        "Percepat PLTS Atap Industri",
        "ISO 50001",
        "PPA Energi Terbarukan",
        "TKDN Komponen EBT",
        "Green Hydrogen",
        "Regulasi Emisi Industri"
    ],
    "Horizon":[
        "Jangka Pendek",
        "Jangka Pendek",
        "Jangka Menengah",
        "Jangka Menengah",
        "Jangka Panjang",
        "Jangka Panjang"
    ],
    "Prioritas":["★★★","★★★","★★☆","★★☆","★☆☆","★☆☆"]
})

# =========================
# HEADER
# =========================
st.title("⚡ Adaptasi Sektor Manufaktur terhadap Penggunaan Energi Bersih")
st.markdown(
    "Dashboard interaktif untuk mengeksplorasi konsumsi energi, perkembangan EBT, gap target nasional, dan strategi adaptasi sektor manufaktur."
)

col1,col2,col3,col4,col5 = st.columns(5)

col1.metric("Energi Industri 2024","4.52 JT")
col2.metric("Pertumbuhan 2020-2024","+90.7%")
col3.metric("EBT 2023","13.09%")
col4.metric("Target EBT 2025","23%")
col5.metric("Gap Target","9.91 ppt")

tab1,tab2,tab3,tab4 = st.tabs([
    "📈 Konsumsi Energi",
    "🌱 Bauran Energi & EBT",
    "🎯 Gap & Strategi",
    "📖 Storytelling"
])

# =========================
# TAB 1
# =========================
with tab1:
    st.subheader("Konsumsi Energi per Sektor")

    long_df = energy_df.melt(
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

    st.plotly_chart(fig, use_container_width=True)

    year = st.slider(
        "Pilih Tahun",
        2020,
        2024,
        2024
    )

    selected = energy_df[["Sektor", year]]

    fig2 = px.bar(
        selected,
        x="Sektor",
        y=year,
        text=year
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.info(
        "Konsumsi energi sektor industri meningkat hampir dua kali lipat dari 2020 ke 2024 dan menjadi penyerap energi terbesar nasional."
    )

# =========================
# TAB 2
# =========================
with tab2:

    c1,c2 = st.columns([1,1])

    with c1:
        fig3 = px.pie(
            bauran_df,
            values="Porsi",
            names="Jenis Energi",
            hole=0.55
        )
        st.plotly_chart(fig3, use_container_width=True)

    with c2:
        fig4 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=13.09,
            title={"text":"Progress Menuju Target EBT 23%"},
            gauge={
                "axis":{"range":[0,23]}
            }
        ))
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Konsumsi Listrik per Kapita")

    fig5 = px.line(
        listrik_df,
        x="Tahun",
        y="kWh",
        markers=True
    )

    st.plotly_chart(fig5, use_container_width=True)

# =========================
# TAB 3
# =========================
with tab3:

    st.subheader("Gap Target EBT")

    fig6 = go.Figure()

    fig6.add_bar(
        name="Realisasi",
        x=gap_df["Tahun"],
        y=gap_df["Realisasi"]
    )

    fig6.add_bar(
        name="Target",
        x=gap_df["Tahun"],
        y=gap_df["Target"]
    )

    fig6.update_layout(barmode="group")

    st.plotly_chart(fig6, use_container_width=True)

    fig7 = px.line(
        gap_df,
        x="Tahun",
        y="Gap",
        markers=True
    )

    st.plotly_chart(fig7, use_container_width=True)

    st.subheader("Rekomendasi Kebijakan")

    horizon = st.selectbox(
        "Filter Horizon",
        ["Semua"] + list(rekom_df["Horizon"].unique())
    )

    if horizon == "Semua":
        filtered = rekom_df
    else:
        filtered = rekom_df[rekom_df["Horizon"] == horizon]

    st.dataframe(filtered, use_container_width=True)

# =========================
# TAB 4
# =========================
with tab4:

    st.markdown("## Babak 1 — Masalah")
    st.warning(
        "Konsumsi energi sektor industri meningkat dari 2.37 juta TJ menjadi 4.52 juta TJ dalam empat tahun."
    )

    st.markdown("## Babak 2 — Perjalanan")
    st.success(
        "Audit energi industri, biodiesel B35, dan adopsi PLTS Atap mulai mendorong efisiensi energi nasional."
    )

    st.markdown("## Babak 3 — Tantangan")
    st.error(
        "Bauran EBT 2023 masih 13.09%, jauh di bawah target nasional 17.87% dan target 23% pada 2025."
    )

    st.markdown("## Babak 4 — Solusi")

    col1,col2,col3 = st.columns(3)

    with col1:
        st.metric("PLTS Atap Industri","Prioritas Tinggi")

    with col2:
        st.metric("ISO 50001","Prioritas Tinggi")

    with col3:
        st.metric("Green Hydrogen","Jangka Panjang")

    st.markdown("---")
    st.markdown(
        """
        ### Kesimpulan
        
        Adaptasi manufaktur terhadap energi bersih merupakan langkah strategis
        untuk menjaga daya saing industri sekaligus mendukung target transisi energi nasional.
        """
    )
