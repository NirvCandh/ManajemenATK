import customtkinter as ctk
from tkinter import messagebox, simpledialog
from database import connect_db
from datetime import date
import random
import string


class PemohonDashboard(ctk.CTk):
    def __init__(self, current_pengguna_id):
        super().__init__()
        self.current_pengguna_id = current_pengguna_id
        self.title("Dashboard Pemohon - Manajemen ATK")
        self.geometry("700x500")
        self.resizable(False, False)
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(
            self, text="Daftar Barang Tersedia", font=("Arial Black", 20)
        ).pack(pady=10)

        self.table_frame = ctk.CTkScrollableFrame(self, width=680, height=400)
        self.table_frame.pack(padx=10, pady=10)

        self.load_barang_table()

    def load_barang_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        headers = ["Kode Barang", "Nama Barang", "Stok", "Aksi"]
        for col, header in enumerate(headers):
            label = ctk.CTkLabel(
                self.table_frame, text=header, font=("Arial", 14, "bold")
            )
            label.grid(row=0, column=col, padx=10, pady=5)

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT kode_barang, nama_barang, stok FROM barang WHERE stok > 0"
            )
            rows = cursor.fetchall()
            conn.close()

            for row_idx, (kode, nama, stok) in enumerate(rows, start=1):
                ctk.CTkLabel(self.table_frame, text=kode).grid(
                    row=row_idx, column=0, padx=10, pady=5
                )
                ctk.CTkLabel(self.table_frame, text=nama).grid(
                    row=row_idx, column=1, padx=10, pady=5
                )
                ctk.CTkLabel(self.table_frame, text=str(stok)).grid(
                    row=row_idx, column=2, padx=10, pady=5
                )

                btn_pinjam = ctk.CTkButton(
                    self.table_frame,
                    text="Pinjam",
                    width=80,
                    command=lambda k=kode, s=stok: self.pinjam_barang(k, s),
                )
                btn_pinjam.grid(row=row_idx, column=3, padx=10, pady=5)

        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data barang: {str(e)}")

    def pinjam_barang(self, kode_barang, stok):
        jumlah_str = simpledialog.askstring(
            "Pinjam Barang",
            f"Masukkan jumlah pinjam untuk {kode_barang} (max {stok}):",
            parent=self,
        )
        if jumlah_str is None:
            return

        if not jumlah_str.isdigit():
            messagebox.showerror("Error", "Jumlah harus angka!")
            return

        jumlah = int(jumlah_str)
        if jumlah < 1 or jumlah > stok:
            messagebox.showerror("Error", f"Jumlah harus antara 1 sampai {stok}.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            new_id = "PR" + "".join(random.choices(string.digits, k=5))

            cursor.execute(
                "INSERT INTO permintaan (id_permintaan , id_pemohon, tgl_permintaan, status) VALUES (%s, %s, %s, %s)",
                (new_id, self.current_pengguna_id, date.today(), "Menunggu"),
            )
            cursor.execute(
                "INSERT INTO detail_permintaan (id_permintaan, kode_barang, jumlah) VALUES (%s, %s, %s)",
                (new_id, kode_barang, jumlah),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", f"Permintaan {new_id} berhasil dibuat.")
            self.destroy()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan permintaan: {str(e)}")
