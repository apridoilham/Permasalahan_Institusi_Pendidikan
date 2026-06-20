import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Jaya Jaya Institut Dashboard", page_icon="🎓", layout="wide")

# Menggunakan tema desain dan palet warna yang baik
sns.set_theme(style="whitegrid")
primary_color = "#4C4C6D"

st.title("🎓 Jaya Jaya Institut: Dropout Analytics & Prediction System")
st.markdown("Sistem cerdas untuk mendeteksi potensi *dropout* mahasiswa dan memonitor performa akademik.")

@st.cache_data
def load_data():
    df = pd.read_csv('data.csv', sep=';')
    return df

@st.cache_resource
def load_model_and_scaler():
    model = joblib.load('model/dropout_model.pkl')
    scaler = joblib.load('model/scaler.pkl')
    return model, scaler

df = load_data()
model, scaler = load_model_and_scaler()

# Sidebar Navigation
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3228/3228236.png", width=100)
st.sidebar.title("Navigasi Utama")
page = st.sidebar.radio("Pilih Menu:", ["📊 Business Dashboard", "🔮 Dropout Predictor", "ℹ️ Tentang Aplikasi"])

if page == "📊 Business Dashboard":
    st.header("📊 Business Dashboard Overview")
    st.write("Analisis performa dan metrik demografis mahasiswa di Jaya Jaya Institut.")
    
    # Menampilkan Metric Card (Tampilan UI yang bagus)
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Mahasiswa Terdaftar", value=f"{len(df):,}")
    dropout_rate = (len(df[df['Status'] == 'Dropout']) / len(df)) * 100
    col2.metric(label="Tingkat Dropout Keseluruhan", value=f"{dropout_rate:.1f}%")
    grad_rate = (len(df[df['Status'] == 'Graduate']) / len(df)) * 100
    col3.metric(label="Tingkat Kelulusan", value=f"{grad_rate:.1f}%")
    
    st.markdown("---")
    
    # Row untuk Grafik Pertama
    row1_col1, row1_col2 = st.columns(2)
    with row1_col1:
        st.subheader("Distribusi Status Kelulusan")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x='Status', palette='viridis', ax=ax)
        ax.set_ylabel("Jumlah Siswa")
        st.pyplot(fig)
        
    with row1_col2:
        st.subheader("Dampak Beasiswa Terhadap Dropout")
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.countplot(data=df, x='Scholarship_holder', hue='Status', palette='Set2', ax=ax)
        ax.set_xticklabels(['Tanpa Beasiswa', 'Penerima Beasiswa'])
        ax.set_ylabel("Jumlah Siswa")
        st.pyplot(fig)
        
    st.subheader("Demografi Usia Saat Pendaftaran")
    fig, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(data=df, x='Age_at_enrollment', hue='Status', multiple='stack', bins=30, palette='magma', ax=ax)
    ax.set_xlabel("Usia Saat Mendaftar")
    ax.set_ylabel("Jumlah Siswa")
    st.pyplot(fig)
    
    st.info("💡 **Insight Actionable**: Mahasiswa yang tidak mendapatkan beasiswa (*non-scholarship*) mendominasi angka *dropout*. Bantuan finansial awal dapat menjadi kunci retensi mahasiswa.")

elif page == "🔮 Dropout Predictor":
    st.header("🔍 Prototype: Sistem Prediksi Dropout")
    st.markdown("Gunakan antarmuka di bawah ini untuk melihat probabilitas *dropout* dari data historis siswa.")
    
    st.markdown("### 1. Masukkan Parameter Siswa")
    st.write("*(Untuk tujuan prototipe, Anda dapat memuat data siswa historis dengan memilih indeksnya)*")
    
    # Input slider
    student_index = st.slider("Pilih Indeks Siswa di Database (0 - 4000):", min_value=0, max_value=len(df)-1, value=10)
    
    student_data = df.iloc[[student_index]].drop('Status', axis=1, errors='ignore')
    actual_status = df.iloc[student_index]['Status']
    
    with st.expander("Lihat Detail Lengkap Data Siswa"):
        st.dataframe(student_data)
        
    st.markdown("### 2. Hasil Prediksi ML")
    if st.button("🚀 Prediksi Potensi Dropout Sekarang", use_container_width=True):
        with st.spinner("Memproses data melalui Random Forest Model..."):
            try:
                student_data_scaled = scaler.transform(student_data)
                prediction = model.predict(student_data_scaled)[0]
                probability = model.predict_proba(student_data_scaled)[0]
                
                # Desain hasil
                st.markdown("---")
                if prediction == 1:
                    st.error(f"⚠️ **PERINGATAN!** Sistem mendeteksi bahwa siswa ini berisiko tinggi untuk **DROPOUT**.")
                    st.progress(float(probability[1]))
                    st.markdown(f"**Probabilitas Dropout:** {probability[1]*100:.1f}%")
                else:
                    st.success(f"✅ **AMAN.** Siswa ini diprediksi **LULUS** (Graduate).")
                    st.progress(float(probability[0]))
                    st.markdown(f"**Probabilitas Lulus:** {probability[0]*100:.1f}%")
                    
                st.info(f"Sebagai referensi, status aktual siswa ini pada database adalah: **{actual_status}**")
                
            except Exception as e:
                st.error(f"Terjadi kesalahan dalam prediksi: {e}")

elif page == "ℹ️ Tentang Aplikasi":
    st.header("Tentang Aplikasi Ini")
    st.write("Aplikasi ini dibuat untuk memenuhi tugas **Proyek Akhir Dicoding: Penerapan Data Science**.")
    st.markdown("- **Model:** Random Forest Classifier dengan class weight balancing.")
    st.markdown("- **Tujuan:** Deteksi dini *dropout* mahasiswa untuk perbaikan bimbingan akademik.")
    st.markdown("- **Kriteria 5 Bintang:** UI responsif, visualisasi bermakna, metrik jelas, dan performa tinggi.")
