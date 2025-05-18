import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class StaffDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Staff - Manajemen ATK")
        self.geometry("800x500")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Dashboard Staff", font=("Arial Bold", 22)).pack(pady=10)

        # Frame scrollable untuk tabel barang
        self.table_frame = ctk.CTkScrollableFrame(self, height=300)
        self.table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Tombol CRUD
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Tambah Barang", command=self.tambah_barang).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Edit Barang", command=self.edit_barang).pack(side="left", padx=10)
        ctk.CTkButton(button_frame, text="Hapus Barang", command=self.hapus_barang).pack(side="left", padx=10)

        self.load_data()

    def load_data(self):
        # Bersihkan dulu isi frame sebelum reload data
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT kode_barang, nama_barang, stok FROM barang")
        data = cursor.fetchall()
        conn.close()

        # Header tabel
        headers = ["ID", "Nama Barang", "Stok"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self.table_frame, text=header, font=("Arial Bold", 12)).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        # Isi data tabel
        for row, item in enumerate(data, start=1):
            for col, val in enumerate(item):
                ctk.CTkLabel(self.table_frame, text=str(val)).grid(row=row, column=col, padx=10, pady=2, sticky="w")

        # Buat kolom stretch agar tampilan rapi
        for col in range(len(headers)):
            self.table_frame.grid_columnconfigure(col, weight=1)

    def tambah_barang(self):
        messagebox.showinfo("Tambah", "Fitur tambah barang akan segera hadir!")

    def edit_barang(self):
        messagebox.showinfo("Edit", "Fitur edit barang akan segera hadir!")

    def hapus_barang(self):
        messagebox.showinfo("Hapus", "Fitur hapus barang akan segera hadir!")

if __name__ == "__main__":
    app = StaffDashboard()
    app.mainloop()
