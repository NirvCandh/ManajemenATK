import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from dashboard.staff_add import TambahBarangPage
from dashboard.staff_edit import EditBarangPage
from dashboard.staff_receive import FormPenerimaanPage
from dashboard.tabel_penerimaan import TabelPenerimaanPage
from dashboard.update_pengeluaran import EditPengeluaranPage


class StaffDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Dashboard Petugas - Manajemen ATK")
        self.geometry("950x800")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.container = ctk.CTkScrollableFrame(self, width=930, height=780)
        self.container.pack(padx=10, pady=10, fill="both", expand=True)

        ctk.CTkLabel(
            self.container, text="Dashboard Petugas", font=("Arial Bold", 22)
        ).pack(pady=10)

        button_frame = ctk.CTkFrame(self.container)
        button_frame.pack(pady=10)

        ctk.CTkButton(
            button_frame, text="Tambah Barang", command=self.tambah_barang
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            button_frame, text="Penerimaan Barang", command=self.buka_form_penerimaan
        ).pack(side="left", padx=5)
        ctk.CTkButton(
            button_frame, text="Lihat Penerimaan", command=self.buka_tabel_penerimaan
        ).pack(side="left", padx=5)

        self.create_section_label("Daftar Barang")
        self.table_frame = self.create_table_frame()

        self.create_section_label("Daftar Request Pinjam")
        self.request_frame = self.create_table_frame()

        self.create_section_label("Daftar Pengeluaran Barang")
        self.pengeluaran_frame = self.create_table_frame()

        self.load_data()

    def create_section_label(self, text):
        ctk.CTkLabel(self.container, text=text, font=("Arial Bold", 18)).pack(
            pady=(15, 5)
        )

    def create_table_frame(self):
        frame = ctk.CTkScrollableFrame(self.container, height=250)
        frame.pack(pady=5, fill="both", expand=False)
        return frame

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

        headers = ["Kode", "Nama Barang", "Merek", "Satuan", "Stok", "Edit", "Hapus"]
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
                pemohon.nama_lengkap AS nama_pemohon,
                petugas.id_pengguna AS id_petugas,
                petugas.nama_lengkap AS nama_petugas,
                p.tgl_setuju
            FROM permintaan p
            LEFT JOIN pengguna pemohon ON p.id_pemohon = pemohon.id_pengguna
            LEFT JOIN pengguna petugas ON p.id_petugas = petugas.id_pengguna
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
            "ID Petugas",
            "Nama Petugas",
            "Tanggal Setuju",
        ]
        self.build_table(self.request_frame, headers, data)

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
            "Edit",
            "Hapus",
        ]
        self.build_table(
            self.pengeluaran_frame, headers, data, self.build_pengeluaran_row
        )

    def build_pengeluaran_row(self, frame, row_index, item):
        for col, val in enumerate(item[:-2]):
            ctk.CTkLabel(frame, text=val).grid(
                row=row_index, column=col, padx=5, pady=3
            )
        id_pengeluaran = item[0]
        ctk.CTkButton(
            frame,
            text="Edit",
            fg_color="blue",
            command=lambda: self.edit_pengeluaran(id_pengeluaran),
        ).grid(row=row_index, column=7, padx=5)
        ctk.CTkButton(
            frame,
            text="Hapus",
            fg_color="red",
            command=lambda: self.hapus_pengeluaran(id_pengeluaran),
        ).grid(row=row_index, column=8, padx=5)

    def edit_pengeluaran(self, id_pengeluaran):
        EditPengeluaranPage(id_pengeluaran)
        self.after(500, self.load_pengeluaran)

    def hapus_pengeluaran(self, id_pengeluaran):
        confirm = messagebox.askyesno(
            "Konfirmasi", f"Yakin ingin menghapus pengeluaran ID {id_pengeluaran}?"
        )
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM pengeluaran WHERE id_pengeluaran = %s", (id_pengeluaran,)
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Pengeluaran berhasil dihapus.")
            self.load_pengeluaran()

    def build_table(self, frame, headers, data, row_builder=None):
        for col, header in enumerate(headers):
            ctk.CTkLabel(frame, text=header, font=("Arial Bold", 12)).grid(
                row=0, column=col, padx=5, pady=3, sticky="w"
            )
            frame.grid_columnconfigure(col, weight=1)

        for row_index, item in enumerate(data, start=1):
            if row_builder:
                row_builder(frame, row_index, item)
            else:
                for col, val in enumerate(item):
                    ctk.CTkLabel(frame, text=val).grid(
                        row=row_index, column=col, padx=5, pady=3
                    )

    def tambah_barang(self):
        TambahBarangPage()
        self.after(500, self.load_barang)

    def buka_form_penerimaan(self):
        FormPenerimaanPage()
        self.after(500, self.load_data)

    def buka_tabel_penerimaan(self):
        TabelPenerimaanPage(self)
