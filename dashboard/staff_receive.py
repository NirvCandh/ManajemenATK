import customtkinter as ctk
from tkinter import messagebox
from database import connect_db


class FormPenerimaanPage(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()

        self.title("Form Penerimaan Barang")
        self.geometry("400x500")
        self.resizable(False, False)

        ctk.CTkLabel(self, text="Input Penerimaan", font=("Arial Bold", 20)).pack(
            pady=20
        )

        self.id_entry = ctk.CTkEntry(self, placeholder_text="ID Penerimaan")
        self.id_entry.pack(pady=10)

        self.kode_entry = ctk.CTkEntry(self, placeholder_text="Kode Barang")
        self.kode_entry.pack(pady=10)

        self.supplier_entry = ctk.CTkEntry(self, placeholder_text="ID Supplier")
        self.supplier_entry.pack(pady=10)

        self.jumlah_entry = ctk.CTkEntry(self, placeholder_text="Jumlah Masuk")
        self.jumlah_entry.pack(pady=10)

        self.tgl_entry = ctk.CTkEntry(
            self, placeholder_text="Tanggal Masuk (YYYY-MM-DD)"
        )
        self.tgl_entry.pack(pady=10)

        self.harga_entry = ctk.CTkEntry(self, placeholder_text="Harga")
        self.harga_entry.pack(pady=10)

        self.petugas_entry = ctk.CTkEntry(self, placeholder_text="ID Petugas")
        self.petugas_entry.pack(pady=10)

        ctk.CTkButton(self, text="Simpan", command=self.simpan_data).pack(pady=20)

    def simpan_data(self):
        data = (
            self.id_entry.get(),
            self.kode_entry.get(),
            self.supplier_entry.get(),
            self.jumlah_entry.get(),
            self.tgl_entry.get(),
            self.harga_entry.get(),
            self.petugas_entry.get(),
        )

        if not all(data):
            messagebox.showerror("Error", "Semua field wajib diisi.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.callproc(
                "tambah_penerimaan",
                (
                    data[0],
                    data[1],
                    data[2],
                    int(data[3]),
                    data[4],
                    float(data[5]),
                    data[6],
                ),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data penerimaan berhasil disimpan.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Gagal", f"Error: {str(e)}")
