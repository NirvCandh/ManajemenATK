import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class UserDashboard(ctk.CTkScrollableFrame):
    def __init__(self, parent, data, role):
        super().__init__(parent)
        self.data = data
        self.role = role
        self.build_ui()

    def build_ui(self):
        # Judul role
        label = ctk.CTkLabel(self, text=self.role.capitalize(), font=("Arial Black", 18))
        label.grid(row=0, column=0, sticky="w", pady=(10, 15), padx=10)

        # Header tabel
        headers = ["ID", "Nama", "Username", "Email", "Aksi"]
        for col, text in enumerate(headers):
            hdr = ctk.CTkLabel(self, text=text, font=("Arial", 12, "bold"))
            hdr.grid(row=1, column=col, padx=10, pady=5, sticky="ew")

        # Rows data user
        for i, user in enumerate(self.data, start=2):
            self.create_row(i, user)

        # Tombol tambah di bawah tabel
        self.add_btn = ctk.CTkButton(self, text=f"Tambah {self.role.capitalize()}", command=self.add_user)
        self.add_btn.grid(row=len(self.data) + 2, column=0, columnspan=5, pady=20, padx=10, sticky="w")

        # Buat kolom stretchable supaya tabel rapi
        for c in range(5):
            self.grid_columnconfigure(c, weight=1)

    def create_row(self, row, user):
        ctk.CTkLabel(self, text=str(user["id"])).grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self, text=user["nama"]).grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self, text=user["username"]).grid(row=row, column=2, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self, text=user["email"]).grid(row=row, column=3, padx=10, pady=5, sticky="ew")

        # Frame aksi untuk tombol Edit & Hapus
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=row, column=4, padx=10, pady=5, sticky="ew")

        ctk.CTkButton(action_frame, text="Edit", width=50, command=lambda u=user: self.edit_user(u)).pack(side="left", padx=(0,5))
        ctk.CTkButton(action_frame, text="Hapus", width=60, fg_color="#BC4749", hover_color="#992D2D", command=lambda u=user: self.delete_user(u)).pack(side="left")

    # Placeholder methods bisa di override
    def add_user(self):
        messagebox.showinfo("Tambah", f"Tambah user baru untuk role {self.role}")

    def edit_user(self, user):
        messagebox.showinfo("Edit", f"Edit {self.role} {user['nama']}")

    def delete_user(self, user):
        confirm = messagebox.askyesno("Hapus", f"Yakin mau hapus {self.role} {user['nama']}?")
        if confirm:
            messagebox.showinfo("Hapus", f"{self.role.capitalize()} {user['nama']} dihapus")

# Subclass Staff
class StaffDashboard(UserDashboard):
    def __init__(self, parent, data):
        super().__init__(parent, data, role="staff")

    def add_user(self):
        messagebox.showinfo("Tambah Staff", "Form tambah staff dibuka")

# Subclass Pemohon
class PemohonDashboard(UserDashboard):
    def __init__(self, parent, data):
        super().__init__(parent, data, role="pemohon")

    def add_user(self):
        messagebox.showinfo("Tambah Pemohon", "Form tambah pemohon dibuka")

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Admin - Manajemen ATK")
        self.geometry("800x600")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Admin Dashboard", font=("Arial Black", 26)).pack(pady=15)

        # Data contoh (dummy) - nanti ganti dari DB
        staff_data = [
            {"id": 1, "nama": "Budi", "username": "budi123", "email": "budi@mail.com"},
            {"id": 2, "nama": "Sari", "username": "sari99", "email": "sari@mail.com"},
            {"id": 3, "nama": "Doni", "username": "doni88", "email": "doni@mail.com"},
        ]

        pemohon_data = [
            {"id": 1, "nama": "Andi", "username": "andi77", "email": "andi@mail.com"},
            {"id": 2, "nama": "Rina", "username": "rina88", "email": "rina@mail.com"},
            {"id": 3, "nama": "Tika", "username": "tika22", "email": "tika@mail.com"},
        ]

        # Frame kontainer dengan scrollbar untuk staff
        staff_frame = StaffDashboard(self, staff_data)
        staff_frame.pack(fill="both", expand=True, padx=20, pady=(10,5))

        # Frame kontainer dengan scrollbar untuk pemohon
        pemohon_frame = PemohonDashboard(self, pemohon_data)
        pemohon_frame.pack(fill="both", expand=True, padx=20, pady=(20,10))

        ctk.CTkLabel(self, text="© 2025 Your Company", font=("Arial", 10)).pack(side="bottom", pady=10)


if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
