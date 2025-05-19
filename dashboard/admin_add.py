import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class AddUserForm(ctk.CTkToplevel):
    def __init__(self, parent, role, refresh_callback=None):
        super().__init__(parent)
        self.role = role
        self.refresh_callback = refresh_callback  # buat refresh list user di parent kalau perlu

        self.title(f"Tambah {role.capitalize()}")
        self.geometry("350x300")
        self.resizable(False, False)

        ctk.CTkLabel(self, text=f"Tambah {role.capitalize()}", font=("Arial Black", 18)).pack(pady=20)

        self.nama_entry = ctk.CTkEntry(self, placeholder_text="Nama")
        self.nama_entry.pack(pady=10, padx=20, fill="x")

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=10, padx=20, fill="x")

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10, padx=20, fill="x")

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10, padx=20, fill="x")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=20, padx=20, fill="x")

        ctk.CTkButton(btn_frame, text="Simpan", command=self.save_user).pack(side="left", expand=True, fill="x", padx=(0,10))
        ctk.CTkButton(btn_frame, text="Batal", fg_color="#BC4749", hover_color="#992D2D", command=self.destroy).pack(side="left", expand=True, fill="x")

    def save_user(self):
        nama = self.nama_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not (nama and username and email and password):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO user (nama, username, email, password, role) VALUES (%s, %s, %s, %s, %s)",
                (nama, username, email, password, self.role)
            )
            conn.commit()
            messagebox.showinfo("Sukses", f"{self.role.capitalize()} berhasil ditambahkan!")
            if self.refresh_callback:
                self.refresh_callback()
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan user: {e}")
        finally:
            conn.close()
