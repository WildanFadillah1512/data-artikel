import streamlit as st
import pandas as pd
import io

# --- KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Aplikasi Filter Data Arsitek", layout="wide", page_icon="🏗️")

# =============================================================================
# 1. DATABASE KOTA (Daftar Lengkap Seluruh Indonesia & Area SEO)
# =============================================================================
DATABASE_KOTA = [
    # --- KAWASAN KHUSUS (SEO) ---
    "Jabodetabek", "Bintaro", "BSD", "BSD City", "Cibubur", "Kelapa Gading", 
    "Pantai Indah Kapuk", "PIK", "Sentul", "Cileungsi", "Cikarang", "Karawang", 
    "Cikampek", "Jababeka", "Meikarta", "Harapan Indah", "Summarecon", "Alam Sutera",
    "Gading Serpong", "Lippo Karawaci", "Citra Raya", "Kota Baru Parahyangan",
    
    # --- SUMATERA ---
    "Banda Aceh", "Sabang", "Lhokseumawe", "Langsa", "Subulussalam", "Meulaboh", "Aceh",
    "Medan", "Binjai", "Pematang Siantar", "Tebing Tinggi", "Sibolga", "Tanjungbalai", 
    "Gunungsitoli", "Padang Sidempuan", "Deli Serdang", "Karo", "Nias", "Samosir",
    "Padang", "Bukittinggi", "Pariaman", "Padang Panjang", "Payakumbuh", "Solok", "Sawahlunto",
    "Pekanbaru", "Dumai", "Riau", "Bengkalis", "Indragiri", "Kampar", "Kuantan Singingi", "Pelalawan", "Rokan", "Siak",
    "Jambi", "Sungai Penuh", "Kerinci", "Merangin", "Batanghari", "Muaro Jambi",
    "Palembang", "Prabumulih", "Lubuklinggau", "Pagar Alam", "Banyuasin", "Empat Lawang", "Lahat", "Muara Enim", "Musi", "Ogan",
    "Bengkulu", "Muko-Muko", "Rejang Lebong", "Kaur",
    "Bandar Lampung", "Metro", "Lampung", "Pringsewu", "Tanggamus", "Way Kanan",
    "Pangkal Pinang", "Bangka", "Belitung", "Tanjung Pandan", "Muntok", "Sungailiat",
    "Batam", "Tanjung Pinang", "Bintan", "Karimun", "Natuna", "Lingga", "Anambas",

    # --- JAWA ---
    "Jakarta", "Jakarta Pusat", "Jakarta Utara", "Jakarta Barat", "Jakarta Selatan", "Jakarta Timur", "Kepulauan Seribu",
    "Bogor", "Sukabumi", "Cianjur", "Bandung", "Garut", "Tasikmalaya", "Ciamis", "Kuningan", "Cirebon", "Majalengka", 
    "Sumedang", "Indramayu", "Subang", "Purwakarta", "Karawang", "Bekasi", "Bandung Barat", "Pangandaran", "Depok", "Cimahi", "Banjar",
    "Semarang", "Salatiga", "Solo", "Surakarta", "Magelang", "Pekalongan", "Tegal", "Brebes", "Pemalang", "Batang", "Kendal", "Demak", 
    "Grobogan", "Purwodadi", "Blora", "Rembang", "Pati", "Kudus", "Jepara", "Temanggung", "Wonosobo", "Purworejo", "Kebumen", 
    "Cilacap", "Purwokerto", "Banyumas", "Banjarnegara", "Purbalingga", "Klaten", "Boyolali", "Sragen", "Sukoharjo", "Wonogiri", "Karanganyar",
    "Yogyakarta", "Jogja", "Bantul", "Sleman", "Gunung Kidul", "Kulon Progo",
    "Surabaya", "Sidoarjo", "Gresik", "Lamongan", "Tuban", "Bojonegoro", "Ngawi", "Madiun", "Magetan", "Ponorogo", "Pacitan", 
    "Trenggalek", "Tulungagung", "Blitar", "Kediri", "Pare", "Nganjuk", "Jombang", "Mojokerto", "Malang", "Batu", "Pasuruan", 
    "Probolinggo", "Lumajang", "Jember", "Bondowoso", "Situbondo", "Banyuwangi", "Bangkalan", "Sampang", "Pamekasan", "Sumenep", "Madura",
    "Serang", "Cilegon", "Tangerang", "Tangsel", "Tangerang Selatan", "Pandeglang", "Lebak",

    # --- BALI & NUSA TENGGARA ---
    "Denpasar", "Badung", "Kuta", "Gianyar", "Ubud", "Tabanan", "Buleleng", "Singaraja", "Jembrana", "Karangasem", "Klungkung", "Bangli", "Bali",
    "Mataram", "Bima", "Lombok", "Sumbawa", "Dompu", "Selong", "Praya",
    "Kupang", "Flores", "Sumba", "Alor", "Belu", "Ende", "Manggarai", "Labuan Bajo", "Rote", "Sikka", "Maumere", "Timor Tengah",

    # --- KALIMANTAN ---
    "Pontianak", "Singkawang", "Sambas", "Mempawah", "Sanggau", "Ketapang", "Sintang", "Kapuas Hulu", "Bengkayang", "Landak", "Sekadau", "Melawi", "Kayong", "Kubu Raya",
    "Palangkaraya", "Kotawaringin", "Sampit", "Pangkalan Bun", "Kapuas", "Barito", "Lamandau", "Seruyan", "Sukamara", "Gunung Mas", "Pulang Pisau", "Murung Raya",
    "Banjarmasin", "Banjarbaru", "Banjar", "Barito", "Tapin", "Hulu Sungai", "Tabalong", "Tanah Laut", "Tanah Bumbu", "Kotabaru", "Balangan",
    "Samarinda", "Balikpapan", "Bontang", "Kutai", "Tenggarong", "Sangatta", "Berau", "Pajam", "Mahakam",
    "Tarakan", "Bulungan", "Tanjung Selor", "Malinau", "Nunukan", "Tana Tidung", "IKN",

    # --- SULAWESI ---
    "Makassar", "Parepare", "Palopo", "Gowa", "Maros", "Bone", "Bulukumba", "Jeneponto", "Takalar", "Bantaeng", "Sinjai", "Soppeng", "Wajo", "Sidrap", "Pinrang", "Enrekang", "Luwu", "Toraja", "Selayar",
    "Manado", "Bitung", "Tomohon", "Kotamobagu", "Minahasa", "Bolaang Mongondow", "Sangihe", "Talaud",
    "Palu", "Donggala", "Poso", "Luwuk", "Banggai", "Buol", "Toli-Toli", "Morowali", "Parigi Moutong", "Tojo Una-Una", "Sigi",
    "Kendari", "Baubau", "Kolaka", "Konawe", "Muna", "Buton", "Wakatobi", "Bombana",
    "Gorontalo", "Boalemo", "Pohuwato",
    "Mamuju", "Majene", "Polewali Mandar", "Mamasa", "Pasangkayu",

    # --- MALUKU & PAPUA ---
    "Ambon", "Tual", "Maluku", "Buru", "Seram", "Aru", "Saumlaki", "Langgur",
    "Ternate", "Tidore", "Halmahera", "Morotai", "Sula",
    "Jayapura", "Sentani", "Sarmi", "Keerom", "Biak", "Yapen", "Nabire", "Mimika", "Timika", "Puncak Jaya", "Paniai", "Dogiyai", "Intan Jaya", "Deiyai",
    "Sorong", "Raja Ampat", "Manokwari", "Fakfak", "Kaimana", "Teluk Bintuni", "Teluk Wondama",
    "Merauke", "Boven Digoel", "Mappi", "Asmat", "Wamena", "Jayawijaya", "Yahukimo", "Pegunungan Bintang", "Tolikara", "Nduga", "Lanny Jaya", "Mamberamo", "Yalimo"
]

