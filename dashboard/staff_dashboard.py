import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from dashboard.staff_add import TambahBarangPage
from dashboard.staff_edit import EditBarangPage
from dashboard.staff_receive import FormPenerimaanPage
from dashboard.tabel_penerimaan import TabelPenerimaanPage


class StaffDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Staff - Manajemen ATK")
        self.geometry("950x800")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Buat frame utama scrollable (container besar)
        self.container = ctk.CTkScrollableFrame(self, width=930, height=780)
        self.container.pack(padx=10, pady=10, fill="both", expand=True)

        # Konten utama di dalam container scrollable
        ctk.CTkLabel(
            self.container, text="Dashboard Staff", font=("Arial Bold", 22)
        ).pack(pady=10)

        # Frame daftar barang
        self.table_frame = ctk.CTkScrollableFrame(self.container, height=250)
        self.table_frame.pack(pady=10, fill="both", expand=False)

        # Tombol-tombol utama
        button_frame = ctk.CTkFrame(self.container)
        button_frame.pack(pady=10)
        ctk.CTkButton(
            button_frame, text="Tambah Barang", command=self.tambah_barang
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            button_frame, text="Penerimaan Barang", command=self.buka_form_penerimaan
        ).pack(side="left", padx=10)
        ctk.CTkButton(
            self.container, text="Lihat Penerimaan", command=self.buka_tabel_penerimaan
        ).pack(pady=10)

        # Label dan frame daftar permintaan
        ctk.CTkLabel(
            self.container, text="Daftar Request Pinjam", font=("Arial Bold", 18)
        ).pack(pady=(20, 5))
        self.request_frame = ctk.CTkScrollableFrame(self.container, height=250)
        self.request_frame.pack(pady=5, fill="both", expand=False)

        ctk.CTkLabel(
            self.container, text="Daftar Pengeluaran Barang", font=("Arial Bold", 18)
        ).pack(pady=(20, 5))
        self.pengeluaran_frame = ctk.CTkScrollableFrame(self.container, height=250)
        self.pengeluaran_frame.pack(pady=5, fill="both", expand=False)

        self.load_data()

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

        data = []
        for result in cursor.stored_results():
            data = result.fetchall()
        conn.close()

        headers = [
            "Kode",
            "Nama Barang",
            "Stok",
            "Merek",
            "Satuan",
            "Aksi Edit",
            "Aksi Hapus",
        ]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self.table_frame, text=header, font=("Arial Bold", 12)).grid(
                row=0, column=col, padx=10, pady=5, sticky="w"
            )

        for row, item in enumerate(data, start=1):
            kode_barang, nama, stok, merek, satuan = item
            ctk.CTkLabel(self.table_frame, text=kode_barang).grid(
                row=row, column=0, padx=10, pady=5
            )
            ctk.CTkLabel(self.table_frame, text=nama).grid(
                row=row, column=1, padx=10, pady=5
            )
            ctk.CTkLabel(self.table_frame, text=stok).grid(
                row=row, column=2, padx=10, pady=5
            )
            ctk.CTkLabel(self.table_frame, text=merek or "-").grid(
                row=row, column=3, padx=10, pady=5
            )
            ctk.CTkLabel(self.table_frame, text=satuan or "-").grid(
                row=row, column=4, padx=10, pady=5
            )

            edit_btn = ctk.CTkButton(
                self.table_frame,
                text="Edit",
                fg_color="blue",
                command=lambda k=kode_barang: self.edit_barang(k),
            )
            edit_btn.grid(row=row, column=5, padx=5, pady=5)
            hapus_btn = ctk.CTkButton(
                self.table_frame,
                text="Hapus",
                fg_color="red",
                command=lambda k=kode_barang: self.hapus_barang(k),
            )
            hapus_btn.grid(row=row, column=6, padx=5, pady=5)

        for col in range(len(headers)):
            self.table_frame.grid_columnconfigure(col, weight=1)

    def load_permintaan(self):
        for widget in self.request_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT dp.id_permintaan, b.nama_barang, dp.jumlah, p.status, p.id_pemohon
        FROM detail_permintaan dp
        JOIN permintaan p ON dp.id_permintaan = p.id_permintaan
        JOIN barang b ON dp.kode_barang = b.kode_barang
        ORDER BY p.tgl_permintaan DESC
        """
        cursor.execute(query)
        requests = cursor.fetchall()
        conn.close()

        headers = ["ID Permintaan", "Nama Barang", "Jumlah", "Status", "ID Pemohon"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self.request_frame, text=header, font=("Arial Bold", 12)).grid(
                row=0, column=col, padx=10, pady=5, sticky="w"
            )

        for row, item in enumerate(requests, start=1):
            id_perm, nama_barang, jumlah, status, id_pemohon = item
            ctk.CTkLabel(self.request_frame, text=id_perm).grid(
                row=row, column=0, padx=10, pady=5
            )
            ctk.CTkLabel(self.request_frame, text=nama_barang).grid(
                row=row, column=1, padx=10, pady=5
            )
            ctk.CTkLabel(self.request_frame, text=jumlah).grid(
                row=row, column=2, padx=10, pady=5
            )
            ctk.CTkLabel(self.request_frame, text=status).grid(
                row=row, column=3, padx=10, pady=5
            )
            ctk.CTkLabel(self.request_frame, text=id_pemohon).grid(
                row=row, column=4, padx=10, pady=5
            )

        for col in range(len(headers)):
            self.request_frame.grid_columnconfigure(col, weight=1)

    def load_pengeluaran(self):
        for widget in self.pengeluaran_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()

        query = """
        SELECT id_pengeluaran, kode_barang, jml_keluar, tgl_keluar, tujuan, id_pemohon, id_petugas
        FROM pengeluaran
        ORDER BY tgl_keluar DESC
        """
        cursor.execute(query)
        pengeluaran_data = cursor.fetchall()
        conn.close()

        headers = [
            "ID Pengeluaran",
            "Kode Barang",
            "Jumlah",
            "Tanggal",
            "Tujuan",
            "ID Pemohon",
            "ID Petugas",
        ]
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                self.pengeluaran_frame, text=header, font=("Arial Bold", 12)
            ).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        for row, item in enumerate(pengeluaran_data, start=1):
            for col, val in enumerate(item):
                ctk.CTkLabel(self.pengeluaran_frame, text=val).grid(
                    row=row, column=col, padx=10, pady=5
                )

        for col in range(len(headers)):
            self.pengeluaran_frame.grid_columnconfigure(col, weight=1)

    def tambah_barang(self):
        TambahBarangPage()

    def edit_barang(self, kode_barang):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.callproc("lihat_barang_satu", (kode_barang,))
        data = None
        for result in cursor.stored_results():
            data = result.fetchone()
        conn.close()
        if data:
            nama_awal, stok_awal, merek_awal, satuan_awal = data
            EditBarangPage(kode_barang, nama_awal, stok_awal, merek_awal, satuan_awal)
        else:
            messagebox.showerror(
                "Error", f"Data barang dengan kode {kode_barang} tidak ditemukan."
            )

    def hapus_barang(self, kode_barang):
        confirm = messagebox.askyesno(
            "Konfirmasi", f"Yakin ingin menghapus barang {kode_barang}?"
        )
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.callproc("hapus_barang", (kode_barang,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Barang berhasil dihapus.")
            self.load_data()

    def buka_form_penerimaan(self):
        FormPenerimaanPage()

    def buka_tabel_penerimaan(self):
        TabelPenerimaanPage(self)
