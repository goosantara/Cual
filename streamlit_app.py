import streamlit as st
import pandas as pd
import io

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Generator Narasi Capaian RO",
    page_icon="📊",
    layout="wide"
)

# Custom Styling CSS sederhana
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
st.markdown('<div class="sub-title">Otomasi penyusunan teks laporan capaian fisik dan realisasi RO dari file Excel</div>', unsafe_allow_html=True)

uploaded_file = st.file_uploader("Unggah File Excel (.xlsx / .xls)", type=['xlsx', 'xls'])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        # Standarisasi nama kolom
        df.columns = df.columns.astype(str).str.lower().str.strip()
        
        # Identifikasi kolom target
        col_ro = next((c for c in df.columns if 'rincian output' in c or c == 'ro' or c == 'b'), df.columns[1])
        col_kegiatan = next((c for c in df.columns if 'kegiatan' in c or c == 'd'), df.columns[3])
        col_satuan = next((c for c in df.columns if 'satuan' in c or c == 'g'), df.columns[6])
        col_tarel = next((c for c in df.columns if 'tarel' in c or c == 'j'), df.columns[9])
        
        # Kolom persentase (PCRO & RVRO)
        col_pcro = next((c for c in df.columns if 'pcro' in c), None)
        col_rvro = next((c for c in df.columns if 'rvro' in c), None)

        if st.button("⚡ Process & Generate Narasi", type="primary"):
            temp_kegiatan = []
            current_ro = ""
            current_pcro = 0.0
            current_rvro = 0.0
            
            hasil_narasi = []

            for idx, row in df.iterrows():
                val_ro = str(row[col_ro]).strip() if pd.notna(row[col_ro]) else ""
                
                # Deteksi penanda BATAS
                if val_ro.upper() == "BATAS":
                    if current_ro:
                        gap = abs(current_pcro - current_rvro)
                        
                        # Penggabungan daftar kegiatan
                        if len(temp_kegiatan) > 1:
                            kegiatan_str = ", ".join(temp_kegiatan[:-1]) + ", dan " + temp_kegiatan[-1]
                        elif len(temp_kegiatan) == 1:
                            kegiatan_str = temp_kegiatan[0]
                        else:
                            kegiatan_str = ""

                        # Penyusunan Pola Kalimat
                        if current_pcro == 0 and current_rvro == 0:
                            narasi = f"S.d. bulan Agustus 2026, PCRO mencapai 0,00% dengan RVRO sebesar 0,00% sehingga terdapat gap sebesar 0,00%, dikarenakan seluruh kegiatan pada RO {current_ro} belum dimulai."
                        elif current_pcro == 100:
                            narasi = f"S.d. bulan Agustus 2026, PCRO mencapai 100,00% dengan RVRO sebesar {current_rvro:.2f}% sehingga terdapat gap sebesar {gap:.2f}%, dikarenakan seluruh kegiatan pada RO {current_ro} telah dilakukan, yaitu {kegiatan_str}."
                        else:
                            narasi = f"S.d. bulan Agustus 2026, PCRO mencapai {current_pcro:.2f}% dengan RVRO sebesar {current_rvro:.2f}% sehingga terdapat gap sebesar {gap:.2f}%, dikarenakan sudah dilakukan {kegiatan_str}, sedangkan kegiatan lain pada RO {current_ro} belum dimulai."
                        
                        hasil_narasi.append({"RO": current_ro, "Narasi": narasi})
                    
                    # Reset state
                    temp_kegiatan = []
                    current_ro = ""
                    continue
                
                # Pengumpulan data per kegiatan
                if val_ro != "":
                    if not current_ro:
                        current_ro = val_ro
                        current_pcro = float(row[col_pcro]) if col_pcro and pd.notna(row[col_pcro]) else 0.0
                        current_rvro = float(row[col_rvro]) if col_rvro and pd.notna(row[col_rvro]) else 0.0

                    keg = str(row[col_kegiatan]).strip() if pd.notna(row[col_kegiatan]) else ""
                    tarel = str(row[col_tarel]).strip() if pd.notna(row[col_tarel]) else ""
                    satuan = str(row[col_satuan]).strip() if pd.notna(row[col_satuan]) else ""
                    
                    if keg and keg.lower() != 'nan':
                        temp_kegiatan.append(f"{keg} {tarel} {satuan}")

            # Tampilan Hasil di Web
            st.markdown("---")
            st.subheader(f"📋 Hasil Generate Narasi ({len(hasil_narasi)} RO)")
            
            full_text = ""
            for item in hasil_narasi:
                st.markdown(f"""
                <div class="narasi-box">
                    <strong>RO {item['RO']}</strong><br>
                    {item['Narasi']}
                </div>
                """, unsafe_allow_html=True)
                full_text += item['Narasi'] + "\n"

            # Action Buttons
            col1, col2 = st.columns(2)
            with col1:
                df_download = pd.DataFrame(hasil_narasi)
                csv = df_download.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Unduh Seluruh Narasi (.CSV)",
                    data=csv,
                    file_name="Hasil_Narasi_RO.csv",
                    mime="text/csv"
                )
            with col2:
                st.download_button(
                    label="📥 Unduh File Teks (.TXT)",
                    data=full_text,
                    file_name="Hasil_Narasi_RO.txt",
                    mime="text/plain"
                )

    except Exception as e:
        st.error(f"Gagal memproses file Excel. Pastikan struktur kolom sesuai. Detail error: {e}")
