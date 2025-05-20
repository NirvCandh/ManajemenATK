import customtkinter as ctk
import bcrypt
from tkinter import messagebox
from database import connect_db


class RegisterApp(ctk.CTkFrame):
    def __init__(self, master, show_login_callback):
        super().__init__(master)
        self.show_login_callback = show_login_callback

        ctk.CTkLabel(self, text="Daftar Akun", font=("Arial Bold", 24)).pack(pady=20)

        self.nama_entry = ctk.CTkEntry(self, placeholder_text="Nama Lengkap")
        self.nama_entry.pack(pady=8)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=8)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=8)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=8)

        self.role_optionmenu = ctk.CTkOptionMenu(
            self, values=["Admin", "Petugas", "Pemohon"]
        )
        self.role_optionmenu.pack(pady=8)
        self.role_optionmenu.set("Pemohon")

        label_frame = ctk.CTkFrame(self, fg_color="transparent")
        label_frame.pack(pady=5)

        ctk.CTkLabel(
            label_frame, text="Sudah punya akun?", font=("Arial Bold", 10)
        ).pack(side="left")

        self.login_label = ctk.CTkLabel(
            label_frame,
            text="Login di sini",
            text_color="#1f6aa5",
            font=("Arial Bold", 10),
            cursor="hand2",
        )
        self.login_label.pack(side="left", padx=4)

        self.login_label.bind(
            "<Enter>",
            lambda e: self.login_label.configure(underline=True, text_color="#144e85"),
        )
        self.login_label.bind(
            "<Leave>",
            lambda e: self.login_label.configure(underline=False, text_color="#1f6aa5"),
        )
        self.login_label.bind("<Button-1>", lambda e: self.open_login())

        ctk.CTkButton(self, text="Register", command=self.register).pack(pady=20)

    def register(self):
        nama_lengkap = self.nama_entry.get().strip()
        username = self.username_entry.get().strip()
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_optionmenu.get()

        if not all([nama_lengkap, username, email, password]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        # Validasi email sederhana (bisa dikembangkan lagi)
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Format email tidak valid!")
            return

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        try:
            conn = connect_db()
            cursor = conn.cursor()

            query = """
                INSERT INTO pengguna (nama_lengkap, username, email, password, role)
                VALUES (%s, %s, %s, %s, %s)
            """

            cursor.execute(
                query,
                (nama_lengkap, username, email, hashed_password.decode("utf-8"), role),
            )
            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Sukses", "Registrasi berhasil. Silakan login.")
            self.open_login()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal registrasi: {str(e)}")
            try:
                conn.close()
            except:
                pass

    def open_login(self):
        self.destroy()
        self.show_login_callback()