# Urutkan dari nama terpanjang agar deteksi akurat
DATABASE_SORTED = sorted(DATABASE_KOTA, key=len, reverse=True)

# =============================================================================
# 2. FUNGSI LOAD DATA ANTI-ERROR (ROBUST LOADER)
# =============================================================================
# Fungsi ini mencoba 3 cara membaca file agar tidak error
@st.cache_data
def load_data_robust(file):
    # Cara 1: Standard (Koma)
    try:
        return pd.read_csv(file)
    except:
        pass
    
    # Cara 2: Format Excel Indonesia (Titik Koma)
    try:
        file.seek(0)
        return pd.read_csv(file, sep=';')
    except:
        pass
    
    # Cara 3: Paksa Baca (Skip baris error)
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
    # Ambil kolom pertama sebagai referensi jika 'Title' tidak ada
    col_name = 'Title' if 'Title' in df.columns else df.columns[0]
    
    # Pastikan data berupa text (string)
    df[col_name] = df[col_name].astype(str)
    
    # Deteksi Kota
    def get_city(text):
        t = str(text).lower()
        for kota in DATABASE_SORTED:
            if kota.lower() in t:
                return kota 
        return "Tidak Terdeteksi"
    
    # Deteksi Kategori
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
# 4. TAMPILAN APLIKASI (UI)
# =============================================================================

