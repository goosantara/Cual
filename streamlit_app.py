import streamlit as st
import pandas as pd
import base64
import os

# ==============================================================================
# 0. FUNGSI PEMBANTU UNTUK MEMUAT LOGO CUAL (BASE64)
# ==============================================================================
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    return ""

# Pastikan gambar "logo_cual.jpg" berada di folder yang sama dengan app.py
logo_b64 = get_base64_image("logo_cual.jpg")

if logo_b64:
    logo_header_html = f'<img src="data:image/jpeg;base64,{logo_b64}" style="width: 48px; height: 48px; border-radius: 12px; object-fit: cover; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">'
    logo_sidebar_html = f'<div style="text-align: center; margin-bottom: 22px;"><img src="data:image/jpeg;base64,{logo_b64}" style="width: 110px; border-radius: 16px; box-shadow: 0 6px 16px rgba(0,0,0,0.12);"></div>'
else:
    # Default emoji jika file gambar tidak ditemukan
    logo_header_html = '🐴'
    logo_sidebar_html = ''

# ==============================================================================
# 1. KONFIGURASI HALAMAN & THEME (iOS 26 Glassmorphism Transparent Edition)
# ==============================================================================
st.set_page_config(
    page_title="iOS Vision Narasi RO",
    page_icon="🐴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Ultra-Modern iOS Glassmorphism, Text Wrap & Jarak Baris Rapat
st.markdown("""
    <style>
    /* Background Animasi Mesh/Liquid */
    .stApp {
        background: radial-gradient(circle at 15% 50%, #D1FAE5 0%, transparent 50%),
                    radial-gradient(circle at 85% 30%, #FEF3C7 0%, transparent 50%),
                    radial-gradient(circle at 50% 80%, #E0F2FE 0%, transparent 50%);
        background-color: #F8FAFC;
        background-attachment: fixed;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Plus Jakarta Sans", sans-serif;
    }

    /* Kustomisasi Wrapper Accordion / Expander */
    [data-testid="stExpander"] {
        background: rgba(255, 255, 255, 0.45) !important;
        backdrop-filter: blur(24px) saturate(200%) !important;
        -webkit-backdrop-filter: blur(24px) saturate(200%) !important;
        border: 1px solid rgba(255, 255, 255, 0.8) !important;
        border-radius: 20px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.04) !important;
        margin-bottom: 14px !important;
        overflow: hidden !important;
        transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1) !important;
    }
    [data-testid="stExpander"]:hover {
        background: rgba(255, 255, 255, 0.7) !important;
        box-shadow: 0 12px 35px 0 rgba(0, 0, 0, 0.07) !important;
        transform: translateY(-2px);
    }
    
    /* Header pada Expander Buka-Tutup */
    [data-testid="stExpander"] summary {
        padding: 16px 22px !important;
        border-radius: 20px !important;
    }
    [data-testid="stExpander"] summary p {
        font-weight: 700 !important;
        font-size: 15px !important;
        color: #0F172A !important;
        display: flex;
        align-items: center;
    }
    
    /* Container/Ruang Dalam Expander */
    [data-testid="stExpanderDetails"] {
        padding: 0px 20px 18px 20px !important;
    }

    /* Header Panel Kaca Utama (Atas) */
    .glass-header {
        background: rgba(255, 255, 255, 0.35);
        backdrop-filter: blur(30px) saturate(180%);
        -webkit-backdrop-filter: blur(30px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.7);
        border-radius: 26px;
        padding: 26px 36px;
        color: #0F172A;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
        margin-bottom: 24px;
    }
    .glass-title {
        font-size: 30px;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin: 0 0 8px 0;
        background: linear-gradient(90deg, #047857, #D97706);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .glass-subtitle {
        font-size: 14px;
        color: #475569;
        font-weight: 500;
    }

    /* Text Wrap Otomatis (Tanpa Scroll Samping) & Jarak Baris Rapat */
    div[data-testid="stCodeBlock"] {
        background: rgba(255, 255, 255, 0.65) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        border: 1px solid rgba(255, 255, 255, 0.85) !important;
        padding: 2px !important;
        box-shadow: inset 0 1px 3px rgba(0,0,0,0.02) !important;
        margin-bottom: 12px !important;
    }
    div[data-testid="stCodeBlock"] pre {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        word-break: break-word !important;
        overflow-x: hidden !important;
        margin: 0 !important;
        padding: 14px !important;
    }
    div[data-testid="stCodeBlock"] code {
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
        word-break: break-word !important;
        overflow-x: hidden !important;
        background: transparent !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
        font-size: 14px !important;
        line-height: 1.38 !important;
        color: #1E293B !important;
    }

    /* Kustomisasi Text Area Komen */
    div[data-baseweb="textarea"] {
        border-radius: 12px !important;
        background-color: rgba(255, 255, 255, 0.8) !important;
        border: 1px solid #CBD5E1 !important;
    }

    /* Status Badges */
    .ios-badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 30px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-left: 10px;
    }
    .ios-badge-success { background: rgba(16, 185, 129, 0.15); color: #047857; border: 1px solid rgba(16, 185, 129, 0.3); }
    .ios-badge-progress { background: rgba(245, 158, 11, 0.15); color: #B45309; border: 1px solid rgba(245, 158, 11, 0.3); }
    .ios-badge-empty { background: rgba(100, 116, 139, 0.15); color: #475569; border: 1px solid rgba(100, 116, 139, 0.3); }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. HEADER UTAMA (GLASSMORPHISM + LOGO CUAL)
# ==============================================================================
st.markdown(f"""
    <div class="glass-header">
        <div style="display: flex; align-items: center; margin-bottom: 8px;">
            <div style="margin-right: 14px; display: flex; align-items: center; justify-content: center; font-size: 32px;">
                {logo_header_html}
            </div>
            <h1 class="glass-title" style="margin: 0;">Automasi Capaian Rincian Output (RO)</h1>
        </div>
        <div class="glass-subtitle">
            Selamat Datang Tuan Muda Egoo, Awali Hari dengan Bismillah...
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SIDEBAR UPLOAD & KONTROL (+ LOGO CUAL)
# ==============================================================================
with st.sidebar:
    if logo_sidebar_html:
        st.markdown(logo_sidebar_html, unsafe_allow_html=True)
        
    st.markdown("### 📱 Panel Pengunggahan")
    uploaded_file = st.file_uploader(
        "Pilih File Excel (.xlsx / .csv)", 
        type=['xlsx', 'xls', 'csv']
    )
    
    st.markdown("---")
    st.markdown("### 🗓️ Pengaturan Waktu")
    selected_month = st.selectbox(
        "Bulan Laporan",
        ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"],
        index=1 # Default index 1 adalah Januari
    )
    selected_year = st.text_input("Tahun Laporan", value="2026")

    st.markdown("---")
    st.markdown("### ⚙️ Pengaturan Kolom Capaian")
    has_pcro = st.checkbox("Ambil angka PCRO & RVRO dari Excel", value=False)
    col_pcro_idx = 12
    col_rvro_idx = 13
    
    if has_pcro:
        col_pcro_idx = st.number_input("Indeks Kolom PCRO (Contoh: M = 12)", value=12, min_value=0)
        col_rvro_idx = st.number_input("Indeks Kolom RVRO (Contoh: N = 13)", value=13, min_value=0)

# Fungsi Pembantu Cek Tarel Nol (Misal: 0/1, 0/30, 0, dll)
def is_tarel_zero(tarel_str):
    t = str(tarel_str).strip()
    if not t or t == "0" or t == "0.0":
        return True
    if "/" in t:
        parts = t.split("/")
        try:
            num = float(parts[0].strip())
            if num == 0:
                return True
        except:
            pass
    return False

# Fungsi Pembantu Cek Persentase Realisasi Nol (Kolom I)
def is_realisasi_zero(val):
    val_str = str(val).strip()
    if not val_str or val_str.lower() == '0':
        return True
    try:
        return float(val_str.replace('%', '').replace(',', '.')) == 0
    except:
        return True

# ==============================================================================
# 4. PEMROSESAN LOGIKA DATA & KALIMAT NARASI
# ==============================================================================
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
        if len(df) > 0 and str(df.iloc[0, 0]).strip().upper() == 'CONTOH':
            df = df.iloc[1:].reset_index(drop=True)

        temp_kegiatan = []
        current_ro = ""
        current_nama_ro = ""
        current_pcro_val = 0.0
        current_rvro_val = 0.0
        current_m_val = "0"
        current_n_val = ""
        current_has_unstarted = False 
        
        hasil_narasi = []

        for idx, row in df.iterrows():
            val_ro = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
            
            if val_ro.upper() == "BATAS":
                if current_ro:
                    rvro_teks = f"{current_m_val} {current_n_val}".strip()
                    
                    if len(temp_kegiatan) == 0 or (current_pcro_val == 0.0 and current_rvro_val == 0.0):
                        status_cat = "Belum Dimulai"
                        narasi = f"S.d. bulan {selected_month} {selected_year}, PCRO mencapai 0,00% dengan RVRO sebesar {rvro_teks} sehingga terdapat gap sebesar 0,00%, dikarenakan seluruh kegiatan pada RO {current_ro} belum dimulai."
                    elif current_pcro_val >= 100.0:
                        kegiatan_str = "\n".join([f"- {keg}" for keg in temp_kegiatan])
                        gap_val = abs(current_pcro_val - current_rvro_val)
                        g_str = f"{gap_val:.2f}".replace('.', ',')
                        status_cat = "Selesai 100%"
                        narasi = f"S.d. bulan {selected_month} {selected_year}, PCRO mencapai 100,00% dengan RVRO sebesar {rvro_teks} sehingga terdapat gap sebesar {g_str}%, dikarenakan seluruh kegiatan pada RO {current_ro} telah dilakukan, yaitu:\n{kegiatan_str}"
                    else:
                        kegiatan_str = "\n".join([f"- {keg}" for keg in temp_kegiatan])
                        gap_val = abs(current_pcro_val - current_rvro_val)
                        p_str = f"{current_pcro_val:.2f}".replace('.', ',')
                        g_str = f"{gap_val:.2f}".replace('.', ',')
                        status_cat = "Dalam Proses"
                        
                        if current_has_unstarted:
                            narasi = f"S.d. bulan {selected_month} {selected_year}, PCRO mencapai {p_str}% dengan RVRO sebesar {rvro_teks} sehingga terdapat gap sebesar {g_str}%, dikarenakan sudah dilakukan:\n{kegiatan_str}\nSedangkan kegiatan lain pada RO {current_ro} belum dimulai."
                        else:
                            narasi = f"S.d. bulan {selected_month} {selected_year}, PCRO mencapai {p_str}% dengan RVRO sebesar {rvro_teks} sehingga terdapat gap sebesar {g_str}%, dikarenakan sudah dilakukan:\n{kegiatan_str}"
                    
                    hasil_narasi.append({
                        "RO": current_ro,
                        "Nama RO": current_nama_ro,
                        "Status": status_cat,
                        "Narasi": narasi
                    })
                
                temp_kegiatan = []
                current_ro = ""
                current_nama_ro = ""
                current_pcro_val = 0.0
                current_rvro_val = 0.0
                current_m_val = "0"
                current_n_val = ""
                current_has_unstarted = False
                continue
            
            if val_ro and val_ro.lower() != 'nan':
                if not current_ro:
                    current_ro = val_ro
                    current_nama_ro = str(row.iloc[2]).strip() if len(row.values) > 2 and pd.notna(row.iloc[2]) else ""
                    
                    if has_pcro:
                        try: current_pcro_val = float(row.iloc[col_pcro_idx]) 
                        except: current_pcro_val = 0.0
                        try: current_rvro_val = float(row.iloc[col_rvro_idx])
                        except: current_rvro_val = 0.0
                        
                    # Ekstraksi Kolom M (Index 12) untuk PCRO Nilai
                    try:
                        m_val = row.iloc[12]
                        if pd.notna(m_val):
                            if isinstance(m_val, (int, float)):
                                current_m_val = str(m_val).replace('.', ',')
                                if current_m_val.endswith(',0'):
                                    current_m_val = current_m_val[:-2]
                            else:
                                current_m_val = str(m_val).strip()
                        else:
                            current_m_val = "0"
                    except:
                        current_m_val = "0"
                        
                    # Ekstraksi Kolom N (Index 13) untuk PCRO Satuan
                    try:
                        n_val = row.iloc[13]
                        current_n_val = str(n_val).strip() if pd.notna(n_val) else ""
                    except:
                        current_n_val = ""

                keg = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
                tarel = str(row.iloc[9]).strip() if pd.notna(row.iloc[9]) else ""
                satuan = str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else ""
                
                if keg and keg.lower() != 'nan' and tarel and tarel.lower() != 'nan':
                    if len(row.values) > 8 and is_realisasi_zero(row.iloc[8]):
                        current_has_unstarted = True

                    if not is_tarel_zero(tarel):
                        temp_kegiatan.append(f"{keg} ({tarel} {satuan})")

        # ==============================================================================
        # 5. FILTER & METRIK DASHBOARD
        # ==============================================================================
        c_search, c_filter = st.columns([3, 1])
        with c_search:
            search_ro = st.text_input("🔍 Cari Kode RO", placeholder="Ketik Kode RO (contoh: 2897.BMA.004)...")
        with c_filter:
            filter_st = st.selectbox("Status", ["Semua Status", "Selesai 100%", "Dalam Proses", "Belum Dimulai"])

        data_tampil = hasil_narasi
        if search_ro:
            data_tampil = [item for item in data_tampil if search_ro.lower() in item["RO"].lower()]
        if filter_st != "Semua Status":
            data_tampil = [item for item in data_tampil if item["Status"] == filter_st]

        st.markdown(f"### 📋 Daftar Narasi Capaian ({len(data_tampil)} RO)")
        st.caption("✨ Tekan kotak di bawah ini untuk melihat narasi otomatis dan menambahkan komentar tambahan.")
        
        # ==============================================================================
        # 6. TAMPILAN WRAPPER EXPANDER (AKORDION iOS KACA) & KOTAK KOMENTAR
        # ==============================================================================
        for item in data_tampil:
            if item['Status'] == 'Selesai 100%': 
                icon = "🟢"
            elif item['Status'] == 'Dalam Proses': 
                icon = "🟠"
            else: 
                icon = "⚪"
                
            with st.expander(f"{icon} RO {item['RO']} — {item['Status']}"):
                st.code(item['Narasi'], language=None)
                
                comment_key = f"comment_{item['RO']}"
                st.text_area(
                    "💬 Catatan / Komentar Tambahan:", 
                    key=comment_key, 
                    height=75,
                    placeholder="Ketik komentar untuk RO ini (teks yang Anda tulis bisa diblok lalu di-copy, serta otomatis masuk ke Excel)...",
                    help="Gunakan (Ctrl+C / Cmd+C) untuk Copy teks di kolom ini."
                )

        # ==============================================================================
        # 7. PUSAT UNDUHAN HASIL MENCANGKUP KOMENTAR
        # ==============================================================================
        st.markdown("---")
        st.markdown("### 📥 Unduh Hasil Keseluruhan (Sekaligus)")
        col_down1, col_down2 = st.columns(2)
        
        with col_down1:
            list_export = []
            for item in hasil_narasi:
                ro_code = item["RO"]
                user_comment = st.session_state.get(f"comment_{ro_code}", "")
                
                list_export.append({
                    "Nomor RO": ro_code,
                    "Uraian Nama RO": item["Nama RO"],
                    "Realisasi": item["Narasi"],
                    "Catatan / Komentar": user_comment
                })
                
            df_export = pd.DataFrame(list_export)
            df_export = df_export[["Nomor RO", "Uraian Nama RO", "Realisasi", "Catatan / Komentar"]]
            
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📊 Unduh Rekap CSV (Excel)",
                data=csv_data,
                file_name="Hasil_Narasi_Capaian_RO.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_down2:
            txt_lines = []
            for item in hasil_narasi:
                ro_code = item["RO"]
                c_text = st.session_state.get(f"comment_{ro_code}", "")
                block = item["Narasi"]
                if c_text.strip():
                    block += f"\nCatatan/Komentar: {c_text.strip()}"
                txt_lines.append(block)
                
            txt_data = "\n\n".join(txt_lines)
            st.download_button(
                "📄 Unduh Seluruh Teks (.TXT)",
                data=txt_data,
                file_name="Hasil_Narasi_Lengkap.txt",
                mime="text/plain",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan. Pastikan library `openpyxl` terpasang. Detail error: {e}")

else:
    st.info("💡 Silakan unggah file Excel `CAPUT` pada menu kiri untuk memunculkan kotak panel otomatis.")
