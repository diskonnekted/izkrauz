import streamlit as st
import json
import folium
from streamlit_folium import st_folium
import ee

# 1. MENGATUR TAMPILAN HALAMAN WEB
st.set_page_config(page_title="Aplikasi GEE Gratis", layout="wide")
st.title("🌍 Peta Topografi Interaktif")
st.markdown("Ini adalah contoh aplikasi web gratis menggunakan Streamlit dan Google Earth Engine.")

# 2. INISIALISASI GOOGLE EARTH ENGINE
try:
    # Baca service account JSON dari Streamlit secrets
    credentials = ee.ServiceAccountCredentials(
        st.secrets['GEE']['email'],
        key_data=st.secrets['GEE']['json']
    )
    ee.Initialize(credentials=credentials)
except KeyError:
    st.error("Gagal terhubung ke Earth Engine. Pastikan secret `GEE` sudah diatur di Streamlit Cloud Settings.")
    st.markdown("**Cara menambahkan secret:**")
    st.markdown("1. Buka https://streamlit.io/cloud")
    st.markdown("2. Klik project **izkrauz** → tab **Settings**")
    st.markdown("3. Di section **Secrets**, tambahkan dengan format TOML:")
    st.code("""[GEE]
email = "gee-144@baranews.iam.gserviceaccount.com"
json = '''{
  "type": "service_account",
  "project_id": "baranews",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...",
  "client_email": "gee-144@baranews.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/gee-144%40baranews.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}'''
""", language="toml")
    st.stop()
except Exception as e:
    st.error(f"Gagal terhubung ke Earth Engine: {e}")
    st.stop()

# 3. MEMBUAT LOGIKA PETA
def buat_peta():
    # Memanggil dataset elevasi digital (DEM SRTM) dari server Google
    dataset_dem = ee.Image('USGS/SRTMGL1_003')

    # Parameter visualisasi
    parameter_visual = {
        'min': 0,
        'max': 4000,
        'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']
    }

    # Buat peta dengan folium (titik tengah di Indonesia, zoom level 5)
    peta = folium.Map(location=[-2.5, 118.0], zoom_start=5, tiles='OpenStreetMap')

    # Tambahkan layer GEE menggunakan getMapId + TileLayer
    map_id_dict = dataset_dem.getMapId(parameter_visual)
    mapid = map_id_dict.get('mapid', '')

    if mapid:
        # Gunakan token GEE untuk auth tile layer
        token = map_id_dict.get('token', '')
        image_id = mapid.split('/')[-1]
        tile_url = f'https://earthengine.googleapis.com/v1/projects/earthengine-legacy/images/{image_id}:tile?token={token}'

        folium.TileLayer(
            tiles=tile_url,
            name='Elevasi (DEM)',
            attr='Google Earth Engine'
        ).add_to(peta)

    # Layer control untuk switch antar layer
    folium.LayerControl().add_to(peta)

    return peta

# 4. MENAMPILKAN PETA DI APLIKASI WEB
peta_gee = buat_peta()
st_folium(peta_gee, height=600)
