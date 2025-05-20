import customtkinter as ctk
from tkinter import messagebox, simpledialog
from database import connect_db
from datetime import date


class PemohonDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Dashboard Pemohon - Manajemen ATK")
        self.geometry("700x500")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Barang Tersedia", font=("Arial Black", 22)).pack(
            pady=20
        )

        self.table_frame = ctk.CTkScrollableFrame(self, height=300)
        self.table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_barang_table()

        self.current_pemohon_id = "P001"

    def load_barang_table(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT kode_barang, nama_barang, stok FROM barang")
            rows = cursor.fetchall()
            conn.close()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data barang: {str(e)}")
            rows = []

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Header tabel
        ctk.CTkLabel(self.table_frame, text="Kode", font=("Arial Bold", 14)).grid(
            row=0, column=0, padx=10, pady=8, sticky="w"
        )
        ctk.CTkLabel(
            self.table_frame, text="Nama Barang", font=("Arial Bold", 14)
        ).grid(row=0, column=1, padx=10, pady=8, sticky="w")
        ctk.CTkLabel(self.table_frame, text="Stok", font=("Arial Bold", 14)).grid(
            row=0, column=2, padx=10, pady=8, sticky="e"
        )
        ctk.CTkLabel(self.table_frame, text="Aksi", font=("Arial Bold", 14)).grid(
            row=0, column=3, padx=10, pady=8
        )

        for i, (kode, nama, stok) in enumerate(rows, start=1):
            ctk.CTkLabel(self.table_frame, text=kode).grid(
                row=i, column=0, padx=10, pady=5, sticky="w"
            )
            ctk.CTkLabel(self.table_frame, text=nama).grid(
                row=i, column=1, padx=10, pady=5, sticky="w"
            )
            ctk.CTkLabel(self.table_frame, text=str(stok)).grid(
                row=i, column=2, padx=10, pady=5, sticky="e"
            )

            btn_pinjam = ctk.CTkButton(
                self.table_frame,
                text="Pinjam",
                width=80,
                command=lambda k=kode, n=nama, s=stok: self.pinjam_barang(k, n, s),
            )
            btn_pinjam.grid(row=i, column=3, padx=10, pady=5)

        self.table_frame.grid_columnconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(1, weight=3)
        self.table_frame.grid_columnconfigure(2, weight=1)
        self.table_frame.grid_columnconfigure(3, weight=1)

    def pinjam_barang(self, kode_barang, nama_barang, stok):
        if stok == 0:
            messagebox.showwarning(
                "Stok Kosong", f"Barang '{nama_barang}' sedang habis stok."
            )
            return

        jumlah = simpledialog.askinteger(
            "Pinjam Barang",
            f"Masukkan jumlah '{nama_barang}' yang ingin dipinjam (max {stok}):",
            minvalue=1,
            maxvalue=stok,
            parent=self,
        )
        if jumlah is None:
            return  # batal input

        import random, string

        new_id = "PR" + "".join(random.choices(string.digits, k=5))

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.callproc(
                "tambah_permintaan",
                (
                    new_id,
                    self.current_pemohon_id,
                    date.today().isoformat(),
                    "Menunggu",
                    None,
                    None,
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo(
                "Sukses",
                f"Permintaan pinjam {jumlah} '{nama_barang}' berhasil dibuat dengan ID {new_id}",
            )
            self.load_barang_table()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan permintaan: {str(e)}")
