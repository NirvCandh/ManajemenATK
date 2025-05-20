import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class TambahBarangPage(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Tambah Barang")
        self.geometry("400x400")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Form Tambah Barang", font=("Arial Bold", 20)).pack(pady=20)

        self.nama_entry = ctk.CTkEntry(self, placeholder_text="Nama Barang")
        self.nama_entry.pack(pady=10)

        self.jumlah_entry = ctk.CTkEntry(self, placeholder_text="Jumlah")
        self.jumlah_entry.pack(pady=10)

        self.kategori_entry = ctk.CTkEntry(self, placeholder_text="Kategori")
        self.kategori_entry.pack(pady=10)

        self.satuan_entry = ctk.CTkEntry(self, placeholder_text="Satuan")
        self.satuan_entry.pack(pady=10)

        ctk.CTkButton(self, text="Simpan", command=self.simpan_barang).pack(pady=20)

    def simpan_barang(self):
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
            query = "INSERT INTO barang (nama_brg, jumlah, kategori, satuan) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nama, jumlah, kategori, satuan))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Barang berhasil ditambahkan.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")
