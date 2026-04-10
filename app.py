import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Sistem Pemetaan Risiko Demografi Pemuda", page_icon="📈", layout="wide")

# Inject Custom Font Jakarta Sans & Minimalist CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
    }
    
    /* Clean Minimalist Tweaks */
    [data-testid="stSidebar"] {
        border-right: 1px solid #EAEAEA;
        background-color: #FAFAFA !important;
    }
    [data-testid="stHeader"] {
        background-color: transparent;
    }
    .stDataFrame {
        border: 1px solid #EAEAEA;
        border-radius: 8px;
    }
    
    /* Override default colors */
    h1, h2, h3 {
        color: #111111 !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)

# a. Judul dan Deskripsi
st.title("Sistem Cerdas Pemetaan Risiko Demografi Pemuda di 38 Provinsi Indonesia")
st.markdown("""
Aplikasi ini menggunakan model *Machine Learning* **K-Means Clustering** untuk mengelompokkan 38 Provinsi di Indonesia menjadi tiga tingkat risiko demografis: **Risiko Rendah**, **Risiko Sedang**, dan **Risiko Tinggi**.

Variabel penentu klaster meliputi tingginya pengangguran usia muda (**NEET**) dan rendahnya pencapaian pendidikan/ketenagakerjaan (**APK**, **RLS**, dan **TPAK**).
""")

# Load Data (tanpa cache agar data klasterisasi 38 provinsi yang diperbarui bisa langsung tampil)
def load_data():
    try:
        # Load clustered data from output step 1
        df = pd.read_csv('data_clustered.csv')
    except Exception as e:
        df = pd.DataFrame()
    return df

df = load_data()

if df.empty:
    st.error("Terdapat error: Data `data_clustered.csv` tidak ditemukan. Pastikan Anda telah menjalankan file `preprocessing_modeling.py`.")
else:
    # d. Sidebar Interaktif Filter
    st.sidebar.header("Filter Dashboard")
    st.sidebar.write("Gunakan filter di bawah untuk menyesuaikan data.")
    
    # Filter Kategori (Opsional tambahan kenyamanan)
    selected_kategori = st.sidebar.multiselect(
        "Kategori Risiko:", 
        options=df['Kategori_Risiko'].unique(), 
        default=df['Kategori_Risiko'].unique()
    )
    
    # Filter Provinsi
    provinsi_list = df['Provinsi'].tolist()
    selected_prov = st.sidebar.multiselect(
        "Pilih Provinsi:", 
        options=provinsi_list, 
        default=provinsi_list
    )
    
    # Terapkan filter ke dataframe
    filtered_df = df[
        (df['Provinsi'].isin(selected_prov)) & 
        (df['Kategori_Risiko'].isin(selected_kategori))
    ]
    
    # Hitung jumlah klasifikasi dari data yang difilter
    st.sidebar.subheader("Ringkasan Hasil Tampil")
    count_data = filtered_df['Kategori_Risiko'].value_counts()
    for cat, count in count_data.items():
        st.sidebar.write(f"- {cat}: **{count} Provinsi**")

    # b. Tabel Data Gabungan Mentah
    st.subheader("Data Set (Hasil Analisis Klastering)")
    st.dataframe(filtered_df, use_container_width=True)
    
    st.divider()

    # c. Visualisasi (Scatter Plot & Bar Chart)
    color_map = {
        "Risiko Rendah": "#34C759", # Hijau Estetik Apple
        "Risiko Sedang": "#FFCC00", # Kuning Estetik Apple
        "Risiko Tinggi": "#FF3B30"  # Merah Estetik Apple
    }

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Scatter Plot: NEET vs APK Perguruan Tinggi")
        fig_scatter = px.scatter(
            filtered_df, 
            x="APK_PT", 
            y="NEET", 
            color="Kategori_Risiko", 
            size="RLS_Total",
            hover_name="Provinsi",
            color_discrete_map=color_map,
            title="Peta Sebaran Variabel Indikator",
            labels={"APK_PT": "APK Perguruan Tinggi (%)", "NEET": "Tingkat NEET Pemuda (%)"}
        )
        fig_scatter.update_layout(
            template="plotly_white", 
            font=dict(family="Plus Jakarta Sans", color="#333333"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    with col2:
        st.subheader("Bar Chart: Rataan Skor Risiko per Kategori")
        # Mengagregasi data berdasarkan kategori risiko untuk bar chart
        agg_df = df.groupby('Kategori_Risiko')[['RLS_Total', 'APK_SMA']].mean().reset_index()
        # Mengubah data dari wide ke long format untuk group bar chart
        agg_melted = agg_df.melt(id_vars='Kategori_Risiko', var_name='Indikator', value_name='Rata-Rata Angka')
        
        fig_bar = px.bar(
            agg_melted, 
            x="Kategori_Risiko", 
            y="Rata-Rata Angka", 
            color="Indikator", 
            barmode="group",
            title="Perbandingan Rata-rata Variabel per Kategori (Seluruh Data)",
            labels={"Kategori_Risiko": "Tingkat Risiko"}
        )
        fig_bar.update_layout(
            template="plotly_white", 
            font=dict(family="Plus Jakarta Sans", color="#333333"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(title_font_family="Plus Jakarta Sans", font=dict(family="Plus Jakarta Sans", color="#333333")),
            margin=dict(l=20, r=20, t=50, b=20)
        )
        # Menyesuaikan palet warna bar chart agar lebih estetik dan minimalis
        fig_bar.update_traces(marker_line_width=0)
        st.plotly_chart(fig_bar, use_container_width=True)
