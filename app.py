import streamlit as st
import pandas as pd
import math # Import math untuk pembulatan ke atas

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Aplikasi Split Data Arsitek (Batch Download)", layout="wide", page_icon="🏗️")

# =============================================================================
# 1. DATABASE KOTA (DATABASE ULTIMATE)
# =============================================================================
DATABASE_KOTA = [
    # --- DAERAH KHUSUS & UNIK ---
    "Kuala Kencana", "Rengasdengklok", "Baturaden", "Rantau Prapat", "Rantauprapat",
    "Ujung Batu", "Bagan Batu", "Pasir Pengaraian", "Pangkalan Kerinci",
    "Ampana", "Woha", "Mandalika", "Cipatat", "Kroya", "Wates", "Bangil", 
    "Cepu", "Ungaran", "Ambarawa", "Majenang", "Gombong", "Karanganyar",
    "Painan", "Sipirok", "Sidempuan", "Padang Sidempuan", "Sibuhuan",
    "Gunung Tua", "Panyabungan", "Kotanopan", "Barus", "Pandan", 
    "Tarutung", "Balige", "Dolok Sanggul", "Pangururan", "Sidikalang",
    "Kabanjahe", "Berastagi", "Stabat", "Tanjung Morawa", "Lubuk Pakam",
    "Perbaungan", "Sei Rampah", "Indrapura", "Lima Puluh", "Kisaran",
    "Aek Kanopan", "Kota Pinang", "Gunung Sitoli", "Gunungsitoli",
    "Teluk Dalam", "Lahomi", "Lotu", "Tuhemberua", "Gido", 
    "Sidenreng Rappang", "Pangkajene", "Watansoppeng", "Belopa", "Malili",
    "Masamba", "Makale", "Rantepao", "Benteng", "Bulukumba", "Bantaeng",
    "Jeneponto", "Takalar", "Sungguminasa", "Maros", "Pangkep", "Barru",
    "Pinrang", "Enrekang", "Parepare", "Palopo", "Watampone", "Sengkang",
    "Kuala Tungkal", "Muara Bulian", "Muara Bungo", "Bangko", "Sarolangun",
    
    # --- PAPUA & MALUKU ---
    "Intan Jaya", "Dogiyai", "Deiyai", "Paniai", "Nabire", "Puncak Jaya", 
    "Puncak", "Lanny Jaya", "Tolikara", "Mamberamo", "Yalimo", "Jayawijaya", 
    "Wamena", "Nduga", "Yahukimo", "Pegunungan Bintang", "Boven Digoel", 
    "Mappi", "Asmat", "Mimika", "Timika", "Sarmi", "Keerom", "Waropen", 
    "Kepulauan Yapen", "Biak", "Numfor", "Supiori", "Mamberamo Raya", 
    "Jayapura", "Sentani", "Merauke", "Sorong", "Manokwari", "Fakfak", 
    "Kaimana", "Teluk Bintuni", "Teluk Wondama", "Raja Ampat", "Tambrauw", 
    "Maybrat", "Sorong Selatan", "Tual", "Maluku", "Ambon", "Ternate", "Tidore",

    # --- KAWASAN SEO (JABODETABEK & SEKITARNYA) ---
    "Jabodetabek", "Bintaro", "BSD", "BSD City", "Cibubur", "Kelapa Gading", 
    "Pantai Indah Kapuk", "PIK", "Sentul", "Cileungsi", "Cikarang", "Karawang", 
    "Cikampek", "Jababeka", "Meikarta", "Harapan Indah", "Summarecon", "Alam Sutera",
    "Gading Serpong", "Lippo Karawaci", "Citra Raya", "Kota Baru Parahyangan",
    "Jakarta", "Bogor", "Depok", "Tangerang", "Bekasi", "Bandung", "Cimahi",
    "Cianjur", "Sukabumi", "Tasikmalaya", "Ciamis", "Garut", "Cirebon", "Kuningan",
    "Indramayu", "Majalengka", "Subang", "Purwakarta", "Sumedang", "Banjar",
    "Pangandaran", "Serang", "Cilegon", "Pandeglang", "Lebak", 

    # --- JAWA TENGAH & TIMUR ---
    "Semarang", "Yogyakarta", "Jogja", "Solo", "Surakarta", "Malang", "Batu",
    "Surabaya", "Sidoarjo", "Gresik", "Lamongan", "Tuban", "Bojonegoro", "Ngawi", 
    "Madiun", "Magetan", "Ponorogo", "Pacitan", "Trenggalek", "Tulungagung", "Blitar",
    "Kediri", "Pare", "Nganjuk", "Jombang", "Mojokerto", "Pasuruan", "Probolinggo",
    "Lumajang", "Jember", "Bondowoso", "Situbondo", "Banyuwangi", "Bangkalan",
    "Sampang", "Pamekasan", "Sumenep", "Madura", "Pekalongan", "Tegal", "Brebes", 
    "Pemalang", "Batang", "Kendal", "Demak", "Grobogan", "Purwodadi", "Blora", 
    "Rembang", "Pati", "Kudus", "Jepara", "Temanggung", "Wonosobo", "Purworejo", 
    "Kebumen", "Cilacap", "Purwokerto", "Banyumas", "Banjarnegara", "Purbalingga", 
    "Klaten", "Boyolali", "Sragen", "Sukoharjo", "Wonogiri", "Sleman", "Bantul", 
    "Gunung Kidul", "Kulon Progo",

    # --- SUMATERA ---
    "Banda Aceh", "Medan", "Padang", "Pekanbaru", "Jambi", "Palembang", "Bengkulu",
    "Bandar Lampung", "Pangkal Pinang", "Tanjung Pinang", "Batam", "Lhokseumawe",
    "Langsa", "Binjai", "Tebing Tinggi", "Pematang Siantar", "Sibolga", "Dumai",
    "Prabumulih", "Lubuklinggau", "Pagar Alam", "Metro", "Subulussalam", "Sabang",
    "Sungaipenuh", "Sungai Penuh", "Solok", "Sawahlunto", "Pariaman", "Payakumbuh",
    "Bukittinggi", "Padang Panjang",

    # --- KALIMANTAN, SULAWESI, BALI, NTB, NTT ---
    "Pontianak", "Palangkaraya", "Banjarmasin", "Samarinda", "Tanjung Selor", "Manado", 
    "Palu", "Makassar", "Kendari", "Gorontalo", "Mamuju", "Denpasar", "Mataram", "Kupang",
    "Tarakan", "Balikpapan", "Bontang", "Singkawang", "Banjarbaru", "Baubau", "Kotamobagu",
    "Tomohon", "Bitung", "Bima"
]

