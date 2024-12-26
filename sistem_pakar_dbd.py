import streamlit as st

# Class untuk Gejala
class Gejala:
    def __init__(self, kode, deskripsi):
        self.kode = kode
        self.deskripsi = deskripsi

    def __str__(self):
        return self.deskripsi


# Class untuk Aturan (Rule)
class Rule:
    def __init__(self, kondisi, kesimpulan):
        self.kondisi = kondisi  # Kondisi adalah list gejala yang harus dipenuhi
        self.kesimpulan = kesimpulan  # Kesimpulan yang akan diambil jika kondisi terpenuhi


# Class untuk Sistem Pakar dengan Backward Chaining
class SistemPakarDBD:
    def __init__(self):
        self.gejala = {}  # Menyimpan daftar gejala
        self.aturan = []  # Menyimpan aturan (rule)

    # Menambah gejala baru
    def tambah_gejala(self, kode, deskripsi):
        self.gejala[kode] = Gejala(kode, deskripsi)

    # Menambah aturan baru
    def tambah_aturan(self, kondisi, kesimpulan):
        self.aturan.append(Rule(kondisi, kesimpulan))

    # Melakukan diagnosa berdasarkan gejala yang diberikan
    def diagnosa(self, gejala_terpenuhi):
        # Cari aturan yang seluruh kondisi-nya terpenuhi
        aturan_valid = [
            aturan for aturan in self.aturan
            if set(aturan.kondisi) == set(gejala_terpenuhi)
        ]

        # Jika tidak ada aturan yang valid
        if not aturan_valid:
            return "Gejala tidak mencukupi untuk diagnosis DBD. Silakan konsultasi lebih lanjut ke dokter."

        # Jika ada lebih dari satu aturan yang valid
        if len(aturan_valid) > 1:
            return (
                "Terdapat lebih dari satu kemungkinan diagnosis. "
                "Silakan konsultasi lebih lanjut ke dokter untuk memastikan."
            )

        # Jika hanya ada satu aturan yang valid
        return aturan_valid[0].kesimpulan


# Inisialisasi sistem pakar
sistem_pakar = SistemPakarDBD()
sistem_pakar.tambah_gejala("G01", "Demam berlangsung kurang dari 7 hari")
sistem_pakar.tambah_gejala("G02", "Demam hari keempat tubuh terasa lemas")
sistem_pakar.tambah_gejala("G03", "Di lingkungan sekitar ada yang terjangkit DBD")
sistem_pakar.tambah_gejala("G04", "Bintik merah pada tubuh")
sistem_pakar.tambah_gejala("G05", "Pendarahan spontan dalam tubuh (gusi/air seni kemerahan)")
sistem_pakar.tambah_gejala("G06", "Mual muntah")
sistem_pakar.tambah_gejala("G07", "Nyeri kepala")
sistem_pakar.tambah_gejala("G08", "Nyeri sendi")
sistem_pakar.tambah_gejala("G09", "Nyeri ulu hati atau perut bagian atas")
sistem_pakar.tambah_gejala("G10", "Tinja berwarna hitam")

sistem_pakar.tambah_aturan(["G01", "G02"], "Pasien mengalami Demam Berdarah ringan")
sistem_pakar.tambah_aturan(["G01", "G04"], "Pasien mengalami Demam Berdarah")
sistem_pakar.tambah_aturan(["G06", "G04"], "Pasien mengalami Demam Berdarah tingkat lanjut")
sistem_pakar.tambah_aturan(["G01", "G03", "G04"], "Pasien mengalami Demam Berdarah Dengue")
sistem_pakar.tambah_aturan(["G02", "G07", "G08"], "Pasien mengalami DBD ringan atau demam biasa")
sistem_pakar.tambah_aturan(["G06", "G09"], "Pasien mengalami DBD berat atau gangguan pencernaan lainnya")
sistem_pakar.tambah_aturan(["G10", "G05"], "Pasien mengalami komplikasi DBD berat (perdarahan dalam)")

# Tampilan sistem
st.title("Sistem Pakar Diagnosa DBD")
st.write("Selamat datang di sistem pakar diagnosa Demam Berdarah Dengue (DBD). Silakan mulai diagnosis untuk mengetahui kemungkinan kondisi Anda.")

# Session states untuk manajemen alur
if "page" not in st.session_state:
    st.session_state.page = 1

if "selected_gejala" not in st.session_state:
    st.session_state.selected_gejala = []

if "hasil_diagnosis" not in st.session_state:
    st.session_state.hasil_diagnosis = None

# Fungsi untuk memulai diagnosis
def start_diagnosis():
    st.session_state.page = 2
    st.session_state.selected_gejala = []
    st.session_state.hasil_diagnosis = None  # Reset hasil diagnosis saat memulai ulang

# Fungsi untuk memulai ulang diagnosis
def restart_diagnosis():
    st.session_state.page = 1
    st.session_state.selected_gejala = []
    st.session_state.hasil_diagnosis = None  # Reset hasil diagnosis saat memulai ulang

# Halaman 1: Memulai Diagnosis
if st.session_state.page == 1:
    if st.button("Mulai Diagnosis"):
        start_diagnosis()

# Halaman 2: Memilih Gejala
if st.session_state.page == 2:
    st.subheader("Pilih Gejala yang Anda Alami")
    for kode, gejala in sistem_pakar.gejala.items():
        # Menggunakan radio button untuk memilih ya/tidak
        pilihan = st.radio(f"{gejala.deskripsi}", options=["Ya", "Tidak"], key=f"radio_{kode}")
        if pilihan == "Ya":
            if kode not in st.session_state.selected_gejala:
                st.session_state.selected_gejala.append(kode)
        elif kode in st.session_state.selected_gejala:
            st.session_state.selected_gejala.remove(kode)

    if st.button("Lihat Hasil Diagnosis"):
        # Proses diagnosis dan pindah ke halaman 3
        hasil = sistem_pakar.diagnosa(st.session_state.selected_gejala)
        st.session_state.hasil_diagnosis = hasil
        st.session_state.page = 3  # Beralih ke halaman hasil diagnosis

# Halaman 3: Hasil Diagnosis
if st.session_state.page == 3:
    st.subheader("Hasil Diagnosis")
    st.write(st.session_state.hasil_diagnosis)
    if st.button("Mulai Ulang Diagnosis"):
        restart_diagnosis()  # Memulai ulang diagnosis setelah tombol ditekan
