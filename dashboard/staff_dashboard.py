import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from dashboard.staff_add import TambahBarangPage
from dashboard.staff_edit import EditBarangPage

class StaffDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Staff - Manajemen ATK")
        self.geometry("800x500")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Dashboard Staff", font=("Arial Bold", 22)).pack(pady=10)

        self.table_frame = ctk.CTkScrollableFrame(self, height=300)
        self.table_frame.pack(pady=10, padx=10, fill="both", expand=True)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Tambah Barang", command=self.tambah_barang).pack(side="left", padx=10)

        self.load_data()

    def load_data(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM barang")
        count = cursor.fetchone()[0]
        if count == 0:
            dummy_data = [
                ("BRG001", "Pulpen", 50),
                ("BRG002", "Pensil", 70),
                ("BRG003", "Penghapus", 40)
            ]
            cursor.executemany("INSERT INTO barang (kode_barang, nama_barang, stok) VALUES (%s, %s, %s)", dummy_data)
            conn.commit()

        cursor.execute("SELECT kode_barang, nama_barang, stok FROM barang")
        data = cursor.fetchall()
        conn.close()

        headers = ["Kode", "Nama Barang", "Stok", "Aksi"]
        for col, header in enumerate(headers):
            ctk.CTkLabel(self.table_frame, text=header, font=("Arial Bold", 12)).grid(row=0, column=col, padx=10, pady=5, sticky="w")

        for row, item in enumerate(data, start=1):
            kode_barang, nama, stok, kategori, satuan = item

            ctk.CTkLabel(self.table_frame, text=kode_barang).grid(row=row, column=0, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=nama).grid(row=row, column=1, padx=10, pady=5)
            ctk.CTkLabel(self.table_frame, text=stok).grid(row=row, column=2, padx=10, pady=5)

            edit_btn = ctk.CTkButton(
            self.table_frame, text="Edit", fg_color="blue",
            command=lambda k=kode_barang, n=nama, s=stok, kat=kategori, sat=satuan: EditBarangPage(k, n, s, kat, sat)
    )
        edit_btn.grid(row=row, column=3, padx=5, pady=5)

        for col in range(len(headers)):
            self.table_frame.grid_columnconfigure(col, weight=1)

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
