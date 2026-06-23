import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import datetime

# Konfigurasi Halaman Web
st.set_page_config(page_title="Kasir Swalayan Pro Max", page_icon="🛍️", layout="wide")

# Inisialisasi Session State untuk menyimpan database riwayat transaksi
if 'riwayat' not in st.session_state:
    st.session_state.riwayat = []

# Modifikasi CSS agar tombol lebih elegan
st.markdown("""
    <style>
    div.stButton > button:first-child { width: 100%; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- AREA PANEL SAMPING (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Panel Transaksi")
    total_belanja = st.number_input("Total Belanja (Rp)", min_value=0, step=50000)
    uang_pembayaran = st.number_input("Uang Pembayaran (Rp)", min_value=0, step=50000)
    st.divider()
    proses_btn = st.button("Hitung Transaksi", type="primary")
    
    # Tombol Tambahan untuk Menghapus Database
    if st.button("Hapus Riwayat"):
        st.session_state.riwayat = []
        st.rerun()

# --- AREA UTAMA (MAIN SCREEN) ---
st.title("🛍️ Smart POS & Data Analytics")
st.markdown("Sistem Kasir Swalayan Terintegrasi dengan Perekaman Data Transaksi Otomatis.")
st.divider()

if proses_btn:
    if uang_pembayaran == 0 and total_belanja == 0:
        st.warning("⚠️ Silakan masukkan nominal transaksi di panel samping kiri terlebih dahulu.")
    else:
        # 1. Logika Diskon
        if total_belanja >= 80000000: diskon_persen = 0.20
        elif total_belanja >= 45000000: diskon_persen = 0.14
        elif total_belanja >= 35000000: diskon_persen = 0.12
        elif total_belanja >= 25000000: diskon_persen = 0.10
        else: diskon_persen = 0.0

        # 2. Hitung Pembayaran
        nominal_diskon = int(total_belanja * diskon_persen)
        total_bayar = total_belanja - nominal_diskon
        kembalian = uang_pembayaran - total_bayar

        # 3. Output Struk
        if kembalian < 0:
            st.error(f"❌ Transaksi Gagal! Uang konsumen kurang Rp {abs(kembalian):,}".replace(",", "."))
        else:
            st.toast('Transaksi Berhasil Diproses!', icon='✅')
            st.balloons()
            
            # Merekam data ke dalam Session State
            waktu_sekarang = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
            st.session_state.riwayat.append({
                "Waktu": waktu_sekarang,
                "Total Belanja": total_belanja,
                "Diskon": nominal_diskon,
                "Total Bayar": total_bayar,
                "Pembayaran": uang_pembayaran,
                "Kembalian": kembalian
            })

            st.subheader("🧾 Struk Pembayaran Digital")
            st.caption(f"Waktu Cetak: {waktu_sekarang}")
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Belanja", f"Rp {total_belanja:,}".replace(",", "."))
            col2.metric(f"Diskon ({int(diskon_persen*100)}%)", f"- Rp {nominal_diskon:,}".replace(",", "."), delta_color="inverse")
            col3.metric("Total Bayar", f"Rp {total_bayar:,}".replace(",", "."))
            
            st.success(f"**Uang Kembalian: Rp {kembalian:,}**".replace(",", "."))
            
            with st.expander("Klik untuk melihat Rincian Pecahan Kembalian 💵", expanded=False):
                daftar_pecahan = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 100, 50]
                sisa_kembalian = kembalian
                for pecahan in daftar_pecahan:
                    jumlah_lembar = sisa_kembalian // pecahan
                    sisa_kembalian = sisa_kembalian % pecahan
                    if jumlah_lembar > 0:
                        satuan = "lembar" if pecahan >= 1000 else "keping"
                        st.write(f"🔹 **Rp {pecahan:,}**".replace(",", ".") + f" : {jumlah_lembar} {satuan}")

st.divider()

# --- AREA ANALITIK RIWAYAT TRANSAKSI ---
if st.session_state.riwayat:
    st.subheader("📊 Database Riwayat Transaksi")
    df_riwayat = pd.DataFrame(st.session_state.riwayat)
    
    # Format angka agar rapi saat ditampilkan di tabel web
    df_display = df_riwayat.copy()
    for col in ["Total Belanja", "Diskon", "Total Bayar", "Pembayaran", "Kembalian"]:
        df_display[col] = df_display[col].apply(lambda x: f"Rp {x:,}".replace(",", "."))
        
    st.dataframe(df_display, use_container_width=True)
    
    # Fitur Download File Ekstraksi
    csv_data = df_riwayat.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download Laporan Transaksi (Format CSV)",
        data=csv_data,
        file_name=f"laporan_transaksi_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )

