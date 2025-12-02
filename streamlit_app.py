[00.59, 3/12/2025] Bagus Yudhistira: import streamlit as st
import pandas as pd
import joblib
import numpy as np

# Load the trained model
# IMPORTANT: Pastikan 'linear_regression_model.pkl' ditempatkan dengan benar dan disimpan dengan joblib.
try:
    model = joblib.load('linear_regression_model.pkl')
except FileNotFoundError:
    st.error("Error: Model file 'linear_regression_model.pkl' not found. Please ensure it is in the same directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- BLOK DEBUGGING KRITIS: Mengambil kolom yang diharapkan dari model ---
# Karena error menunjukkan model mengharapkan *_0 dan *_1, kita ganti fallback column names.
if hasattr(model, 'feature_names_in_'):
    MODEL_EXPECTED_COLUMNS = list(model.feature_names_in_)
else:
    # Menggunakan nama kolom yang DITUNJUKKAN oleh error traceback (mental_health_history_1)
    MODEL_EXPECTED_COLUMNS = [
        'academic_performance',
        'study_load',
        'peer_pressure',
        'extracurricular_activities',
        'bullying',
        'mental_health_history_0',       # Diperkirakan untuk 'Tidak Ada'
        'mental_health_history_1'       # Diperkirakan untuk 'Ada'
    ]

# Mapping untuk konversi pilihan pengguna ke kolom dummy yang diharapkan model
DUMMY_COLUMN_MAPPING = {
    'Tidak Ada': 'mental_health_history_0',
    'Ada': 'mental_health_history_1'
}

# Streamlit app title
st.title('Prediksi Tingkat Stres Mahasiswa')
st.write('Aplikasi untuk memprediksi tingkat stres mahasiswa.')

# Sidebar for user inputs
st.sidebar.header('Input Parameter')

def user_input_features():
    # Sliders and selectbox for collecting user input
    academic_performance = st.sidebar.slider('Peforma Akademik (1=Rendah, 5=Tinggi)', 1, 5, 3)
    study_load = st.sidebar.slider('Beban Belajar (1=Ringan, 5=Berat)', 1, 5, 3)
    peer_pressure = st.sidebar.slider('Tekanan Teman (1=Rendah, 5=Tinggi)', 1, 5, 3) 
    extracurricular_activities = st.sidebar.slider('Kegiatan Ekstrakurikuler (1=Sedikit, 5=Banyak)', 1, 5, 3)
    bullying = st.sidebar.slider('Bullying (1=Tidak Ada, 5=Sering)', 1, 5, 3)
    mental_health_history = st.sidebar.selectbox('Riwayat Mental', ['Tidak Ada', 'Ada'])

    data = {
        'academic_performance': academic_performance,
        'study_load': study_load,
        'peer_pressure': peer_pressure,
        'extracurricular_activities': extracurricular_activities,
        'bullying': bullying,
        'mental_health_history': mental_health_history
    }
    # Return the data as a simple DataFrame for display purposes
    return pd.DataFrame(data, index=[0])

# Collect user input
df_input = user_input_features()

st.subheader('Parameter Input Pengguna:')
st.dataframe(df_input, use_container_width=True)


# --- Data Preparation for Prediction ---

# Create an empty DataFrame initialized with all zeros and the exact columns expected by the model
final_input_df = pd.DataFrame(np.zeros((1, len(MODEL_EXPECTED_COLUMNS))), columns=MODEL_EXPECTED_COLUMNS)

# Populate numerical features using the values from the user input DataFrame (df_input)
for col in ['academic_performance', 'study_load', 'peer_pressure', 'extracurricular_activities', 'bullying']:
    if col in final_input_df.columns:
        final_input_df[col] = df_input[col][0]

# Populate the one-hot encoded categorical feature

# --- LOGIKA PENYESUAIAN NAMA KOLOM DUMMY YANG TEPAT (MENGGUNAKAN _0 DAN _1) ---
mhh_value = df_input['mental_health_history'][0]
dummy_col_name = DUMMY_COLUMN_MAPPING.get(mhh_value)

# Set the relevant dummy variable to 1
if dummy_col_name and dummy_col_name in final_input_df.columns:
    final_input_df[dummy_col_name] = 1
else:
    # Tampilkan error jika tidak dapat menemukan kolom dummy, ini menandakan masalah serius pada model.pkl
    st.error(f"Peringatan: Tidak dapat mencocokkan kolom dummy untuk R…
[01.00, 3/12/2025] Bagus Yudhistira: ini app.py ku
[01.00, 3/12/2025] Bagus Yudhistira: coba kembangin dik
[01.00, 3/12/2025] Bagus Yudhistira: aku ga kuat meh turu sek
[01.02, 3/12/2025] Bagus Yudhistira: kata gemini suruh nyoba ganti model lain, coba dik
