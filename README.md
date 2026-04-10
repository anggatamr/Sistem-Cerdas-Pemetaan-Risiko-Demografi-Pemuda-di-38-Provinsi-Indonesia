# Sistem Cerdas Pemetaan Risiko Demografi Pemuda di 38 Provinsi Indonesia

> **Tugas Mata Kuliah Big Data dan Data Mining**  
> Program Studi Statistika, Universitas Negeri Medan
>
> **Anggota Kelompok:**
> 1. Adi Gunawan
> 2. Angga Tamara
> 3. Era Evalin Tampubolon
> 4. Randy Obie
> 5. Rizky Rafiza Panjaitan

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white) 
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) 
![Scikit-Learn](https://img.shields.io/badge/scikit_learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)

## Deskripsi Singkat
Aplikasi ini adalah _decision support system_ (Sistem Pendukung Keputusan) yang dirancang untuk mengelompokkan dan memvisualisasikan tingkat risiko keberhasilan demografi-pendidikan pemuda pada 38 provinsi di Indonesia (BPS 2025). Menggunakan algoritma **K-Means Clustering**, program memetakan daerah ke dalam tiga kelas: **Risiko Rendah, Risiko Sedang, dan Risiko Tinggi** dengan meninjau tingkat TPAK, NEET, RLS, APK SMA, dan APK PT.

## Struktur File
* `preprocessing_modeling.py` - File inti untuk melakukan normalisasi data (StandardScaler) serta implementasi _Machine Learning_ (K-Means Clustering). Output dari file ini adalah `data_clustered.csv`.
* `app.py` - File utama _frontend web_ yang merender visualisasi grafis menggunakan framework Streamlit dan Plotly berdasarkan dataset hasil clustering.
* *CSV files* - Kumpulan dataset indikator BPS 2025 yang dipakai sebagai data input (seperti TPAK, NEET, RLS, APK SMA, dan APK PT).

## Cara Instalasi & Requirements

1. **Clone repository ini ke komputermu:**
   ```bash
   git clone https://github.com/USERNAME/repo-name.git
   cd repo-name
   ```

2. **Buat Virtual Environment (Sangat Disarankan):**
   ```bash
   python -m venv env
   # Windows
   env\Scripts\activate
   # Mac/Linux
   source env/bin/activate
   ```

3. **Install Requirements:**
   Jalankan perintah berikut untuk mengunduh package yang dibutuhkan:
   ```bash
   pip install pandas scikit-learn streamlit plotly
   ```

## Cara Menjalankan Aplikasi

**LANGKAH 1: Lakukan Modeling dan Penggabungan Data**  
Jalankan file ML guna membangun file `data_clustered.csv` terlebih dahulu:
```bash
python preprocessing_modeling.py
```
*(Apabila format kolom mu belum rapi, pastikan untuk menyesuaikan pembacaan csv di dalam script agar fiturnya konsisten: 'Provinsi', 'TPAK_Agustus', 'NEET', 'RLS_Total', 'APK_SMA', 'APK_PT')*

**LANGKAH 2: Jalankan Streamlit Server**  
Mulai antarmuka aplikasi dengan menjalankan Streamlit:
```bash
streamlit run app.py
```
Aplikasi akan secara otomatis terbuka di halaman web _browser_ bawaan (secara default di `http://localhost:8501`).

---
Dibuat sebagai bagian dari _End-to-End Assignment_ untuk analisis Big Data dengan luaran Hak Kekayaan Intelektual (HKI) berbasis SaaS Data Science tingkat Provinsi.
