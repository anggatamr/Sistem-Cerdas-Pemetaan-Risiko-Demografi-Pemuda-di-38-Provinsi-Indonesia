import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

def process_and_cluster():
    print("Memulai Preprocessing dan Modeling...")
    
    # --- 1. MEMUAT DATA ---
    # Berdasarkan asumsi: Anda telah merapikan file dan kolom-kolomnya menjadi:
    # 'Provinsi', 'TPAK_Agustus', 'NEET', 'RLS_Total', 'APK_SMA', 'APK_PT'
    # Pada langkah praktisnya, Anda bisa memuat file satu per satu, misalnya:
    # df_tpak = pd.read_csv('tpak.csv')[['Provinsi', 'TPAK_Agustus']]
    # dst, lalu di-merge.
    # Untuk template script ini, kita buat mock-up muat dari satu CSV jika sudah disatukan otomatis:
    
    try:
        # 1. TPAK
        df_tpak = pd.read_csv('Persentase Angkatan Kerja Terhadap Penduduk Usia Kerja (TPAK) menurut Provinsi, 2025.csv', sep=';', skiprows=4, header=None, names=['Provinsi', 'TPAK_Februari', 'TPAK_Agustus'])
        df_tpak = df_tpak[['Provinsi', 'TPAK_Agustus']]
        df_tpak['Provinsi'] = df_tpak['Provinsi'].str.strip().str.upper()

        # 2. NEET
        df_neet = pd.read_csv('Percentage of Youth (Aged 15-24 Years) Not in Education, Employment or Training (NEET), 2025.csv', sep=';', skiprows=3, header=None, names=['Provinsi', 'NEET'])
        df_neet['Provinsi'] = df_neet['Provinsi'].str.strip().str.upper()

        # 3. RLS
        df_rls_raw = pd.read_csv('Rata-rata Lama Sekolah (RLS) menurut Jenis Kelamin, 2025.csv', sep=',', skiprows=4, header=None, names=['Provinsi_Kab', 'Laki', 'Perempuan'])
        df_rls = df_rls_raw[df_rls_raw['Provinsi_Kab'].str.isupper() & (df_rls_raw['Provinsi_Kab'] != 'INDONESIA')].copy()
        df_rls['Laki'] = pd.to_numeric(df_rls['Laki'], errors='coerce')
        df_rls['Perempuan'] = pd.to_numeric(df_rls['Perempuan'], errors='coerce')
        df_rls['RLS_Total'] = (df_rls['Laki'] + df_rls['Perempuan']) / 2
        df_rls = df_rls[['Provinsi_Kab', 'RLS_Total']].rename(columns={'Provinsi_Kab': 'Provinsi'})
        df_rls['Provinsi'] = df_rls['Provinsi'].str.strip().str.upper()

        # 4. APK SMA
        df_apk_sma = pd.read_csv('Angka Partisipasi Kasar (APK) Menurut Provinsi dan Jenjang Pendidikan, 2025.csv', sep=';', skiprows=4, header=None, names=['Provinsi', 'SD', 'SMP', 'APK_SMA'])
        df_apk_sma = df_apk_sma[['Provinsi', 'APK_SMA']]
        df_apk_sma['Provinsi'] = df_apk_sma['Provinsi'].str.strip().str.upper()

        # 5. APK PT
        df_apk_pt = pd.read_csv('Angka Partisipasi Kasar (APK) Perguruan Tinggi (PT) Menurut Provinsi, 2025.csv', sep=';', skiprows=3, header=None, names=['Provinsi', 'APK_PT'])
        df_apk_pt['Provinsi'] = df_apk_pt['Provinsi'].str.strip().str.upper()

        # Merge all
        df = df_tpak.merge(df_neet, on='Provinsi', how='inner')\
                    .merge(df_rls, on='Provinsi', how='inner')\
                    .merge(df_apk_sma, on='Provinsi', how='inner')\
                    .merge(df_apk_pt, on='Provinsi', how='inner')
        
        # Mengecualikan record 'INDONESIA'
        df = df[df['Provinsi'] != 'INDONESIA']
        df['Provinsi'] = df['Provinsi'].str.title()
        
        # Mengubah beberapa format khusus (misal "Dki Jakarta", "Di Yogyakarta")
        df['Provinsi'] = df['Provinsi'].replace({'Dki Jakarta': 'DKI Jakarta', 'Di Yogyakarta': 'DI Yogyakarta', 'D.I. Yogyakarta': 'DI Yogyakarta'})

        print(f"Data 38 Provinsi berhasil dimuat dan digabungkan. Jumlah provinsi yang sinkron: {len(df)}")
    except Exception as e:
        print(f"Gagal memuat file CSV asli: {e}")
        return # Mengakhiri operasi jika data gagal digabungkan

    # Pastikan tidak ada data kosong
    df = df.dropna()

    # --- 2. PREPROCESSING ---
    features = ['TPAK_Agustus', 'NEET', 'RLS_Total', 'APK_SMA', 'APK_PT']
    X = df[features]

    # Standarisasi Data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # --- 3. MODELING (K-MEANS CLUSTERING) ---
    # Mencari 3 Klaster
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    df['Cluster_ID'] = clusters

    # --- 4. PENENTUAN TINGKAT RISIKO ---
    # Risiko didefinisikan: Tingginya NEET dan Rendahnya TPAK, RLS, APK_SMA, APK_PT
    # Kita buat skor risiko pada cluster centroid
    # Nilai standar untuk pusat klaster
    centers = pd.DataFrame(kmeans.cluster_centers_, columns=features)
    
    # Hitung 'Risk Score' untuk setiap centroid (NEET - (TPAK + RLS + APK_SMA + APK_PT))
    # Semakin besar skor, semakin tinggi risiko
    centers['Risk_Score'] = centers['NEET'] - (centers['TPAK_Agustus'] + centers['RLS_Total'] + centers['APK_SMA'] + centers['APK_PT'])
    
    # Urutkan berdasarkan Risk_Score untuk memberikan label
    sorted_clusters = centers.sort_values(by='Risk_Score').index.tolist()
    
    # Mapping
    # Index 0 dari sorted_clusters -> Skor terkecil (Risiko Rendah)
    # Index 1 dari sorted_clusters -> Skor menengah (Risiko Sedang)
    # Index 2 dari sorted_clusters -> Skor terbesar (Risiko Tinggi)
    risk_mapping = {
        sorted_clusters[0]: 'Risiko Rendah',
        sorted_clusters[1]: 'Risiko Sedang',
        sorted_clusters[2]: 'Risiko Tinggi'
    }
    
    df['Kategori_Risiko'] = df['Cluster_ID'].map(risk_mapping)

    # --- 5. EKSPOR HASIL ---
    output_filename = 'data_clustered.csv'
    df.to_csv(output_filename, index=False)
    print(f"Modeling selesai! Data clustering disimpan di: {output_filename}")
    print(df[['Provinsi', 'Kategori_Risiko']])

if __name__ == "__main__":
    process_and_cluster()
