import streamlit as st
import folium
from streamlit_folium import st_folium
import ee

# 1. MENGATUR TAMPILAN HALAMAN WEB
st.set_page_config(page_title="Aplikasi GEE Gratis", layout="wide")
st.title("🌍 Peta Topografi Interaktif")
st.markdown("Ini adalah contoh aplikasi web gratis menggunakan Streamlit dan Google Earth Engine.")

# 2. INISIALISASI GOOGLE EARTH ENGINE
try:
    ee.Initialize()
except Exception as e:
    st.error("Gagal terhubung ke Earth Engine. Pastikan token autentikasi sudah diatur.")
    st.stop()

# 3. MEMBUAT LOGIKA PETA
def buat_peta():
    # Membuat peta dengan folium (titik tengah di Indonesia, zoom level 5)
    peta = folium.Map(location=[-2.5, 118.0], zoom_start=5)

    # Memanggil dataset elevasi digital (DEM SRTM) dari server Google
    dataset_dem = ee.Image('USGS/SRTMGL1_003')

    # Parameter visualisasi
    parameter_visual = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
    }

    # Menambahkan layer elevasi ke peta
    peta.add_tile_layer(
        url=dataset_dem.toImageUrl(parameter_visual),
        name='Elevasi (DEM)'
    )

    return peta

# 4. MENAMPILKAN PETA DI APLIKASI WEB
peta_gee = buat_peta()
st_folium(peta_gee, height=600)
