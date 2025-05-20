import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class TambahBarangPage(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Tambah Barang")
        self.geometry("400x500")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Form Tambah Barang", font=("Arial Bold", 20)).pack(pady=20)

        self.kode_entry = ctk.CTkEntry(self, placeholder_text="Kode Barang")
        self.kode_entry.pack(pady=10)

        self.nama_entry = ctk.CTkEntry(self, placeholder_text="Nama Barang")
        self.nama_entry.pack(pady=10)

        self.stok_entry = ctk.CTkEntry(self, placeholder_text="Merek")
        self.stok_entry.pack(pady=10)

        self.satuan_entry = ctk.CTkEntry(self, placeholder_text="Satuan")
        self.satuan_entry.pack(pady=10)

        self.merk_entry = ctk.CTkEntry(self, placeholder_text="Stok")
        self.merk_entry.pack(pady=10)

        ctk.CTkButton(self, text="Simpan", command=self.simpan_barang).pack(pady=20)

    def simpan_barang(self):
        kode = self.kode_entry.get()
        nama = self.nama_entry.get()
        merek = self.stok_entry.get()
        satuan = self.satuan_entry.get()
        stok = self.merk_entry.get()

        if not all([kode, nama, merek, satuan, satuan]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        try:
            stok_int = int(stok)
        except ValueError:
            messagebox.showerror("Error", "Stok harus berupa angka!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "CALL tambah_barang(%s, %s, %s, %s, %s)"
            cursor.execute(query, (kode, nama, merek, satuan, stok_int))
            conn.commit()
            conn.close()

            messagebox.showinfo("Sukses", "Barang berhasil ditambahkan.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data: {str(e)}")
