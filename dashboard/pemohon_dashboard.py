import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class PemohonDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Pemohon - Manajemen ATK")
        self.geometry("700x500")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Barang Tersedia", font=("Arial Black", 22)).pack(pady=20)

        self.table_frame = ctk.CTkScrollableFrame(self, height=300)
        self.table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        self.load_barang_table()

        ctk.CTkButton(self, text="Pinjam Barang", command=self.open_peminjaman_form).pack(pady=15)

    def load_barang_table(self):
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT nama_barang, stok FROM barang")
        rows = cursor.fetchall()
        conn.close()

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.table_frame, text="Nama Barang", font=("Arial Bold", 14)).grid(row=0, column=0, padx=15, pady=8, sticky="w")
        ctk.CTkLabel(self.table_frame, text="Stok", font=("Arial Bold", 14)).grid(row=0, column=1, padx=15, pady=8, sticky="e")

        for i, (nama, stok) in enumerate(rows, start=1):
            ctk.CTkLabel(self.table_frame, text=nama).grid(row=i, column=0, padx=15, pady=5, sticky="w")
            ctk.CTkLabel(self.table_frame, text=str(stok)).grid(row=i, column=1, padx=15, pady=5, sticky="e")

        self.table_frame.grid_columnconfigure(0, weight=3)
        self.table_frame.grid_columnconfigure(1, weight=1)

    def open_peminjaman_form(self):
        self.destroy()
        print("Arahkan ke halaman peminjaman form...") 
        
if __name__ == "__main__":
    app = PemohonDashboard()
    app.mainloop()
