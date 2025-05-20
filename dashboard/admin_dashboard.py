import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from dashboard.admin_add import AddUserForm 
from dashboard.admin_edit import EditUserForm

class UserDashboard(ctk.CTkScrollableFrame):
    def __init__(self, parent, role):
        super().__init__(parent)
        self.role = role
        self.data = []
        self.refresh_data()

    def build_ui(self):
        label = ctk.CTkLabel(self, text=self.role.capitalize(), font=("Arial Black", 18))
        label.grid(row=0, column=0, sticky="w", pady=(10, 15), padx=10)

        headers = ["ID Pengguna", "Nama Lengkap", "Username", "Email", "Aksi"]
        for col, text in enumerate(headers):
            hdr = ctk.CTkLabel(self, text=text, font=("Arial", 12, "bold"))
            hdr.grid(row=1, column=col, padx=10, pady=5, sticky="ew")

        for i, user in enumerate(self.data, start=2):
            self.create_row(i, user)

        if self.role != "pemohon":
            self.add_btn = ctk.CTkButton(self, text=f"Tambah {self.role.capitalize()}", command=self.add_user)
            self.add_btn.grid(row=len(self.data) + 2, column=0, columnspan=5, pady=20, padx=10, sticky="w")

        for c in range(5):
            self.grid_columnconfigure(c, weight=1)

    def create_row(self, row, user):
        ctk.CTkLabel(self, text=str(user["id_pengguna"])).grid(row=row, column=0, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self, text=user["nama_lengkap"]).grid(row=row, column=1, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self, text=user["username"]).grid(row=row, column=2, padx=10, pady=5, sticky="ew")
        ctk.CTkLabel(self, text=user["email"]).grid(row=row, column=3, padx=10, pady=5, sticky="ew")

        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=row, column=4, padx=10, pady=5, sticky="ew")

        if self.role != "pemohon":
            ctk.CTkButton(action_frame, text="Edit", width=50, command=lambda u=user: self.edit_user(u)).pack(side="left", padx=(0,5))

        ctk.CTkButton(
            action_frame,
            text="Hapus",
            width=60,
            fg_color="#BC4749",
            hover_color="#992D2D",
            command=lambda u=user: self.delete_user(u)
        ).pack(side="left")

    def add_user(self):
        form = AddUserForm(self.master, self.role, refresh_callback=self.refresh_data)
        form.grab_set()

    def edit_user(self, user):
        form = EditUserForm(self.master, user, self.role, refresh_callback=self.refresh_data)
        form.grab_set()

    def delete_user(self, user):
        confirm = messagebox.askyesno("Hapus", f"Yakin mau hapus {self.role} {user['nama_lengkap']}?")
        if confirm:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pengguna WHERE id_pengguna = %s", (user["id_pengguna"],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Hapus", f"{self.role.capitalize()} {user['nama_lengkap']} dihapus")
            self.refresh_data()

    def refresh_data(self):
        conn = connect_db()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id_pengguna, nama_lengkap, username, email FROM pengguna WHERE role=%s", (self.role,))
        self.data = cursor.fetchall()
        conn.close()

        for widget in self.winfo_children():
            widget.destroy()

        self.build_ui()

class StaffDashboard(UserDashboard):
    def __init__(self, parent):
        super().__init__(parent, role="petugas")

class PemohonDashboard(UserDashboard):
    def __init__(self, parent):
        super().__init__(parent, role="pemohon")

class AdminDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Dashboard Admin - Manajemen ATK")
        self.geometry("800x600")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Admin Dashboard", font=("Arial Black", 26)).pack(pady=15)

        # Tampilkan dashboard staff & pemohon tanpa passing data manual
        staff_frame = StaffDashboard(self)
        staff_frame.pack(fill="both", expand=True, padx=20, pady=(10,5))

        pemohon_frame = PemohonDashboard(self)
        pemohon_frame.pack(fill="both", expand=True, padx=20, pady=(20,10))

if __name__ == "__main__":
    app = AdminDashboard()
    app.mainloop()
