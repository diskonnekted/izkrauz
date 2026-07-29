import streamlit as st
import geemap.foliumap as geemap
import ee

# 1. MENGATUR TAMPILAN HALAMAN WEB
st.set_page_config(page_title="Aplikasi GEE Gratis", layout="wide")
st.title("🌍 Peta Topografi Interaktif")
st.markdown("Ini adalah contoh aplikasi web gratis menggunakan Streamlit dan Google Earth Engine.")

# 2. INISIALISASI GOOGLE EARTH ENGINE
# Blok ini akan mencoba menghubungkan aplikasi Anda ke server Google.
# Jika di-deploy di cloud, pastikan kredensial (token) sudah diset di pengaturan server.
try:
    ee.Initialize()
except Exception as e:
    st.error("Gagal terhubung ke Earth Engine. Pastikan token autentikasi sudah diatur.")
    st.stop() # Menghentikan aplikasi jika gagal login ke Google

# 3. MEMBUAT LOGIKA PETA
def buat_peta():
    # Membuat kanvas peta (mengatur titik tengah di kordinat Indonesia dengan zoom level 5)
    peta = geemap.Map(center=[-2.5, 118.0], zoom=5)
    
    # Memanggil dataset elevasi digital (DEM SRTM) dari katalog server Google
    dataset_dem = ee.Image('USGS/SRTMGL1_003')
    
    # Mengatur parameter warna untuk ketinggian daratan
    parameter_visual = {
        'min': 0,      # Ketinggian minimal (permukaan laut)
        'max': 4000,   # Ketinggian maksimal (pegunungan tinggi)
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5'] # Warna: Hijau ke Putih/Salju
    }
    
    # Menambahkan layer elevasi tersebut ke dalam peta
    peta.addLayer(dataset_dem, parameter_visual, 'Elevasi (DEM)')
    
    return peta

# 4. MENAMPILKAN PETA DI APLIKASI WEB
peta_gee = buat_peta()
peta_gee.to_streamlit(height=600)