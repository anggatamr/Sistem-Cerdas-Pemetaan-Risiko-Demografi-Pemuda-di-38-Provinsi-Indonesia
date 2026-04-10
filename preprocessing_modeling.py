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
        # Load the combined data if you made it into one, OR change these lines to read multiple CSVs
        # Example for multiple files:
        df_tpak = pd.read_csv('TPAK_clean.csv', sep=';') # sesuaikan separator
        df_neet = pd.read_csv('NEET_clean.csv', sep=';')
        df_rls = pd.read_csv('RLS_clean.csv', sep=';')
        df_apk_sma = pd.read_csv('APK_SMA_clean.csv', sep=';')
        df_apk_pt = pd.read_csv('APK_PT_clean.csv', sep=';')
        
        # Merge all dataframes based on 'Provinsi'
        df = df_tpak.merge(df_neet, on='Provinsi', how='inner')\
                    .merge(df_rls, on='Provinsi', how='inner')\
                    .merge(df_apk_sma, on='Provinsi', how='inner')\
                    .merge(df_apk_pt, on='Provinsi', how='inner')
        
        print("Data berhasil dimuat dan digabungkan.")
    except Exception as e:
        print(f"Data belum tersedia dalam format yang dirapikan. Error: {e}")
        print(">> Membuat dummy data agar pipeline tetap berjalan untuk testing...")
        # Dummy data untuk keperluan testing jika file CSV belum disesuaikan
        data = {
            'Provinsi': ['Aceh', 'Sumatera Utara', 'Jakarta', 'Papua', 'Jawa Timur', 'Nusa Tenggara Timur'],
            'TPAK_Agustus': [65.2, 68.1, 72.5, 60.1, 70.2, 62.5],
            'NEET': [24.5, 17.4, 12.8, 26.3, 16.7, 22.1],
            'RLS_Total': [9.2, 9.5, 11.2, 7.1, 9.8, 8.0],
            'APK_SMA': [85.1, 86.2, 98.1, 65.2, 88.5, 70.1],
            'APK_PT': [30.1, 32.5, 55.4, 15.2, 35.1, 18.5]
        }
        df = pd.DataFrame(data)

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
