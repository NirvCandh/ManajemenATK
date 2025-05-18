import customtkinter as ctk
from tkinter import messagebox

class UserDashboard(ctk.CTkFrame):
    def __init__(self, parent, data, role):
        super().__init__(parent)
        self.data = data
        self.role = role
        self.build_ui()

    def build_ui(self):
        ctk.CTkLabel(self, text=self.role.capitalize(), font=("Arial Black", 18)).pack(anchor="w", pady=5)

        # Header
        header_frame = ctk.CTkFrame(self, fg_color="#E0E0E0")
        header_frame.pack(fill="x")

        for col, width in zip(["ID", "Nama", "Username", "Email", "Aksi"], [50, 150, 150, 200, 130]):
            ctk.CTkLabel(header_frame, text=col, width=width, anchor="center", font=("Arial", 12, "bold")).pack(side="left")

        # Rows
        for user in self.data:
            self.create_row(user)

        # Tombol tambah
        ctk.CTkButton(self, text=f"Tambah {self.role.capitalize()}", width=150, command=self.add_user).pack(pady=10)

    def create_row(self, user):
        row_frame = ctk.CTkFrame(self)
        row_frame.pack(fill="x", pady=2)

        ctk.CTkLabel(row_frame, text=str(user["id"]), width=50, anchor="center").pack(side="left")
        ctk.CTkLabel(row_frame, text=user["nama"], width=150, anchor="w", padx=5).pack(side="left")
        ctk.CTkLabel(row_frame, text=user["username"], width=150, anchor="w", padx=5).pack(side="left")
        ctk.CTkLabel(row_frame, text=user["email"], width=200, anchor="w", padx=5).pack(side="left")

        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent", width=130)
        action_frame.pack(side="left")

        ctk.CTkButton(action_frame, text="Edit", width=40, command=lambda u=user: self.edit_user(u)).pack(side="left", padx=5)
        ctk.CTkButton(action_frame, text="Hapus", width=50, fg_color="#BC4749", hover_color="#992D2D", command=lambda u=user: self.delete_user(u)).pack(side="left")

    # Method-method ini bisa di-override oleh subclass kalau perlu custom behavior
    def add_user(self):
        messagebox.showinfo("Tambah", f"Tambah user baru untuk role {self.role}")

    def edit_user(self, user):
        messagebox.showinfo("Edit", f"Edit {self.role} {user['nama']}")

    def delete_user(self, user):
        confirm = messagebox.askyesno("Hapus", f"Yakin mau hapus {self.role} {user['nama']}?")
        if confirm:
            messagebox.showinfo("Hapus", f"{self.role.capitalize()} {user['nama']} dihapus")

# Subclass khusus Staff
class StaffDashboard(UserDashboard):
    def __init__(self, parent, data):
        super().__init__(parent, data, role="staff")

    # Override kalau ada custom logika
    def add_user(self):
        messagebox.showinfo("Tambah Staff", "Form tambah staff dibuka")

# Subclass khusus Pemohon
class PemohonDashboard(UserDashboard):
    def __init__(self, parent, data):
        super().__init__(parent, data, role="pemohon")

    # Override kalau ada custom logika
    def add_user(self):
        messagebox.showinfo("Tambah Pemohon", "Form tambah pemohon dibuka")

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Admin - Manajemen ATK")
        self.geometry("700x600")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Admin Dashboard", font=("Arial Black", 24)).pack(pady=15)

        # Contoh data dummy, nanti diganti ambil dari database
        staff_data = [
            {"id": 1, "nama": "Budi", "username": "budi123", "email": "budi@mail.com"},
            {"id": 2, "nama": "Sari", "username": "sari99", "email": "sari@mail.com"},
        ]

        pemohon_data = [
            {"id": 1, "nama": "Andi", "username": "andi77", "email": "andi@mail.com"},
            {"id": 2, "nama": "Rina", "username": "rina88", "email": "rina@mail.com"},
        ]

        # Frame buat staff dashboard
        staff_frame = StaffDashboard(self, staff_data)
        staff_frame.pack(fill="x", padx=20, pady=(10,5))

        # Frame buat pemohon dashboard
        pemohon_frame = PemohonDashboard(self, pemohon_data)
        pemohon_frame.pack(fill="x", padx=20, pady=(20,5))

        ctk.CTkLabel(self, text="© 2025 Instansi Lo", font=("Arial", 10)).pack(side="bottom", pady=10)

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
