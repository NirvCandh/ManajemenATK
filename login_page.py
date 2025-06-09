import customtkinter as ctk
import bcrypt
from tkinter import messagebox
from database import connect_db


class LoginApp(ctk.CTkFrame):
    def __init__(self, master, login_success_callback, show_register_callback):
        super().__init__(master)
        self.login_success_callback = login_success_callback
        self.show_register_callback = show_register_callback

        ctk.CTkLabel(self, text="ATK Manager", font=("Arial Black", 26)).pack(pady=30)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.role_dropdown = ctk.CTkOptionMenu(
            self, values=["Admin", "Petugas", "Pemohon"]
        )
        self.role_dropdown.pack(pady=10)
        self.role_dropdown.set("Admin")

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=10)

        label1 = ctk.CTkLabel(frame, text="Belum punya akun?", text_color="black")
        label1.pack(side="left")

        label2 = ctk.CTkLabel(
            frame,
            text="Daftar di sini",
            text_color="#1f6aa5",
            cursor="hand2",
            font=("Arial Bold", 10),
        )
        label2.pack(side="left", padx=5)
        label2.bind("<Button-1>", lambda e: self.show_register_callback())

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        selected_role = self.role_dropdown.get()

        if not email or not password:
            messagebox.showerror("Error", "Email dan password harus diisi!")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            query = "SELECT id_pengguna, password, role, nama_lengkap FROM pengguna WHERE email=%s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()

            if result:
                id_pengguna_db, stored_hash, db_role, nama_lengkap = result

                if bcrypt.checkpw(
                    password.encode("utf-8"), stored_hash.encode("utf-8")
                ):
                    if db_role.lower() != selected_role.lower():
                        messagebox.showerror(
                            "Role Tidak Sesuai",
                            "Role yang dipilih tidak cocok dengan data di database.",
                        )
                        return

                    messagebox.showinfo(
                        "Login Berhasil", f"Halo {nama_lengkap} ({db_role})!"
                    )
                    # Ubah di sini: oper 3 argumen
                    self.login_success_callback(db_role, id_pengguna_db, nama_lengkap)

                else:
                    messagebox.showerror("Gagal", "Password salah!")
            else:
                messagebox.showerror("Gagal", "Email tidak ditemukan!")

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")

        finally:
            try:
                cursor.close()
                conn.close()
            except:
                pass
