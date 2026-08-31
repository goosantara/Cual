import streamlit as st
import pandas as pd
import io

# ==============================================================================
# 1. KONFIGURASI HALAMAN & THEME (iOS + KAIN CUAL BANGKA BELITUNG)
# ==============================================================================
st.set_page_config(
    page_title="Generator Narasi RO - Cual iOS Edition",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Kombinasi Estetika iOS (Clean Glassmorphism) & Motif Kain Cual Bangka Belitung (Emas & Marun)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Background Aplikasi - iOS Clean Neutral */
    .stApp {
        background-color: #F4F4F7;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Plus Jakarta Sans", sans-serif;
    }

    /* Header Banner - Motif Kain Cual Bangka Belitung (Marun & Emas) */
    .cual-header {
        background: linear-gradient(135deg, #4A0E17 0%, #7A1C36 50%, #1E293B 100%);
        border-radius: 22px;
        padding: 30px 35px;
        color: #FFFFFF;
        box-shadow: 0 10px 30px rgba(122, 28, 54, 0.2);
        border: 1px solid rgba(212, 175, 55, 0.4);
        position: relative;
        overflow: hidden;
        margin-bottom: 28px;
    }

    /* Motif Tenun Emas Cual Trim (Top & Bottom Border) */
    .cual-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 5px;
        background: repeat-x linear-gradient(90deg, #D4AF37 0%, #FDF0A6 25%, #D4AF37 50%, #B38F24 75%, #D4AF37 100%);
    }
    .cual-header::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 4px;
        background: repeat-x linear-gradient(90deg, #D4AF37 0%, #FDF0A6 50%, #D4AF37 100%);
    }

    .cual-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #FFFFFF;
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0;
    }
    .cual-subtitle {
        font-size: 14px;
        color: #E2E8F0;
        margin-top: 8px;
        font-weight: 400;
    }

    /* Card Container - iOS Frosted Glass Aesthetic */
    .ios-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 18px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        padding: 22px 26px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.03);
        transition: all 0.2s ease-in-out;
    }
    .ios-card:hover {
        box-shadow: 0 8px 25px rgba(122, 28, 54, 0.08);
        border-color: rgba(212, 175, 55, 0.4);
    }

    /* PERBAIKAN PENTING: Force Text Wrapping agar Narasi Tidak Scroll Samping */
    div[data-testid="stCodeBlock"] code, 
    div[data-testid="stCodeBlock"] pre {
        white-space: pre-wrap !important;
        word-break: break-word !important;
        overflow-x: hidden !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
        font-size: 14.5px !important;
        line-height: 1.65 !important;
        background-color: #F8FAFC !important;
        color: #0F172A !important;
        border-radius: 14px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 16px !important;
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
    .ios-badge-success { background-color: #E6F4EA; color: #137333; border: 1px solid #CEEAD6; }
    .ios-badge-progress { background-color: #E8F0FE; color: #1A73E8; border: 1px solid #D2E3FC; }
    .ios-badge-empty { background-color: #F1F3F4; color: #5F6368; border: 1px solid #E8EAED; }

    /* Custom Styling Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. HEADER UTAMA (CUAL & IOS DESIGN)
# ==============================================================================
st.markdown("""
    <div class="cual-header">
        <div class="cual-title">
            <span>🌸</span> Generator Narasi Capaian Rincian Output (RO)
        </div>
        <div class="cual-subtitle">
            Sistem Otomasi Penyusunan Laporan Capaian Kinerja • Motif Cual Bangka Belitung & iOS Interface
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SIDEBAR UPLOAD & KONTROL
# ==============================================================================
with st.sidebar:
    st.markdown("### 📱 Panel Pengunggahan")
    st.caption("Unggah file Excel `CAPUT` untuk memproses narasi secara otomatis.")
    
    uploaded_file = st.file_uploader(
        "Pilih File Excel (.xlsx / .csv)", 
        type=['xlsx', 'xls', 'csv']
