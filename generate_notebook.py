import nbformat as nbf
from nbconvert.preprocessors import ExecutePreprocessor
import os

nb = nbf.v4.new_notebook()

# Metadata & Business Understanding
nb.cells.append(nbf.v4.new_markdown_cell("""# Proyek Akhir: Menyelesaikan Permasalahan Perusahaan Edutech

- **Nama:** Aprido Ilham
- **Email:** aprido233@gmail.com
- **Id Dicoding:** aprido_ilham

## 1. Business Understanding
Jaya Jaya Institut menghadapi tingginya persentase mahasiswa putus sekolah (*dropout*). Hal ini berdampak buruk bagi reputasi institut dan mengindikasikan adanya masalah yang tidak terdeteksi pada performa mahasiswa.

### Permasalahan Bisnis
- Tingkat *dropout* yang tinggi yang merugikan institusi pendidikan.
- Tidak adanya deteksi dini yang memadai sehingga bimbingan konseling dan akademik terlambat diberikan kepada mahasiswa yang berisiko.

### Cakupan Proyek
- **Eksplorasi Data (EDA):** Mengidentifikasi faktor dominan yang menyebabkan mahasiswa *dropout* (seperti usia, beasiswa, kondisi ekonomi).
- **Pemodelan Machine Learning:** Membuat model klasifikasi untuk memprediksi probabilitas *dropout* seorang mahasiswa.
- **Implementasi:** Mendeploy model ke dalam sebuah prototipe aplikasi berbasis Streamlit dan menyusun *Business Dashboard* untuk memonitor performa mahasiswa."""))

# Persiapan
nb.cells.append(nbf.v4.new_markdown_cell("""## 2. Persiapan

Tahap persiapan ini bertujuan untuk memuat pustaka (*libraries*) analitik standar dan melakukan *import* data.

### Menyiapkan library yang dibutuhkan"""))
code_imports = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

# Konfigurasi gaya visualisasi agar terlihat profesional (Prinsip Desain & Integritas Data)
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)"""
nb.cells.append(nbf.v4.new_code_cell(code_imports))

nb.cells.append(nbf.v4.new_markdown_cell("### Menyiapkan data yang akan digunakan"))
code_load = """# Membaca dataset
df = pd.read_csv('data.csv', sep=';')
df.head()"""
nb.cells.append(nbf.v4.new_code_cell(code_load))

# Data Understanding
nb.cells.append(nbf.v4.new_markdown_cell("""## 3. Data Understanding

Pada tahap ini, kita akan mengenali data secara menyeluruh. Kita memeriksa apakah ada *missing values*, melihat distribusi target (*Status*), dan mencari pola yang mungkin tersembunyi menggunakan visualisasi yang jelas dan mematuhi prinsip desain (konsistensi warna, pelabelan, dan kemudahan dibaca)."""))
code_eda = """# Informasi dataset dan cek missing values
print(df.info())
print("\\nMissing values:\\n", df.isnull().sum().sum())

# 1. Distribusi Target Variabel (Status)
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Status', palette='viridis')
plt.title('Distribusi Status Kelulusan Siswa', fontsize=14, fontweight='bold')
plt.ylabel('Jumlah Siswa')
plt.xlabel('Status Akhir')
plt.show()

# 2. Analisis Pengaruh Beasiswa terhadap Dropout
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='Scholarship_holder', hue='Status', palette='Set2')
plt.title('Proporsi Beasiswa vs Status Kelulusan', fontsize=14, fontweight='bold')
plt.xticks(ticks=[0, 1], labels=['Tanpa Beasiswa', 'Penerima Beasiswa'])
plt.ylabel('Jumlah Siswa')
plt.xlabel('Kepemilikan Beasiswa')
plt.legend(title='Status')
plt.show()

# 3. Distribusi Usia saat mendaftar
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x='Age_at_enrollment', hue='Status', multiple='stack', bins=25, palette='magma')
plt.title('Distribusi Usia Pendaftaran Berdasarkan Status', fontsize=14, fontweight='bold')
plt.ylabel('Jumlah Siswa')
plt.xlabel('Usia Saat Mendaftar')
plt.show()"""
nb.cells.append(nbf.v4.new_code_cell(code_eda))

# Data Preparation
nb.cells.append(nbf.v4.new_markdown_cell("""## 4. Data Preparation / Preprocessing

