import streamlit as st
import pandas as pd

# ==============================================================================
# 1. KONFIGURASI HALAMAN & THEME (iOS + ESTETIKA MELAYU-CINA / PERANAKAN)
# ==============================================================================
st.set_page_config(
    page_title="Generator Narasi RO - Melayu Cina iOS",
    page_icon="🏮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Perpaduan Warna Angpao Red, Hijau Zamrud Melayu, Emas & iOS Clean Glass
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Background Aplikasi - Neutral Soft Cream khas Canvas iOS */
    .stApp {
        background-color: #F9F8F6;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Plus Jakarta Sans", sans-serif;
    }

    /* Header Banner - Estetika Peranakan Melayu-Cina (Marun Angpao & Hijau Melayu dengan Aksen Emas) */
    .peranakan-header {
        background: linear-gradient(135deg, #7F1D1D 0%, #065F46 50%, #450A0A 100%);
        border-radius: 22px;
        padding: 30px 35px;
        color: #FFFFFF;
        box-shadow: 0 10px 30px rgba(127, 29, 29, 0.2);
        border: 1.5px solid #D4AF37;
        position: relative;
        overflow: hidden;
        margin-bottom: 28px;
    }

    /* Motif Garis List Emas Murni (Golden Lattice Trim) */
    .peranakan-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 6px;
        background: linear-gradient(90deg, #D4AF37 0%, #FEF08A 25%, #F59E0B 50%, #FDE047 75%, #D4AF37 100%);
    }
    .peranakan-header::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #D4AF37 0%, #FDE047 50%, #D4AF37 100%);
    }

    .peranakan-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0;
    }
    .peranakan-subtitle {
        font-size: 14px;
        color: #FEF3C7;
        margin-top: 8px;
        font-weight: 400;
    }

    /* Card Container - iOS Frosted Glass Aesthetic dengan Border Emas Tipis */
    .ios-card {
        background: rgba(255, 255, 255, 0.96);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 20px;
        border: 1px solid rgba(212, 175, 55, 0.3);
        padding: 24px 28px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .ios-card:hover {
        box-shadow: 0 8px 30px rgba(127, 29, 29, 0.08);
        border-color: #D4AF37;
        transform: translateY(-2px);
    }

    /* PERBAIKAN UTAMA: MATIKAN SCROLLBAR KETAT & WRAP TEKS SECARA STATIS */
    div[data-testid="stCodeBlock"] {
        overflow: hidden !important;
    }
    div[data-testid="stCodeBlock"] code, 
    div[data-testid="stCodeBlock"] pre {
        white-space: pre-wrap !important;
        word-break: break-word !important;
        overflow-x: hidden !important;
        overflow-y: hidden !important;
        overflow: hidden !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
        font-size: 14.5px !important;
        line-height: 1.75 !important;
        background-color: #FFFDF7 !important;
        color: #1F2937 !important;
        border-radius: 14px !important;
        border: 1px solid #E5E7EB !important;
        border-left: 5px solid #D4AF37 !important;
        padding: 18px 20px !important;
    }

    /* iOS Status Pill Badges */
    .ios-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: -0.2px;
    }
    .ios-badge-success { background-color: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; }
    .ios-badge-progress { background-color: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
    .ios-badge-empty { background-color: #FEF2F2; color: #991B1B; border: 1px solid #FCA5A5; }

    /* Custom Styling Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E5E7EB;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. HEADER UTAMA (MELAYU-CINA & IOS DESIGN)
# ==============================================================================
st.markdown("""
    <div class="peranakan-header">
        <div class="peranakan-title">
            <span>🏮</span> Generator Narasi Rincian Output (RO)
        </div>
        <div class="peranakan-subtitle">
            Sistem Otomasi Laporan Capaian Kinerja • Akulturasi Estetika Melayu-Cina & Antarmuka iOS
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SIDEBAR UPLOAD & KONTROL
# ==============================================================================
with st.sidebar:
    st.markdown("### 📱 Panel Pengunggahan")
    st.caption("Unggah file Excel `CAPUT` Anda untuk memproses narasi.")
    
    uploaded_file = st.file_uploader(
        "Pilih File Excel (.xlsx / .csv)", 
        type=['xlsx', 'xls', 'csv']
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Pengaturan Kolom Capaian")
    has_pcro = st.checkbox("Ambil angka PCRO & RVRO dari Excel", value=False)
    col_pcro_idx = 12
    col_rvro_idx = 13
    
    if has_pcro:
        col_pcro_idx = st.number_input("Indeks Kolom PCRO (Contoh: M = 12)", value=12, min_value=0)
        col_rvro_idx = st.number_input("Indeks Kolom RVRO (Contoh: N = 13)", value=13, min_value=0)

# =================================
