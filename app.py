import streamlit as st
import pandas as pd
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Aplikasi Filter Data Arsitek (CSV Output)", layout="wide", page_icon="🏗️")

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
# 4. UI HALAMAN
# =============================================================================
st.title("Aplikasi Sortir Data Arsitek (Database Lengkap)")
st.markdown("Upload file CSV Anda. Aplikasi akan membaca **seluruh baris data** dan mendeteksi lokasinya.")

uploaded_file = st.file_uploader("Upload File CSV di sini", type=["csv"])

if uploaded_file:
    df_raw = load_data_robust(uploaded_file)
    
    if df_raw is not None:
        total_baris = len(df_raw)
        st.info(f"📂 File berhasil dibaca! Total Data ditemukan: **{total_baris} baris**.")
        
        with st.spinner(f'Sedang memproses deteksi kota untuk {total_baris} data...'):
            df_hasil = scan_data(df_raw)
        
        st.success("✅ Deteksi Selesai!")
        st.divider()
        
        # --- SIDEBAR MENU ---
        st.sidebar.header("🎛️ Menu Filter")
        
        list_kota = sorted(df_hasil[df_hasil['Kota_Terdeteksi'] != "Tidak Terdeteksi"]['Kota_Terdeteksi'].unique())
        pilih_kota = st.sidebar.multiselect("📍 Pilih Kota:", list_kota)
        
        list_kategori = sorted(df_hasil['Kategori_Jasa'].unique())
        pilih_kategori = st.sidebar.multiselect("🏷️ Pilih Kategori:", list_kategori)
        
        limit = st.sidebar.number_input("🔢 Preview Berapa Baris?", min_value=1, value=50)
        
        # --- PROSES FILTER ---
        df_export = df_hasil.copy()
        
        if pilih_kota:
            df_export = df_export[df_export['Kota_Terdeteksi'].isin(pilih_kota)]
        if pilih_kategori:
            df_export = df_export[df_export['Kategori_Jasa'].isin(pilih_kategori)]
        
        # --- TAMPILAN HASIL ---
        st.subheader(f"📋 Hasil Filter: {len(df_export)} Data Terpilih")
        
        st.dataframe(df_export.head(limit), use_container_width=True)
        if len(df_export) > limit:
            st.caption(f"*Menampilkan {limit} baris pertama dari {len(df_export)} data hasil filter.*")

        # --- DOWNLOAD BUTTON (CSV) ---
        # Konversi dataframe ke CSV string
        csv_data = df_export.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="📥 Download Semua Hasil Filter (CSV)",
            data=csv_data,
            file_name="Data_Arsitek_Terfilter.csv",
            mime="text/csv",
            type="primary"
        )
            
    else:
        st.error("⚠️ Gagal membaca file. Pastikan file CSV tidak rusak.")