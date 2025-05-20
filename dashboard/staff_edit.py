import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class EditBarangPage(ctk.CTkToplevel):
    def __init__(self, barang_id, nama_awal, jumlah_awal, kategori_awal, satuan_awal):
        super().__init__()

        self.barang_id = barang_id

        self.title("Edit Barang")
        self.geometry("400x400")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Form Edit Barang", font=("Arial Bold", 20)).pack(pady=20)

        self.nama_entry = ctk.CTkEntry(self, placeholder_text="Nama Barang")
        self.nama_entry.insert(0, nama_awal)
        self.nama_entry.pack(pady=10)

        self.jumlah_entry = ctk.CTkEntry(self, placeholder_text="Jumlah")
        self.jumlah_entry.insert(0, str(jumlah_awal))
        self.jumlah_entry.pack(pady=10)

        self.kategori_entry = ctk.CTkEntry(self, placeholder_text="Kategori")
        self.kategori_entry.insert(0, kategori_awal)
        self.kategori_entry.pack(pady=10)

        self.satuan_entry = ctk.CTkEntry(self, placeholder_text="Satuan")
        self.satuan_entry.insert(0, satuan_awal)
        self.satuan_entry.pack(pady=10)

        ctk.CTkButton(self, text="Simpan Perubahan", command=self.update_barang).pack(pady=20)

    def update_barang(self):
        nama = self.nama_entry.get()
        jumlah = self.jumlah_entry.get()
        kategori = self.kategori_entry.get()
        satuan = self.satuan_entry.get()

        if not all([nama, jumlah, kategori, satuan]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "UPDATE barang SET nama_brg=%s, jumlah=%s, kategori=%s, satuan=%s WHERE id_brg=%s"
            cursor.execute(query, (nama, jumlah, kategori, satuan, self.barang_id))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Data barang berhasil diperbarui.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update data: {str(e)}")
            