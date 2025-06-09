import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from dashboard.staff_add import TambahBarangPage
from dashboard.staff_edit import EditBarangPage
from dashboard.staff_receive import FormPenerimaanPage
from dashboard.tabel_penerimaan import TabelPenerimaanPage
from dashboard.update_pengeluaran import EditPengeluaranPage
from dashboard.form_permintaan import FormPermintaanPage


class StaffDashboard(ctk.CTk):
    def __init__(self, id_petugas=None, nama_petugas=None):
        super().__init__()
        self.title("Dashboard Petugas - Manajemen ATK")
        self.geometry("950x800")
        self.resizable(False, False)
        self.id_petugas = id_petugas
        self.nama_petugas = nama_petugas

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.container = ctk.CTkScrollableFrame(self, width=930, height=780)
        self.container.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(
            self.container, text="Dashboard Petugas", font=("Arial Bold", 22)
        ).pack(pady=(0, 15), padx=10, anchor="w")

        button_frame = ctk.CTkFrame(self.container)
        button_frame.pack(pady=(0, 20), padx=10, anchor="w")

        ctk.CTkButton(
            button_frame, text="Tambah Barang", command=self.tambah_barang
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            button_frame, text="Penerimaan Barang", command=self.buka_form_penerimaan
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            button_frame, text="Lihat Penerimaan", command=self.buka_tabel_penerimaan
        ).pack(side="left", padx=5)

        # Buat section dengan margin dan padding teratur
        self.table_frame = self.create_section("Daftar Barang")
        self.request_frame = self.create_section("Daftar Request Pinjam")
        self.pengeluaran_frame = self.create_section("Daftar Pengeluaran Barang")

        self.load_data()

    def create_section(self, title):
        section_wrapper = ctk.CTkFrame(self.container)
        section_wrapper.pack(pady=20, padx=10, fill="x")

        ctk.CTkLabel(
            section_wrapper,
            text=title,
            font=("Arial Bold", 18),
            anchor="w",
            justify="left",
        ).pack(anchor="w", padx=10, pady=(5, 10))

        table_frame = ctk.CTkScrollableFrame(section_wrapper, height=250)
        table_frame.pack(padx=10, fill="x")

        return table_frame

    def load_data(self):
        self.load_barang()
        self.load_permintaan()
        self.load_pengeluaran()

    def load_barang(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.callproc("lihat_barang")
        data = [row for result in cursor.stored_results() for row in result.fetchall()]
        conn.close()

        headers = ["Kode", "Nama Barang", "Stok", "Merek", "Satuan", "Edit", "Hapus"]
        self.build_table(self.table_frame, headers, data, self.build_barang_row)

    def build_barang_row(self, frame, row_index, item):
        kode, nama, stok, merek, satuan = item
        values = [kode, nama, stok, merek or "-", satuan or "-"]
        for col, val in enumerate(values):
            ctk.CTkLabel(frame, text=val).grid(
                row=row_index, column=col, padx=5, pady=3
            )
        ctk.CTkButton(
            frame, text="Edit", fg_color="blue", command=lambda: self.edit_barang(kode)
        ).grid(row=row_index, column=5, padx=5)
        ctk.CTkButton(
            frame, text="Hapus", fg_color="red", command=lambda: self.hapus_barang(kode)
        ).grid(row=row_index, column=6, padx=5)

    def edit_barang(self, kode_barang):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT nama_barang, stok, merek, satuan FROM barang WHERE kode_barang = %s",
            (kode_barang,),
        )
        result = cursor.fetchone()
        conn.close()

        if result:
            nama, stok, merek, satuan = result
            EditBarangPage(kode_barang, nama, stok, merek, satuan)
            self.after(500, self.load_barang)
        else:
            messagebox.showerror("Error", "Barang tidak ditemukan.")

    def hapus_barang(self, kode_barang):
        confirm = messagebox.askyesno(
            "Konfirmasi", f"Yakin ingin menghapus barang {kode_barang}?"
        )
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM barang WHERE kode_barang = %s", (kode_barang,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Barang berhasil dihapus.")
            self.load_barang()

    def load_permintaan(self):
        for widget in self.request_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT 
                p.id_permintaan,
                p.tgl_permintaan,
                p.status,
                pemohon.id_pengguna AS id_pemohon,
                pemohon.nama_lengkap AS nama_pemohon
            FROM permintaan p
            LEFT JOIN pengguna pemohon ON p.id_pemohon = pemohon.id_pengguna
            WHERE p.status = 'Menunggu'
            ORDER BY p.tgl_permintaan DESC
            """
        )
        data = cursor.fetchall()
        conn.close()

        headers = [
            "ID Permintaan",
            "Tanggal Permintaan",
            "Status",
            "ID Pemohon",
            "Nama Pemohon",
            "Proses",
            "Hapus",
        ]
        self.build_table(self.request_frame, headers, data, self.build_request_row)

    def build_request_row(self, frame, row_index, item):
        id_permintaan, tgl_permintaan, status, id_pemohon, nama_pemohon = item
        values = [id_permintaan, tgl_permintaan, status, id_pemohon, nama_pemohon]
        for col, val in enumerate(values):
            ctk.CTkLabel(frame, text=val).grid(
                row=row_index, column=col, padx=5, pady=3
            )
        ctk.CTkButton(
            frame,
            text="Proses",
            fg_color="green",
            command=lambda: FormPermintaanPage(
                id_permintaan, self.id_petugas, self.nama_petugas, self.load_data
            ),
        ).grid(row=row_index, column=5, padx=5)
        ctk.CTkButton(
            frame,
            text="Hapus",
            fg_color="red",
            command=lambda: self.hapus_permintaan(id_permintaan),
        ).grid(row=row_index, column=6, padx=5)

    def hapus_permintaan(self, id_permintaan):
        confirm = messagebox.askyesno(
            "Konfirmasi", f"Yakin ingin menghapus permintaan ID {id_permintaan}?"
        )
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM permintaan WHERE id_permintaan = %s", (id_permintaan,)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Permintaan berhasil dihapus.")
            self.load_permintaan()

    def load_pengeluaran(self):
        for widget in self.pengeluaran_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.callproc("lihat_pengeluaran")
        data = [row for result in cursor.stored_results() for row in result.fetchall()]
        conn.close()

        headers = [
            "ID",
            "Kode",
            "Jumlah",
            "Tanggal",
            "Tujuan",
            "Pemohon",
            "Petugas",
        ]
        self.build_table(
            self.pengeluaran_frame, headers, data, self.build_pengeluaran_row
        )

    def build_pengeluaran_row(self, frame, row_index, item):
        # Sesuaikan sesuai data kolom, tanpa tombol edit & hapus
        for col, val in enumerate(item):
            ctk.CTkLabel(frame, text=val).grid(
                row=row_index, column=col, padx=5, pady=3
            )

    def tambah_barang(self):
        TambahBarangPage(self.load_barang)

    def buka_form_penerimaan(self):
        FormPenerimaanPage(self.load_data)

    def buka_tabel_penerimaan(self):
        TabelPenerimaanPage()

    def build_table(self, frame, headers, data, row_builder=None):
        for col, header in enumerate(headers):
            ctk.CTkLabel(frame, text=header, font=("Arial Bold", 12)).grid(
                row=0, column=col, padx=5, pady=3, sticky="w"
            )
        frame.grid_columnconfigure(col, weight=1)

        for row_index, item in enumerate(data, start=1):
            if row_builder:
                row_builder(frame, row_index, item)
