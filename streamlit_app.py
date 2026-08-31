import streamlit as st
import pandas as pd

# Konfigurasi Tampilan
st.set_page_config(page_title="Generator Narasi Capaian RO", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; margin-bottom: 5px; }
    .sub-title { font-size: 14px; color: #4B5563; margin-bottom: 25px; }
    .narasi-box { 
        background-color: #F9FAFB; 
        border-left: 4px solid #2563EB; 
        padding: 15px; 
        border-radius: 4px; 
        margin-bottom: 12px;
        font-family: sans-serif;
        line-height: 1.6;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📊 Generator Narasi Capaian Rincian Output (RO)</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Sistem otomatis dengan penyesuaian format Excel "CAPUT 2026"</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Unggah File Excel (.xlsx / .csv)", type=['xlsx', 'xls', 'csv'])

if uploaded_file is not None:
    try:
        # 1. Membaca data (support baik excel maupun csv)
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file, engine='openpyxl')
            
        # 2. Hapus baris 'CONTOH' jika ada di baris pertama
        if str(df.iloc[0, 0]).upper() == 'CONTOH':
            df = df.iloc[1:].reset_index(drop=True)
            
        st.success("✅ File berhasil dibaca sistem. Klik Generate untuk memproses.")
        
        # 3. Ekspander Pengaturan (Fitur untuk menyesuaikan posisi kolom PCRO & RVRO)
        with st.expander("⚙️ Pengaturan Kolom (Mapping Khusus)"):
            st.info("Secara bawaan sistem sudah mengunci Kolom B (RO), D (Kegiatan), G (Satuan), dan J (Tarel).")
            has_pcro = st.checkbox("Ambil angka PCRO & RVRO dari dalam file Excel", value=False)
            if has_pcro:
                col_pcro = st.number_input("Kolom ke-berapa untuk PCRO? (Mulai dari 0, contoh Kolom M = 12)", value=12, min_value=0)
                col_rvro = st.number_input("Kolom ke-berapa untuk RVRO? (Mulai dari 0, contoh Kolom N = 13)", value=13, min_value=0)

        if st.button("⚡ Process & Generate Narasi", type="primary"):
            temp_kegiatan = []
            current_ro = ""
            current_pcro_val = 0.0
            current_rvro_val = 0.0
            
            hasil_narasi = []

            for idx, row in df.iterrows():
                # Membaca Kolom B (Index 1) untuk Rincian Output
                val_ro = str(row.iloc[1]).strip() if pd.notna(row.iloc[1]) else ""
                
                # --- JIKA BERTEMU "BATAS" ---
                if val_ro.upper() == "BATAS":
                    if current_ro:
                        # Logika tata bahasa penggabungan list kegiatan
                        if len(temp_kegiatan) > 1:
                            kegiatan_str = ", ".join(temp_kegiatan[:-1]) + ", dan " + temp_kegiatan[-1]
                        elif len(temp_kegiatan) == 1:
                            kegiatan_str = temp_kegiatan[0]
                        else:
                            kegiatan_str = ""
                            
                        # Hitung GAP
                        gap_val = abs(current_pcro_val - current_rvro_val)
                        
                        # Format ke koma desimal Indonesia
                        p_str = f"{current_pcro_val:.2f}".replace('.', ',')
                        r_str = f"{current_rvro_val:.2f}".replace('.', ',')
                        g_str = f"{gap_val:.2f}".replace('.', ',')

                        # Logika Penyusunan Kalimat
                        if current_pcro_val == 0.0 and current_rvro_val == 0.0:
                            narasi = f"S.d. bulan Agustus 2026, PCRO mencapai {p_str}% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan seluruh kegiatan pada RO {current_ro} belum dimulai."
                        elif current_pcro_val == 100.0:
                            narasi = f"S.d. bulan Agustus 2026, PCRO mencapai {p_str}% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan seluruh kegiatan pada RO {current_ro} telah dilakukan, yaitu {kegiatan_str}."
                        else:
                            narasi = f"S.d. bulan Agustus 2026, PCRO mencapai {p_str}% dengan RVRO sebesar {r_str}% sehingga terdapat gap sebesar {g_str}%, dikarenakan sudah dilakukan {kegiatan_str}, sedangkan kegiatan lain pada RO {current_ro} belum dimulai."
                        
                        hasil_narasi.append({"RO": current_ro, "Narasi": narasi})
                    
                    # Reset variabel pengumpul untuk RO selanjutnya
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
                            # Jika diatur, ambil dari sel, jika gagal ubah jadi 0.0
                            try: current_pcro_val = float(row.iloc[col_pcro]) 
                            except: current_pcro_val = 0.0
                            
                            try: current_rvro_val = float(row.iloc[col_rvro])
                            except: current_rvro_val = 0.0

                    # Kolom D (Idx 3) Kegiatan, Kolom J (Idx 9) Tarel, Kolom G (Idx 6) Satuan
                    keg = str(row.iloc[3]).strip() if pd.notna(row.iloc[3]) else ""
                    tarel = str(row.iloc[9]).strip() if pd.notna(row.iloc[9]) else ""
                    satuan = str(row.iloc[6]).strip() if pd.notna(row.iloc[6]) else ""
                    
                    if keg and keg.lower() != 'nan' and tarel and tarel.lower() != 'nan':
                        # PENTING: Hanya memasukkan kegiatan yang Tarel-nya sudah ada progres 
                        # Abaikan jika tarel berawalan "0/" (Misal 0/1, 0/40) karena belum dilakukan
                        if not tarel.startswith("0/") and tarel != "0":
                            temp_kegiatan.append(f"{keg} {tarel} {satuan}")
                            
            # ----- Menampilkan UI Hasil -----
            st.markdown("---")
            st.subheader(f"📋 Hasil Generate Narasi ({len(hasil_narasi)} RO)")
            
            full_text = ""
            for item in hasil_narasi:
                st.markdown(f'''
                <div class="narasi-box">
                    <strong>RO {item['RO']}</strong><br>
                    {item['Narasi']}
                </div>
                ''', unsafe_allow_html=True)
                full_text += item['Narasi'] + "\n"

            # Tombol Unduh
            if len(hasil_narasi) > 0:
                col1, col2 = st.columns(2)
                with col1:
                    df_download = pd.DataFrame(hasil_narasi)
                    csv = df_download.to_csv(index=False).encode('utf-8')
                    st.download_button("📥 Unduh Excel / CSV", data=csv, file_name="Narasi_Laporan_RO.csv", mime="text/csv")
                with col2:
                    st.download_button("📥 Unduh File Teks (.TXT)", data=full_text, file_name="Narasi_Laporan_RO.txt", mime="text/plain")

    except Exception as e:
        st.error(f"Terjadi kesalahan saat mengolah struktur file. Detail: {e}")
