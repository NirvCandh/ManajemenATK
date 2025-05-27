import customtkinter as ctk
from tkinter import messagebox
from database import connect_db


class EditBarangPage(ctk.CTkToplevel):
    def __init__(self, kode_barang, nama_awal, stok_awal, merek_awal, satuan_awal):
        super().__init__()

        self.kode_barang = kode_barang

        self.title("Edit Barang")
        self.geometry("400x400")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Form Edit Barang", font=("Arial Bold", 20)).pack(
            pady=20
        )

        self.nama_entry = ctk.CTkEntry(self, placeholder_text="Nama Barang")
        self.nama_entry.insert(0, nama_awal)
        self.nama_entry.pack(pady=10)

        self.stok_entry = ctk.CTkEntry(self, placeholder_text="Stok")
        self.stok_entry.insert(0, str(stok_awal))
        self.stok_entry.pack(pady=10)

        self.merek_entry = ctk.CTkEntry(self, placeholder_text="Merek")
        self.merek_entry.insert(0, merek_awal if merek_awal else "")
        self.merek_entry.pack(pady=10)

        self.satuan_entry = ctk.CTkEntry(self, placeholder_text="Satuan")
        self.satuan_entry.insert(0, satuan_awal if satuan_awal else "")
        self.satuan_entry.pack(pady=10)

        ctk.CTkButton(self, text="Simpan Perubahan", command=self.update_barang).pack(
            pady=20
        )

    def update_barang(self):
        nama = self.nama_entry.get().strip()
        stok = self.stok_entry.get().strip()
        merek = self.merek_entry.get().strip()
        satuan = self.satuan_entry.get().strip()

        if not all([nama, stok, merek, satuan]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        try:
            stok_int = int(stok)
            if stok_int < 0:
                raise ValueError("Stok harus angka positif")
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka positif")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.callproc(
                "update_barang", (self.kode_barang, nama, merek, satuan, stok_int)
            )
            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data barang berhasil diperbarui.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update data: {str(e)}")