DATABASE_SORTED = sorted(DATABASE_KOTA, key=len, reverse=True)

# =============================================================================
# 2. FUNGSI LOAD DATA ANTI-ERROR
# =============================================================================
@st.cache_data
def load_data_robust(file):
    try:
        return pd.read_csv(file)
    except:
        pass
    try:
        file.seek(0)
        return pd.read_csv(file, sep=';')
    except:
        pass
    try:
        file.seek(0)
        return pd.read_csv(file, sep=None, engine='python', on_bad_lines='skip')
    except Exception as e:
        return None

# =============================================================================
# 3. LOGIKA PEMROSESAN DATA
# =============================================================================
@st.cache_data
def scan_data(df):
    col_name = 'Title' if 'Title' in df.columns else df.columns[0]
    df[col_name] = df[col_name].astype(str)
    
    def get_city(text):
        t = str(text).lower()
        for kota in DATABASE_SORTED:
            if kota.lower() in t:
                return kota 
        return "Tidak Terdeteksi"
    
    def get_category(text):
        t = str(text).lower()
        if 'masjid' in t or 'musholla' in t: return "🕌 Proyek Masjid"
        if '3d' in t or 'render' in t: return "🖥️ Visualisasi 3D"
        if 'interior' in t: return "🛋️ Interior Design"
        if 'renovasi' in t: return "🔨 Renovasi Rumah"
        if 'bangun' in t or 'kontraktor' in t: return "🏗️ Konstruksi & Bangun"
        if 'biaya' in t or 'konsultasi' in t or 'rab' in t: return "💰 Konsultasi & Biaya"
        if 'desain' in t or 'arsitek' in t: return "🏠 Jasa Desain Arsitek"
        return "📂 Umum/Lainnya"

    df['Kota_Terdeteksi'] = df[col_name].apply(get_city)
    df['Kategori_Jasa'] = df[col_name].apply(get_category)
    return df

# =============================================================================
# 4. TAMPILAN APLIKASI (USER INTERFACE)
# =============================================================================
st.title("Aplikasi Split Data Arsitek (Batch System)")
st.markdown("""
Aplikasi ini akan memfilter data, lalu **memecahnya menjadi beberapa bagian (batch)**.
Anda bebas menentukan **jumlah baris per file**, lalu download secara berurutan.
""")

uploaded_file = st.file_uploader("Upload File CSV di sini", type=["csv"])

