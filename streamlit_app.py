import streamlit as st
import pandas as pd

# ==============================================================================
# 1. KONFIGURASI HALAMAN & THEME (iOS + NUANSA MELAYU)
# ==============================================================================
st.set_page_config(
    page_title="Generator Narasi RO - Melayu iOS Edition",
    page_icon="🕌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS: Estetika Melayu (Hijau & Emas) + iOS (Glassmorphism & Rounded)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    /* Background Aplikasi - Abu-abu bersih khas iOS */
    .stApp {
        background-color: #F4F5F9;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Plus Jakarta Sans", sans-serif;
    }

    /* Header Banner - Nuansa Melayu (Hijau Lumut & Kuning Keemasan) */
    .melayu-header {
        background: linear-gradient(135deg, #064E3B 0%, #047857 50%, #065F46 100%);
        border-radius: 22px;
        padding: 30px 35px;
        color: #FFFFFF;
        box-shadow: 0 10px 30px rgba(4, 120, 87, 0.25);
        border: 1px solid rgba(245, 158, 11, 0.5);
        position: relative;
        overflow: hidden;
        margin-bottom: 28px;
    }

    /* Aksen Emas (Pucuk Rebung Abstract / List Emas Melayu) */
    .melayu-header::before {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 6px;
        background: linear-gradient(90deg, #D97706 0%, #FBBF24 25%, #F59E0B 50%, #FCD34D 75%, #D97706 100%);
    }
    .melayu-header::after {
        content: "";
        position: absolute;
        bottom: 0; left: 0; right: 0;
        height: 4px;
        background: linear-gradient(90deg, #D97706 0%, #FBBF24 50%, #D97706 100%);
    }

    .melayu-title {
        font-size: 26px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: #F8FAFC;
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 0;
    }
    .melayu-subtitle {
        font-size: 14px;
        color: #D1FAE5;
        margin-top: 8px;
        font-weight: 400;
    }

    /* Card Container - iOS Frosted Glass */
    .ios-card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 18px;
        border: 1px solid rgba(226, 232, 240, 0.8);
        padding: 22px 26px;
        margin-bottom: 22px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.04);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .ios-card:hover {
        box-shadow: 0 8px 25px rgba(4, 120, 87, 0.08);
        border-color: rgba(245, 158, 11, 0.4);
        transform: translateY(-2px);
    }

    /* CSS Text Wrap di dalam Kotak Code & Font Rapi iOS */
    div[data-testid="stCodeBlock"] code, 
    div[data-testid="stCodeBlock"] pre {
        white-space: pre-wrap !important;
        word-break: break-word !important;
        overflow-x: hidden !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif !important;
        font-size: 14.5px !important;
        line-height: 1.7 !important;
        background-color: #FAFAFA !important;
        color: #1E293B !important;
        border-radius: 14px !important;
        border: 1px solid #E2E8F0 !important;
        padding: 18px !important;
    }

    /* iOS Status Pill Badges (Warna disesuaikan ke estetika Melayu/Hijau Emas) */
    .ios-badge {
        display: inline-block;
        padding: 5px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: -0.2px;
    }
    .ios-badge-success { background-color: #ECFDF5; color: #047857; border: 1px solid #D1FAE5; }
    .ios-badge-progress { background-color: #FEF3C7; color: #B45309; border: 1px solid #FDE68A; }
    .ios-badge-empty { background-color: #F1F5F9; color: #64748B; border: 1px solid #E2E8F0; }

    /* Custom Styling Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. HEADER UTAMA (MELAYU & IOS DESIGN)
# ==============================================================================
st.markdown("""
    <div class="melayu-header">
        <div class="melayu-title">
            <span>🕌</span> Generator Narasi Rincian Output (RO)
        </div>
        <div class="melayu-subtitle">
            Sistem Otomasi Laporan Capaian Kinerja • Estetika Tanah Melayu & Antarmuka iOS
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SIDEBAR UPLOAD & KONTROL
# ==============================================================================
with st.sidebar:
    st.markdown("### 📱 Panel Pengunggahan")
    st.caption("Unggah file Excel `CAPUT` Anda untuk menyusun narasi.")
    
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

# ==============================================================================
# 4. PEMROSESAN LOGIKA DATA & KALIMAT NARASI (FORMAT BULLET POINTS)
# ==============================================================================
if uploaded_file is not None:
    try:
        # Membaca Data
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
        # Abaikan baris header 'CONTOH' jika ada di baris pertama
        if len(df) > 0 and str(df.iloc[0, 0]).strip().upper() == 'CONTOH':
            df = df.iloc[1:].reset_index(drop=True)

        temp_kegiatan = []
        current_ro = ""
        current_pcro_val = 0.0
        current_rvro_val = 0.0
        
        hasil_narasi = []

        for idx, row in df.iterrows():
            val_ro = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
            
            # --- DETEKSI KATA "BATAS" ---
            if val_ro.upper() == "BATAS":
                if current_ro:
                    
                    # FORMAT BARU: Membuat daftar kegiatan menyusun ke bawah (Bullet Points)
                    if len(temp_kegiatan) > 0:
                        kegiatan_str = "\n".join([f"- {keg}" for keg in temp_kegiatan])
                    else:
                        kegiatan_str = ""
                        
                    # Hitung GAP
                    gap_val = abs(current_pcro_val - current_rvro_val)
                    
                    # Format ke Desimal Indonesia (Koma)
                    p_str = f"{current_pcro_val:.2f}".replace('.', ',')
                    r_str = f"{current_rvro_val:.2f}".replace('.', ',')
                    g_str = f"{gap_val:.2f}".replace('.', ',')

                    # Evaluasi Kondisi & Pembentukan Narasi (Format Rapi)
                    if current_pcro_val == 0.0 and current_rvro_val == 0.0:
                        status_badge = '<span class="ios-badge ios-badge-empty">Belum Dimulai</span>'
                        status_cat = "Belum Dimulai"
                        narasi = f"S.d. bulan Agustus 2026, PCRO mencapai {p_str}% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan seluruh kegiatan pada RO {current_ro} belum dimulai."
                        
                    elif current_pcro_val >= 100.0:
                        status_badge = '<span class="ios-badge ios-badge-success">Selesai 100%</span>'
                        status_cat = "Selesai 100%"
                        narasi = f"S.d. bulan Agustus 2026, PCRO mencapai 100,00% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan seluruh kegiatan pada RO {current_ro} telah dilakukan, yaitu:\n{kegiatan_str}"
                        
                    else:
                        status_badge = f'<span class="ios-badge ios-badge-progress">Berjalan ({p_str}%)</span>'
                        status_cat = "Dalam Proses"
                        narasi = f"S.d. bulan Agustus 2026, PCRO mencapai {p_str}% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan sudah dilakukan:\n{kegiatan_str}\n\nSedangkan kegiatan lain pada RO {current_ro} belum dimulai."
                    
                    hasil_narasi.append({
                        "RO": current_ro,
                        "PCRO": current_pcro_val,
                        "RVRO": current_rvro_val,
                        "GAP": gap_val,
                        "Status": status_cat,
                        "Badge": status_badge,
                        "Narasi": narasi
                    })
                
                # Reset penampung untuk RO berikutnya
                temp_kegiatan = []
                current_ro = ""
                current_pcro_val = 0.0
                current_rvro_val = 0.0
                continue
            
            # --- PENGUMPULAN KEGIATAN PER BARIS ---
            if val_ro and val_ro.lower() != 'nan':
                if not current_ro:
                    current_ro = val_ro
                    if has_pcro:
                        try: current_pcro_val = float(row.iloc[col_pcro_idx]) 
                        except: current_pcro_val = 0.0
                        
                        try: current_rvro_val = float(row.iloc[col_rvro_idx])
                        except: current_rvro_val = 0.0

                # Read Kolom D (Idx 3), Kolom J (Idx 9), Kolom G (Idx 6)
                keg = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
                tarel = str(row.iloc[9]).strip() if pd.notna(row.iloc[9]) else ""
                satuan = str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else ""
                
                # Hanya masukkan kegiatan yang sudah memiliki progres (mengabaikan 0/X)
                if keg and keg.lower() != 'nan' and tarel and tarel.lower() != 'nan':
                    if not tarel.startswith("0/") and tarel != "0":
                        # Susun ke format: Nama Kegiatan (Realisasi/Target Satuan)
                        temp_kegiatan.append(f"{keg} ({tarel} {satuan})")

        # ==============================================================================
        # 5. METRIK RINGKASAN GAYA iOS WIDGET
        # ==============================================================================
        total_ro = len(hasil_narasi)
        ro_selesai = sum(1 for item in hasil_narasi if item["Status"] == "Selesai 100%")
        ro_proses = sum(1 for item in hasil_narasi if item["Status"] == "Dalam Proses")
        ro_belum = sum(1 for item in hasil_narasi if item["Status"] == "Belum Dimulai")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Rincian Output", f"{total_ro} RO")
        col2.metric("Selesai 100%", f"{ro_selesai} RO", delta=f"{(ro_selesai/total_ro*100 if total_ro else 0):.0f}%")
        col3.metric("Dalam Proses", f"{ro_proses} RO")
        col4.metric("Belum Dimulai", f"{ro_belum} RO")

        st.markdown("<br>", unsafe_allow_html=True)

        # ==============================================================================
        # 6. FILTER & PENCARIAN
        # ==============================================================================
        c_search, c_filter = st.columns([3, 1])
        with c_search:
            search_ro = st.text_input("🔍 Cari Kode RO", placeholder="Ketik Kode RO (contoh: 2897.BMA.004)...")
        with c_filter:
            filter_st = st.selectbox("Status RO", ["Semua Status", "Selesai 100%", "Dalam Proses", "Belum Dimulai"])

        # Filter Process
        data_tampil = hasil_narasi
        if search_ro:
            data_tampil = [item for item in data_tampil if search_ro.lower() in item["RO"].lower()]
        if filter_st != "Semua Status":
            data_tampil = [item for item in data_tampil if item["Status"] == filter_st]

        # ==============================================================================
        # 7. TAMPILAN NARASI (AUTO COPAS & BULLET POINTS RAPI)
        # ==============================================================================
        st.markdown(f"### 📋 Daftar Narasi Capaian ({len(data_tampil)} RO)")
        st.caption("Klik tombol **Salin / Copy** di sudut kanan atas tiap kotak teks untuk menyalin langsung.")

        for item in data_tampil:
            # Wrap dalam iOS Container Card yang Estetik
            st.markdown(f"""
            <div class="ios-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
                    <span style="font-weight: 700; font-size: 16px; color: #064E3B;">
                        📍 RO {item['RO']}
                    </span>
                    <div>{item['Badge']}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Text Area dengan fitur Auto-Copy & Baris Menyusun (Bullet points)
            st.code(item['Narasi'], language=None)
            
            st.markdown("</div>", unsafe_allow_html=True)

        # ==============================================================================
        # 8. PUSAT UNDUHAN HASIL
        # ==============================================================================
        st.markdown("---")
        st.markdown("### 📥 Unduh Hasil Narasi")
        col_down1, col_down2 = st.columns(2)
        
        with col_down1:
            df_export = pd.DataFrame(hasil_narasi)[["RO", "Status", "PCRO", "RVRO", "GAP", "Narasi"]]
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button(
                "📊 Unduh Rekap CSV / Excel",
                data=csv_data,
                file_name="Hasil_Narasi_Capaian_RO.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_down2:
            txt_data = "\n\n".join([item["Narasi"] for item in hasil_narasi])
            st.download_button(
                "📄 Unduh Seluruh Teks (.TXT)",
                data=txt_data,
                file_name="Hasil_Narasi_Lengkap.txt",
                mime="text/plain",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan pemrosesan. Pastikan library `openpyxl` terpasang. Detail: {e}")

else:
    # Tampilan saat aplikasi baru dibuka
    st.info("💡 Silakan upload file Excel `CAPUT 2026` pada menu di sebelah kiri untuk menampilkan narasi otomatis.")
