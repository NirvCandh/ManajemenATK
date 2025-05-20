import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from dashboard.staff_add import TambahBarangPage
from dashboard.staff_edit import EditBarangPage

class StaffDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Staff - Manajemen ATK")
        self.geometry("950x600")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Dashboard Staff", font=("Arial Bold", 22)).pack(pady=10)

        # Tabel Barang
        self.table_frame = ctk.CTkScrollableFrame(self, height=250)
        self.table_frame.pack(pady=10, padx=10, fill="both", expand=False)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)
        ctk.CTkButton(button_frame, text="Tambah Barang", command=self.tambah_barang).pack(side="left", padx=10)

        # Label Request Pinjam
        ctk.CTkLabel(self, text="Daftar Request Pinjam", font=("Arial Bold", 18)).pack(pady=(20, 5))
        self.request_frame = ctk.CTkScrollableFrame(self, height=250)
        self.request_frame.pack(pady=5, padx=10, fill="both", expand=False)

        self.load_data()

    def load_data(self):
        self.load_barang()
        self.load_permintaan()

    def load_barang(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT kode_barang, nama_barang, stok, merek, satuan
            FROM barang
        """)
        data = cursor.fetchall()
        conn.close()

        headers = ["Kode", "Nama Barang", "Stok", "Merek", "Satuan", "Aksi Edit", "Aksi Hapus"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self.table_frame, text=header, font=("Arial Bold", 12)).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        for row, item in enumerate(data, start=1):
            kode_barang, nama, stok, merek, satuan = item

            ctk.CTkLabel(self.table_frame, text=kode_barang).grid(row=row, column=0, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=nama).grid(row=row, column=1, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=stok).grid(row=row, column=2, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=merek or "-").grid(row=row, column=3, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=satuan or "-").grid(row=row, column=4, padx=10, pady=5)

            edit_btn = ctk.CTkButton(
                self.table_frame, text="Edit", fg_color="blue",
                command=lambda k=kode_barang: self.edit_barang(k)
            )
            edit_btn.grid(row=row, column=5, padx=5, pady=5)

            hapus_btn = ctk.CTkButton(
                self.table_frame, text="Hapus", fg_color="red",
                command=lambda k=kode_barang: self.hapus_barang(k)
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
            ctk.CTkLabel(self.request_frame, text=header, font=("Arial Bold", 12)).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        for row, item in enumerate(requests, start=1):
            id_perm, nama_barang, jumlah, status, id_pemohon = item

            ctk.CTkLabel(self.request_frame, text=id_perm).grid(row=row, column=0, padx=10, pady=5)
            ctk.CTkLabel(self.request_frame, text=nama_barang).grid(row=row, column=1, padx=10, pady=5)
            ctk.CTkLabel(self.request_frame, text=jumlah).grid(row=row, column=2, padx=10, pady=5)
            ctk.CTkLabel(self.request_frame, text=status).grid(row=row, column=3, padx=10, pady=5)
            ctk.CTkLabel(self.request_frame, text=id_pemohon).grid(row=row, column=4, padx=10, pady=5)

        for col in range(len(headers)):
            self.request_frame.grid_columnconfigure(col, weight=1)

    def tambah_barang(self):
        TambahBarangPage()

    def edit_barang(self, kode_barang):
        EditBarangPage(kode_barang)

    def hapus_barang(self, kode_barang):
        confirm = messagebox.askyesno("Konfirmasi", f"Yakin ingin menghapus barang {kode_barang}?")
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM barang WHERE kode_barang = %s", (kode_barang,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Barang berhasil dihapus.")
            self.load_data()


if __name__ == "__main__":
    app = StaffDashboard()
    app.mainloop()
