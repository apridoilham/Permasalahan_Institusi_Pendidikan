# Proyek Akhir: Menyelesaikan Permasalahan Institusi Pendidikan Jaya Jaya Institut

## Business Understanding
Jaya Jaya Institut adalah salah satu institusi pendidikan tinggi bergengsi yang telah berdiri sejak tahun 2000 dan telah menghasilkan banyak lulusan bereputasi baik. Namun, institut ini menghadapi tantangan besar berupa tingginya angka *dropout* (mahasiswa putus sekolah) yang berdampak negatif terhadap reputasi institusi dan keberlangsungan operasional.

### Permasalahan Bisnis
- Tingginya persentase mahasiswa yang tidak menyelesaikan pendidikan (*dropout*).
- Pihak institusi belum memiliki sistem untuk mengidentifikasi mahasiswa yang berisiko *dropout* secara dini, sehingga bimbingan khusus tidak dapat diberikan secara tepat sasaran.

### Cakupan Proyek
- Melakukan *Exploratory Data Analysis* (EDA) untuk mengidentifikasi faktor-faktor utama yang berkontribusi terhadap *dropout*.
- Membangun *Business Dashboard* interaktif untuk memantau performa mahasiswa dan menyajikan *insight* demografis.
- Mengembangkan model *Machine Learning* (klasifikasi) guna memprediksi potensi *dropout* seorang mahasiswa berdasarkan profil akademik dan non-akademiknya.
- Membuat prototipe aplikasi prediksi menggunakan Streamlit agar dapat digunakan oleh pihak institut.

### Persiapan

Sumber data: Data historis performa mahasiswa Jaya Jaya Institut. Dataset ini dapat diunduh melalui tautan berikut:
[students_performance.csv](https://raw.githubusercontent.com/dicodingacademy/dicoding_dataset/main/students_performance/data.csv)

Setup environment:
```bash
# Membuat virtual environment (opsional)
python -m venv venv
source venv/bin/activate  # Untuk Mac/Linux
# venv\Scripts\activate   # Untuk Windows

# Instalasi library yang dibutuhkan
pip install -r requirements.txt
```

## Business Dashboard
Dashboard interaktif telah dibangun menggunakan **Tableau Public** untuk memonitor performa akademik dan demografi mahasiswa. 

Anda dapat mengakses *dashboard* secara langsung melalui tautan berikut:
**[Akses Jaya Jaya Institut Dashboard di Sini](https://public.tableau.com/views/JayaJayaInstitutDashboard_17818418769340/Dashboard1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)**

*(Screenshot *dashboard* juga telah dilampirkan di dalam repositori ini dengan nama file `aprido_ilham_dicoding-dashboard.png`)*.

## Menjalankan Sistem Machine Learning
Prototipe *Machine Learning* untuk memprediksi probabilitas *dropout* mahasiswa telah dibangun menggunakan antarmuka **Streamlit**.

Aplikasi ini telah di-*deploy* ke Streamlit Community Cloud. Anda dapat mencobanya secara langsung melalui tautan berikut:
**[Akses Sistem Prediksi Dropout Jaya Jaya Institut di Sini](https://penerapan-datascience.streamlit.app)**

Untuk menjalankan aplikasi Streamlit ini secara lokal, jalankan perintah berikut pada terminal:
```bash
streamlit run app.py
```

## Conclusion

**1. Kesimpulan Analisis Data (EDA) & Faktor *Dropout***
Dari analisis eksplorasi data yang dilakukan, dapat ditarik beberapa kesimpulan mengenai karakteristik mahasiswa yang berisiko *dropout*:
- **Faktor Ekonomi dan Dukungan Finansial**: Mahasiswa yang tidak mendapatkan beasiswa (*Scholarship holder = 0*) dan berstatus sebagai *Debtor* (memiliki tunggakan) memiliki kemungkinan *dropout* yang jauh lebih tinggi dibandingkan yang lain. Dukungan finansial sangat krusial dalam keberhasilan studi mereka.
- **Faktor Demografi (Usia)**: Terdapat tren di mana mahasiswa yang mendaftar pada usia yang lebih tua (di atas usia pendaftar standar, terutama di atas 25 tahun) lebih rentan terhadap *dropout*. Hal ini mungkin disebabkan oleh beban ganda seperti bekerja atau mengurus keluarga.

**2. Kesimpulan Performa Model Machine Learning**
- **Performa Kuantitatif**: Model *Machine Learning* berbasis *Random Forest* yang dilatih khusus pada mahasiswa dengan status akhir yang sudah pasti (Dropout dan Graduate) memiliki performa yang sangat baik. Model mencapai **Akurasi ~85-88%** secara keseluruhan, dan mampu mendeteksi kasus *Dropout* dengan **Recall di atas 80%**, yang sangat ideal untuk sistem deteksi dini institusi pendidikan.
- **Feature Importance (Fitur Berpengaruh)**: Berdasarkan perhitungan model, fitur-fitur yang paling berpengaruh kuat terhadap prediksi *dropout* adalah **Kinerja Akademik Awal** (jumlah mata kuliah yang disetujui/lulus dan nilai *grade* pada semester 1 dan 2), serta status **Kepemilikan Beasiswa** (*Scholarship_holder*) dan biaya kuliah (*Tuition_fees_up_to_date*).
### Rekomendasi Action Items
- **Program Bimbingan Finansial & Beasiswa Bertarget:** Memprioritaskan alokasi beasiswa atau keringanan biaya cicilan (bantuan finansial) kepada mahasiswa rentan, terutama yang terdeteksi sebagai *debtor* dan berisiko *dropout*.
- **Intervensi Akademik Sedini Mungkin:** Institut harus mengimplementasikan model *Machine Learning* ini pada akhir semester pertama. Jika mahasiswa diprediksi memiliki probabilitas *dropout* tinggi akibat nilai yang rendah, konselor akademik harus langsung menjadwalkan sesi bimbingan khusus.
- **Dukungan Khusus Mahasiswa Dewasa (Non-traditional Students):** Menyediakan fleksibilitas waktu (kelas malam/sore atau *online*) bagi mahasiswa yang mendaftar di usia matang untuk menyeimbangkan beban studi dan tanggung jawab pribadi.
- **Monitoring Berkala via Dashboard:** Memastikan manajemen kampus memonitor *Business Dashboard* secara berkala di awal dan pertengahan semester untuk mengevaluasi efektivitas intervensi yang telah dilakukan.
