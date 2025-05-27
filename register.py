import customtkinter as ctk
import mysql.connector
from tkinter import messagebox
import bcrypt


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, show_login_callback):
        super().__init__(parent)
        self.parent = parent
        self.show_login_callback = show_login_callback

        self.label_title = ctk.CTkLabel(
            self, text="REGISTER", font=("Arial", 20, "bold")
        )
        self.label_title.pack(pady=10)

        self.entry_nama = ctk.CTkEntry(self, placeholder_text="Nama Lengkap")
        self.entry_nama.pack(pady=5)

        self.entry_username = ctk.CTkEntry(self, placeholder_text="Username")
        self.entry_username.pack(pady=5)

        self.entry_email = ctk.CTkEntry(self, placeholder_text="Email")
        self.entry_email.pack(pady=5)

        self.entry_password = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.entry_password.pack(pady=5)

        self.entry_unit = ctk.CTkEntry(
            self, placeholder_text="Unit (boleh kosong untuk Admin)"
        )
        self.entry_unit.pack(pady=5)

        self.option_role = ctk.CTkOptionMenu(
            self, values=["Admin", "Petugas", "Pemohon"]
        )
        self.option_role.set("Pilih Role")
        self.option_role.pack(pady=5)

        self.button_register = ctk.CTkButton(
            self, text="Register", command=self.register
        )
        self.button_register.pack(pady=20)

        self.button_to_login = ctk.CTkButton(
            self,
            text="Sudah punya akun? Login",
            fg_color="transparent",
            text_color="blue",
            command=self.show_login_callback,
        )
        self.button_to_login.pack()

    def register(self):
        nama_lengkap = self.entry_nama.get()
        username = self.entry_username.get()
        email = self.entry_email.get()
        password = self.entry_password.get()
        role = self.option_role.get()
        unit = self.entry_unit.get()

        if role == "Pilih Role":
            messagebox.showerror("Error", "Role harus dipilih!")
            return

        if not (nama_lengkap and username and email and password):
            messagebox.showerror("Error", "Semua field wajib diisi!")
            return

        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        try:
            conn = mysql.connector.connect(
                host="localhost", user="root", password="", database="db_ta_kelompok7"
            )
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM pengguna WHERE username = %s OR email = %s",
                (username, email),
            )
            if cursor.fetchone():
                messagebox.showerror("Error", "Username atau Email sudah terdaftar.")
                return

            prefix = {"Admin": "AD", "Petugas": "PG", "Pemohon": "PM"}[role]
            cursor.execute("SELECT COUNT(*) FROM pengguna WHERE role = %s", (role,))
            count = cursor.fetchone()[0] + 1
            id_pengguna = f"{prefix}{str(count).zfill(3)}"

            query = """
                INSERT INTO pengguna (id_pengguna, nama_lengkap, username, email, password, role, unit)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    id_pengguna,
                    nama_lengkap,
                    username,
                    email,
                    hashed_password.decode("utf-8"),
                    role,
                    unit if unit else None,
                ),
            )
            conn.commit()

            messagebox.showinfo("Sukses", "Registrasi berhasil!")
            self.show_login_callback()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Gagal konek ke database:\n{err}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()
