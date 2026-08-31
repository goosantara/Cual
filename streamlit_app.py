import streamlit as st
import pandas as pd
import io

# ==============================================================================
# 1. KONFIGURASI HALAMAN & CUSTOM CSS (OFFICIAL DASHBOARD THEME)
# ==============================================================================
st.set_page_config(
    page_title="Portal Otomasi Narasi Capaian RO",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
    /* Main Background & Fonts */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }
    
    /* Header Banner Top */
    .portal-header {
        background: linear-gradient(135deg, #0F172A 0%, #1E3A8A 100%);
        color: #FFFFFF;
        padding: 24px 30px;
        border-radius: 12px;
        margin-bottom: 25px;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.15);
    }
    .portal-title {
        font-size: 26px;
        font-weight: 700;
        margin: 0;
        letter-spacing: -0.5px;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .portal-subtitle {
        font-size: 14px;
        color: #94A3B8;
        margin-top: 6px;
    }
    
    /* Card Container */
    .ro-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 22px;
        margin-bottom: 18px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
        transition: all 0.2s ease-in-out;
    }
    .ro-card:hover {
        border-color: #CBD5E1;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    
    /* Status Badges */
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-success { background-color: #DCFCE7; color: #166534; border: 1px solid #BBF7D0; }
    .badge-progress { background-color: #E0F2FE; color: #075985; border: 1px solid #BAE6FD; }
    .badge-empty { background-color: #F1F5F9; color: #475569; border: 1px solid #E2E8F0; }
    
    /* Copy Instruction Subtext */
    .copy-hint {
        font-size: 12px;
        color: #64748B;
        margin-top: 4px;
        margin-bottom: 6px;
        display: flex;
        align-items: center;
        gap: 4px;
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. HEADER PORTAL UTAMA
# ==============================================================================
st.markdown("""
    <div class="portal-header">
        <div class="portal-title">
            <span>🏛️</span> Sistem Otomasi Pelaporan Capaian Rincian Output (RO)
        </div>
        <div class="portal-subtitle">
            Aplikasi resmi pemrosesan data kinerja fisik & penyusunan kalimat narasi otomatis berdasarkan format Excel CAPUT.
        </div>
    </div>
""", unsafe_allow_html=True)

# ==============================================================================
# 3. SIDEBAR CONTROLS & UPLOAD
# ==============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/analytics.png", width=64)
    st.title("Panel Kontrol")
    st.markdown("---")
    
    uploaded_file = st.file_uploader(
        "Unggah File CAPUT (.xlsx / .csv)", 
        type=['xlsx', 'xls', 'csv'],
        help="Unggah file Excel mentah format CAPUT"
    )
    
    st.markdown("---")
    st.markdown("### ⚙️ Pemetaan Kolom Excel")
    st.caption("Default otomatis membaca susunan standar CAPUT BPS.")
    
    has_pcro = st.checkbox("Ambil angka PCRO & RVRO dari Excel", value=False)
    col_pcro_idx = 12
    col_rvro_idx = 13
    
    if has_pcro:
        col_pcro_idx = st.number_input("Indeks Kolom PCRO (Misal M = 12)", value=12, min_value=0)
        col_rvro_idx = st.number_input("Indeks Kolom RVRO (Misal N = 13)", value=13, min_value=0)

# ==============================================================================
# 4. PEMROSESAN DATA & LOGIKA NARASI
# ==============================================================================
if uploaded_file is not None:
    try:
        # Membaca Data (Engine openpyxl)
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
        # Abaikan baris header contoh jika ada
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
                    # Tata Bahasa Rangkaian Kegiatan
                    if len(temp_kegiatan) > 1:
                        kegiatan_str = ", ".join(temp_kegiatan[:-1]) + ", dan " + temp_kegiatan[-1]
                    elif len(temp_kegiatan) == 1:
                        kegiatan_str = temp_kegiatan[0]
                    else:
                        kegiatan_str = ""
                        
                    # Hitung GAP
                    gap_val = abs(current_pcro_val - current_rvro_val)
                    
                    # Format Angka Desimal Indonesia (Koma)
                    p_str = f"{current_pcro_val:.2f}".replace('.', ',')
                    r_str = f"{current_rvro_val:.2f}".replace('.', ',')
                    g_str = f"{gap_val:.2f}".replace('.', ',')

                    # Konstruksi Teks Narasi & Status Badge
                    if current_pcro_val == 0.0 and current_rvro_val == 0.0:
                        status_badge = '<span class="badge badge-empty">Belum Dimulai</span>'
                        status_cat = "Belum Dimulai"
                        narasi = f"S.d. bulan Agustus 2026, PCRO mencapai {p_str}% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan seluruh kegiatan pada RO {current_ro} belum dimulai."
                    elif current_pcro_val >= 100.0:
                        status_badge = '<span class="badge badge-success">Selesai 100%</span>'
                        status_cat = "Selesai 100%"
                        narasi = f"S.d. bulan Agustus 2026, PCRO mencapai 100,00% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan seluruh kegiatan pada RO {current_ro} telah dilakukan, yaitu {kegiatan_str}."
                    else:
                        status_badge = f'<span class="badge badge-progress">Berjalan ({p_str}%)</span>'
                        status_cat = "Dalam Proses"
                        narasi = f"S.d. bulan Agustus 2026, PCRO mencapai {p_str}% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan sudah dilakukan {kegiatan_str}, sedangkan kegiatan lain pada RO {current_ro} belum dimulai."
                    
                    hasil_narasi.append({
                        "RO": current_ro,
                        "PCRO": current_pcro_val,
                        "RVRO": current_rvro_val,
                        "GAP": gap_val,
                        "Status": status_cat,
                        "Badge": status_badge,
                        "Narasi": narasi
                    })
                
                # Reset State
                temp_kegiatan = []
                current_ro = ""
                current_pcro_val = 0.0
                current_rvro_val = 0.0
                continue
            
            # --- PENGUMPULAN RINCAN KEGIATAN PER BARIS ---
            if val_ro and val_ro.lower() != 'nan':
                if not current_ro:
                    current_ro = val_ro
                    if has_pcro:
                        try: current_pcro_val = float(row.iloc[col_pcro_idx]) 
                        except: current_pcro_val = 0.0
                        
                        try: current_rvro_val = float(row.iloc[col_rvro_idx])
                        except: current_rvro_val = 0.0

                keg = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
                tarel = str(row.iloc[9]).strip() if pd.notna(row.iloc[9]) else ""
                satuan = str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else ""
                
                # Hanya masukkan kegiatan yang sudah memiliki progres (bukan 0/X)
                if keg and keg.lower() != 'nan' and tarel and tarel.lower() != 'nan':
                    if not tarel.startswith("0/") and tarel != "0":
                        temp_kegiatan.append(f"{keg} {tarel} {satuan}")

        # ==============================================================================
        # 5. DASHBOARD STATISTIK UTAMA (EXECUTIVE METRICS)
        # ==============================================================================
        total_ro = len(hasil_narasi)
        ro_selesai = sum(1 for item in hasil_narasi if item["Status"] == "Selesai 100%")
        ro_proses = sum(1 for item in hasil_narasi if item["Status"] == "Dalam Proses")
        ro_belum = sum(1 for item in hasil_narasi if item["Status"] == "Belum Dimulai")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)
        col_m1.metric("Total Rincian Output (RO)", f"{total_ro} RO", delta=None)
        col_m2.metric("Tuntas (100%)", f"{ro_selesai} RO", delta=f"{(ro_selesai/total_ro*100 if total_ro else 0):.1f}%")
        col_m3.metric("Dalam Proses", f"{ro_proses} RO", delta=None)
        col_m4.metric("Belum Dimulai", f"{ro_belum} RO", delta=None)
        
        st.markdown("<br>", unsafe_allow_html=True)

        # ==============================================================================
        # 6. INTERACTIVE SEARCH & FILTER BAR
        # ==============================================================================
        col_search, col_filter = st.columns([3, 1])
        with col_search:
            search_query = st.text_input("🔍 Cari berdasarkan Kode RO", placeholder="Contoh: 2897.BMA.004")
        with col_filter:
            filter_status = st.selectbox("Filter Status", ["Semua Status", "Selesai 100%", "Dalam Proses", "Belum Dimulai"])

        # Filtering Process
        filtered_results = hasil_narasi
        if search_query:
            filtered_results = [item for item in filtered_results if search_query.lower() in item["RO"].lower()]
        if filter_status != "Semua Status":
            filtered_results = [item for item in filtered_results if item["Status"] == filter_status]

        # ==============================================================================
        # 7. TAMPILAN NARASI DENGAN FITUR AUTO-COPAS 1-KLIK
        # ==============================================================================
        st.markdown(f"### 📋 Daftar Narasi Capaian ({len(filtered_results)} Ditampilkan)")
        st.caption("Klik tombol ikon **Copas** di pojok kanan atas tiap kotak teks untuk menyalin langsung ke clipboard.")

        for idx, item in enumerate(filtered_results):
            with st.container():
                st.markdown(f"""
                <div style="display: flex; justify-space-between; align-items: center; margin-bottom: 6px;">
                    <span style="font-weight: 700; font-size: 16px; color: #0F172A;">
                        📍 RO {item['RO']}
                    </span>
                    <div>{item['Badge']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Menggunakan st.code() untuk auto copas bawaan yang sangat cepat & stabil
                st.code(item['Narasi'], language=None)
                st.markdown("<div style='margin-bottom: 20px;'></div>", unsafe_allow_html=True)

        # ==============================================================================
        # 8. TOMBOL EKSPOR & UNDUH KESELURUHAN
        # ==============================================================================
        st.markdown("---")
        st.markdown("### 📥 Pusat Unduhan Laporan")
        
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            df_download = pd.DataFrame(hasil_narasi)[["RO", "Status", "PCRO", "RVRO", "GAP", "Narasi"]]
            csv_buffer = df_download.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📊 Unduh Rekap Laporan Format Excel/CSV",
                data=csv_buffer,
                file_name="Rekap_Narasi_Capaian_RO.csv",
                mime="text/csv",
                use_container_width=True
            )
        with col_d2:
            full_txt = "\n\n".join([item["Narasi"] for item in hasil_narasi])
            st.download_button(
                label="📄 Unduh Seluruh Teks Narasi (.TXT)",
                data=full_txt,
                file_name="Narasi_Laporan_Lengkap.txt",
                mime="text/plain",
                use_container_width=True
            )

    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan saat membaca file. Pastikan pustaka `openpyxl` sudah terinstall. Detail error: {e}")

else:
    # State awal saat belum ada file yang diunggah
    st.info("💡 Silakan unggah file Excel `CAPUT 2026` melalui menu panel di sebelah kiri untuk memulai generate narasi.")