if uploaded_file:
    df_raw = load_data_robust(uploaded_file)
    
    if df_raw is not None:
        total_baris = len(df_raw)
        st.info(f"📂 File terbaca. Total Data Awal: **{total_baris} baris**.")
        
        with st.spinner('Sedang memproses data...'):
            df_hasil = scan_data(df_raw)
        
        st.success("✅ Proses Scan Selesai!")
        st.divider()
        
        # --- SIDEBAR MENU (FILTER) ---
        st.sidebar.header("🎛️ Filter Data")
        
        # 1. Filter Kota
        list_kota = sorted(df_hasil[df_hasil['Kota_Terdeteksi'] != "Tidak Terdeteksi"]['Kota_Terdeteksi'].unique())
        pilih_kota = st.sidebar.multiselect("📍 Pilih Kota:", list_kota)
        
        # 2. Filter Kategori
        list_kategori = sorted(df_hasil['Kategori_Jasa'].unique())
        pilih_kategori = st.sidebar.multiselect("🏷️ Pilih Kategori:", list_kategori)
        
        # 3. Filter Kata Kunci 'Jasa' (FITUR BARU)
        st.sidebar.markdown("---")
        st.sidebar.subheader("🔍 Filter Kata Kunci")
        filter_kata_jasa = st.sidebar.checkbox("✅ Hanya judul yang mengandung kata 'Jasa'", value=False)
        st.sidebar.caption("Jika dicentang, data tanpa kata 'jasa' akan dibuang.")
        
        # --- PROSES FILTER ---
        df_export = df_hasil.copy()
        
        if pilih_kota:
            df_export = df_export[df_export['Kota_Terdeteksi'].isin(pilih_kota)]
        if pilih_kategori:
            df_export = df_export[df_export['Kategori_Jasa'].isin(pilih_kategori)]
            
        # Logika Filter Kata 'Jasa'
        if filter_kata_jasa:
            # Tentukan kolom judul secara dinamis (sama seperti saat scan)
            col_name_filter = 'Title' if 'Title' in df_export.columns else df_export.columns[0]
            # Filter yang mengandung 'jasa' (case insensitive)
            df_export = df_export[df_export[col_name_filter].str.contains("jasa", case=False, na=False)]
            
        total_filtered = len(df_export)
        
        # --- PENGATURAN BATCH / PEMBAGIAN DATA ---
        st.subheader(f"📊 Total Hasil Filter: {total_filtered} Data")
        
        if total_filtered > 0:
            st.markdown("### ✂️ Pengaturan Pembagian Data (Batch)")
            
            # --- INPUT USER: BERAPA ROW PER FILE ---
            batch_size = st.number_input(
                "Ingin berapa baris data per file download? (Contoh: 50, 100, 500)", 
                min_value=1, 
                value=50, 
                step=10
            )
            
            # Hitung jumlah batch berdasarkan input user
            num_batches = math.ceil(total_filtered / batch_size)
            
            st.info(f"Dengan **{batch_size} baris per file**, data akan dibagi menjadi **{num_batches} file (batch)**. Silakan download di bawah ini.")
            
            st.markdown("---")
            st.subheader("📥 Download Area (Urut dari Atas ke Bawah)")
            
            # Identifikasi kolom Title yang asli
            col_name_asli = 'Title' if 'Title' in df_export.columns else df_export.columns[0]
            
            # --- LOOP MEMBUAT TOMBOL DOWNLOAD ---
            for i in range(num_batches):
                # Tentukan index awal dan akhir untuk batch ini berdasarkan input user
                start_idx = i * batch_size
                end_idx = min((i + 1) * batch_size, total_filtered)
                
                # Slice data (Potong data sesuai urutan)
                df_batch = df_export.iloc[start_idx:end_idx]
                
                # Hanya ambil kolom Title (Sesuai Request)
                df_final_download = df_batch[[col_name_asli]]
                
                # Konversi ke CSV
                csv_data = df_final_download.to_csv(index=False).encode('utf-8')
                
                # Buat nama file yang unik dan informatif
                file_label = f"Batch {i+1} (Data ke-{start_idx+1} s/d {end_idx})"
                file_name_download = f"Data_Arsitek_Batch_{i+1}_{start_idx+1}_to_{end_idx}.csv"
                
                # Tampilkan Tombol dalam Expander agar rapi
                with st.expander(f"📦 **{file_label}** - Klik untuk buka"):
                    st.write(f"Berisi {len(df_final_download)} baris data title.")
                    st.dataframe(df_final_download.head(3), use_container_width=True) # Preview kecil
                    st.caption("... (preview 3 data teratas)")
                    
                    st.download_button(
                        label=f"⬇️ Download {file_label}",
                        data=csv_data,
                        file_name=file_name_download,
                        mime="text/csv",
                        type="primary",
                        key=f"btn_{i}" # Key unik agar tombol tidak bentrok
                    )
        else:
            st.warning("⚠️ Tidak ada data yang ditemukan dengan filter tersebut.")
            
    else:
        st.error("⚠️ Gagal membaca file CSV.")