st.title("Aplikasi Sortir Data Arsitek (Anti-Error)")
st.markdown("Upload file CSV Judul Anda, sistem akan mendeteksi **Kota** secara otomatis.")

uploaded_file = st.file_uploader("Upload File CSV di sini", type=["csv"])

if uploaded_file:
    # --- PROSES LOAD DATA (MENGGUNAKAN FUNGSI BARU) ---
    df_raw = load_data_robust(uploaded_file)
    
    if df_raw is not None:
        with st.spinner('Sedang memindai ribuan data...'):
            df_hasil = scan_data(df_raw)
        
        st.success(f"✅ Berhasil memproses {len(df_hasil)} baris data!")
        
        st.divider()
        
        # MENU FILTER (SIDEBAR)
        st.sidebar.header("🎛️ Menu Pilihan")
        
        # Pilihan Kota
        list_kota = sorted(df_hasil[df_hasil['Kota_Terdeteksi'] != "Tidak Terdeteksi"]['Kota_Terdeteksi'].unique())
        pilih_kota = st.sidebar.multiselect("📍 Pilih Kota:", list_kota)
        
        # Pilihan Kategori
        list_kategori = sorted(df_hasil['Kategori_Jasa'].unique())
        pilih_kategori = st.sidebar.multiselect("🏷️ Pilih Kategori:", list_kategori)
        
        # Limit Baris
        limit = st.sidebar.number_input("🔢 Ambil Berapa Baris?", min_value=1, value=50)
        
        # LOGIKA FILTER
        df_export = df_hasil.copy()
        
        if pilih_kota:
            df_export = df_export[df_export['Kota_Terdeteksi'].isin(pilih_kota)]
        if pilih_kategori:
            df_export = df_export[df_export['Kategori_Jasa'].isin(pilih_kategori)]
        
        # Batasi jumlah baris
        df_final = df_export.head(limit)
        
        # TAMPILAN HASIL
        st.subheader(f"📋 Hasil Filter: {len(df_final)} Data")
        st.dataframe(df_final, use_container_width=True)
        
        # TOMBOL DOWNLOAD
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            df_final.to_excel(writer, index=False, sheet_name='Data Filter')
            
        st.download_button(
            label="📥 Download Hasil (Excel)",
            data=buffer,
            file_name="Data_Arsitek_Pilihan.xlsx",
            mime="application/vnd.ms-excel",
            type="primary"
        )
    else:
        st.error("⚠️ Gagal membaca file CSV. Pastikan format file benar atau coba save as CSV UTF-8 di Excel.")