Karena tujuan institusi adalah mendeteksi "Dropout" sedini mungkin, kita akan mengubah klasifikasi ini menjadi *binary classification* (0 = Non-Dropout, 1 = Dropout).
Selain itu, kita memisahkan data latih dan data uji, serta melakukan *scaling* agar model tidak bias terhadap variabel dengan rentang nilai yang besar."""))
code_prep = """# Menyaring data: Hanya gunakan data dengan status Dropout dan Graduate (Hapus Enrolled)
df = df[df['Status'] != 'Enrolled']

# Mengubah target variabel menjadi biner (1: Dropout, 0: Graduate)
df['Target'] = df['Status'].apply(lambda x: 1 if x == 'Dropout' else 0)

# Memisahkan Fitur (X) dan Target (y)
X = df.drop(['Status', 'Target'], axis=1)
y = df['Target']

# Splitting data dengan proporsi 80% latih, 20% uji
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Scaling numerik (Standarisasi)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Menyimpan objek scaler untuk digunakan di app Streamlit
os.makedirs('model', exist_ok=True)
joblib.dump(scaler, 'model/scaler.pkl')
print("Scaler berhasil disimpan di 'model/scaler.pkl'")
"""
nb.cells.append(nbf.v4.new_code_cell(code_prep))

# Modeling
nb.cells.append(nbf.v4.new_markdown_cell("""## 5. Modeling

Model yang dipilih adalah **Random Forest Classifier**. Alasannya:
1. Sangat kuat menghadapi data tabular yang kompleks.
2. Dapat mengatasi *class imbalance* dengan parameter `class_weight='balanced'`.
3. Memiliki fitur `feature_importances_` bawaan yang membantu kita melihat fitur mana yang paling relevan dalam menentukan *dropout* mahasiswa."""))
code_model = """# Inisialisasi model Random Forest dengan class_weight balanced untuk menutupi ketidakseimbangan kelas
model = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')

# Melatih model
model.fit(X_train_scaled, y_train)

# Menyimpan model
joblib.dump(model, 'model/dropout_model.pkl')
print("Model berhasil dilatih dan disimpan di 'model/dropout_model.pkl'")
"""
nb.cells.append(nbf.v4.new_code_cell(code_model))

# Evaluation
nb.cells.append(nbf.v4.new_markdown_cell("""## 6. Evaluation

Kita mengukur kualitas model. Dalam deteksi dini, nilai **Recall** untuk kelas Dropout (1) sangat penting. Institut ingin memastikan sebanyak mungkin siswa berisiko *dropout* berhasil dideteksi."""))
code_eval = """# Prediksi pada data test
y_pred = model.predict(X_test_scaled)

# Menampilkan metrik utama
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\\nClassification Report:\\n", classification_report(y_test, y_pred))

# Confusion Matrix Visualisasi
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', cbar=False, 
            xticklabels=['Non-Dropout', 'Dropout'], yticklabels=['Non-Dropout', 'Dropout'])
plt.xlabel('Prediksi Model', fontsize=12)
plt.ylabel('Fakta Aktual', fontsize=12)
plt.title('Confusion Matrix Evaluasi', fontsize=14, fontweight='bold')
plt.show()

# Menampilkan Feature Importance
importances = model.feature_importances_
feature_names = X.columns
feature_importance_df = pd.DataFrame({'Feature': feature_names, 'Importance': importances}).sort_values(by='Importance', ascending=False)

plt.figure(figsize=(10, 8))
sns.barplot(x='Importance', y='Feature', data=feature_importance_df.head(15), palette='mako')
plt.title('Top 15 Faktor Utama Penentu Dropout (Feature Importance)', fontsize=14, fontweight='bold')
plt.xlabel('Tingkat Kepentingan')
plt.ylabel('Nama Fitur')
plt.show()
"""
nb.cells.append(nbf.v4.new_code_cell(code_eval))

# Menyimpan notebook
with open('notebook.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

# Eksekusi notebook
try:
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    with open('notebook.ipynb', 'r', encoding='utf-8') as f:
        nb_in = nbf.read(f, as_version=4)
    ep.preprocess(nb_in, {'metadata': {'path': './'}})
    with open('notebook.ipynb', 'w', encoding='utf-8') as f:
        nbf.write(nb_in, f)
    print("Notebook executed successfully.")
except Exception as e:
    print(f"Error executing notebook: {e}")
