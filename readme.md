# STEAM GAME SUCCESS ANALYZER

## Sistem Analisis Prediksi Kesuksesan Game Steam Berbasis Machine Learning

---

## 1. Deskripsi Sistem

**Steam Game Success Analyzer** merupakan aplikasi berbasis **Streamlit** yang dikembangkan untuk menganalisis dan memprediksi potensi kesuksesan game pada platform Steam menggunakan pendekatan **Data Mining** dan **Machine Learning**.

Sistem mengimplementasikan:

* **Supervised Learning (Classification)** untuk memprediksi tingkat kesuksesan game.
* **Unsupervised Learning (Clustering)** untuk mengelompokkan game berdasarkan karakteristik tertentu.
* Visualisasi data interaktif untuk membantu interpretasi hasil analisis.

Proyek ini dibuat sebagai pemenuhan **Ujian Akhir Semester Mata Kuliah Data Mining**, Program Studi **Sistem Informasi, Universitas Negeri Surabaya**.

---

## 2. Identitas Kelompok

| Nama                           | NIM         |
| ------------------------------ | ----------- |
| Daniel Evan Rusli              | 24051214009 |
| Azzahra Anggarista Yoan Putri  | 24051214032 |
| Maria Elvaretta Cempaka Ayu S. | 24051214033 |

---

## 3. Struktur Direktori Project

```text
UAS_DataMining_Kelompok15/
│
├── app/
│   ├── pages/
│   │   ├── __pycache__/
│   │   ├── about.py
│   │   ├── dataset.py
│   │   ├── home.py
│   │   ├── prediction.py
│   │   └── visualization.py
│   │
│   └── app.py
│
├── data/
│   └── steam_games_clustered.zip
│
├── model/
│   ├── metadata.json
│   └── prediction_model.pkl
│
├── notebook/
│   └── analysis.ipynb
│
├── laporan/
│   └── Artikel KEL_15 UAS KELAS KDD-01.pdf
│
├── readme.md
├── requirements.txt
└── video.txt
```

---

## 4. Dataset

Dataset yang digunakan adalah **Steam Games Dataset** yang diperoleh dari HuggingFace dan telah melalui proses preprocessing untuk kebutuhan analisis serta pemodelan machine learning.

### Karakteristik Dataset

* Jumlah data: ±124.000 game
* Jumlah fitur: 41 atribut awal
* Rentang tahun rilis: 1997–2026
* Tidak terdapat missing value pada dataset utama
* Dataset telah melalui proses feature engineering dan clustering

### Lokasi Dataset

```text
data/steam_games_clustered.zip
```

---

## 5. Metodologi Penelitian

### 5.1 Data Preparation

Tahapan preprocessing yang dilakukan:

* Data Cleaning
* Feature Engineering
* One Hot Encoding
* Standardization (StandardScaler)
* Handling Imbalanced Data (SMOTE)

### 5.2 Supervised Learning

Model klasifikasi yang diuji:

* Gradient Boosting Classifier
* Random Forest Classifier
* Logistic Regression

### 5.3 Unsupervised Learning

Metode clustering yang digunakan:

* K-Means Clustering

---

## 6. Teknologi yang Digunakan

* Python 3.11
* Streamlit
* Pandas
* NumPy
* Scikit-learn
* Imbalanced-learn
* Plotly
* Matplotlib
* Joblib
* Jupyter Notebook

---

## 7. Fitur Aplikasi

### Home

Menampilkan informasi umum mengenai sistem dan tujuan penelitian.

### Dataset Overview

Menampilkan ringkasan dataset yang digunakan pada penelitian.

### Prediction System

Melakukan prediksi tingkat kesuksesan game berdasarkan fitur yang dimasukkan pengguna.

### Data Visualization

Menyediakan visualisasi interaktif untuk eksplorasi data dan hasil clustering.

### About

Berisi informasi mengenai penelitian, metode yang digunakan, dan anggota kelompok.

---

## 8. Hasil Evaluasi Model

| Model                        | AUC-ROC    |
| ---------------------------- | ---------- |
| Gradient Boosting Classifier | **0.8732** |
| Random Forest Classifier     | 0.8688     |
| Logistic Regression          | 0.7654     |

### Model Terbaik

**Gradient Boosting Classifier**

Karena menghasilkan nilai **AUC-ROC tertinggi sebesar 0.8732**, model ini digunakan sebagai model utama pada fitur prediksi aplikasi.

---

## 9. Cara Menjalankan Aplikasi

### 1. Download Repository

1. Buka repository GitHub.
2. Klik tombol **Code**.
3. Pilih **Download ZIP**.
4. Tunggu hingga proses download selesai.

### 2. Ekstrak File ZIP

Ekstrak file hasil download ke lokasi yang diinginkan.

Contoh:

```text
Downloads
└── UAS_DataMining_Kelompok15
    └── UAS_DataMining_Kelompok15
```

### 3. Buka Command Prompt (CMD)

Tekan:

```text
Windows + R
```

Ketik:

```text
cmd
```

Kemudian tekan **Enter**.

### 4. Masuk ke Folder Project

Sesuaikan dengan lokasi hasil ekstraksi.

Contoh:

```bash
cd C:\Users\ASUS\Downloads\UAS_DataMining_Kelompok15\UAS_DataMining_Kelompok15
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

Tunggu hingga seluruh library selesai terinstal.

### 6. Jalankan Aplikasi Streamlit

```bash
python -m streamlit run app/app.py
```

### 7. Buka Melalui Browser

Apabila browser tidak terbuka otomatis, buka:

```text
http://localhost:8501
```

---

## 10. Laporan Penelitian

Laporan lengkap penelitian dapat dilihat pada:

```text
laporan/laporan.pdf
```

Dokumen laporan memuat:

* Latar belakang penelitian
* Studi literatur
* Metodologi penelitian
* Data preparation
* Implementasi machine learning
* Evaluasi model
* Hasil dan pembahasan
* Kesimpulan

---

## 11. Catatan Penting

* Aplikasi dijalankan secara lokal menggunakan Streamlit.
* Dataset tersedia pada folder:

```text
data/steam_games_clustered.zip
```

* Dataset tidak perlu diekstrak secara manual.
* Model machine learning tersimpan pada folder `model`.
* Pastikan seluruh dependency pada `requirements.txt` telah terinstal sebelum menjalankan aplikasi.
* Disarankan menggunakan **Python 3.11** untuk kompatibilitas terbaik dengan seluruh library yang digunakan.

---

## 12. Kesimpulan

Steam Game Success Analyzer berhasil mengimplementasikan teknik Data Mining dan Machine Learning untuk menganalisis serta memprediksi tingkat kesuksesan game pada platform Steam.

Berdasarkan hasil evaluasi, **Gradient Boosting Classifier** menjadi model terbaik dengan nilai **AUC-ROC sebesar 0.8732**, sehingga digunakan sebagai model utama dalam sistem prediksi.

---

## Lisensi

Proyek ini dibuat untuk kebutuhan akademik pada Mata Kuliah **Data Mining**, Program Studi **Sistem Informasi**, Universitas Negeri Surabaya.

© 2026 Kelompok 15
