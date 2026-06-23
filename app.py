import streamlit as st

# Konfigurasi Halaman Web
st.set_page_config(page_title="Kasir Swalayan Teknik Industri", page_icon="🛒", layout="centered")

# Judul dan Deskripsi
st.title("🛒 Sistem Kasir Swalayan")
st.markdown("Aplikasi perhitungan kasir otomatis dengan fitur diskon bertingkat dan kalkulasi pemisahan pecahan uang kembalian.")
st.divider()

# Kolom Input dari Pengguna
total_belanja = st.number_input("Masukkan Total Belanja Konsumen (Rp)", min_value=0, step=50000)
uang_pembayaran = st.number_input("Masukkan Uang Pembayaran (Rp)", min_value=0, step=50000)

# Tombol untuk mengeksekusi perhitungan
if st.button("Hitung Transaksi", type="primary"):
    
    # 1. Menentukan Persentase Diskon
    if total_belanja >= 80000000:
        diskon_persen = 0.20
    elif total_belanja >= 45000000:
        diskon_persen = 0.14
    elif total_belanja >= 35000000:
        diskon_persen = 0.12
    elif total_belanja >= 25000000:
        diskon_persen = 0.10
    else:
        diskon_persen = 0.0

    # 2. Menghitung Pembayaran
    nominal_diskon = int(total_belanja * diskon_persen)
    total_bayar = total_belanja - nominal_diskon
    kembalian = uang_pembayaran - total_bayar

    # 3. Menampilkan Output ke Layar Web
    st.subheader("🧾 Struk Transaksi")
    
    if uang_pembayaran == 0 and total_belanja == 0:
        st.warning("Silakan masukkan nominal transaksi terlebih dahulu.")
    elif kembalian < 0:
        st.error(f"Transaksi Gagal! Uang konsumen kurang Rp {abs(kembalian):,}".replace(",", "."))
    else:
        # Menampilkan rincian bayar dalam kotak metrik yang elegan
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Belanja", f"Rp {total_belanja:,}".replace(",", "."))
        col2.metric(f"Diskon ({int(diskon_persen*100)}%)", f"Rp {nominal_diskon:,}".replace(",", "."))
        col3.metric("Total Bayar", f"Rp {total_bayar:,}".replace(",", "."))
        
        st.success(f"**Kembalian: Rp {kembalian:,}**".replace(",", "."))
        
        # Proses Pemisahan Uang
        st.write("**Rincian Pecahan Kembalian:**")
        daftar_pecahan = [100000, 50000, 20000, 10000, 5000, 2000, 1000, 500, 100, 50]
        sisa_kembalian = kembalian
        
        for pecahan in daftar_pecahan:
            jumlah_lembar = sisa_kembalian // pecahan
            sisa_kembalian = sisa_kembalian % pecahan
            
            if jumlah_lembar > 0:
                satuan = "lembar" if pecahan >= 1000 else "keping"
                st.info(f"Rp {pecahan:,}".replace(",", ".") + f" : {jumlah_lembar} {satuan}")

