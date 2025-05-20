import customtkinter as ctk
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

        self.role_dropdown = ctk.CTkOptionMenu(self, values=["admin", "staff", "pemohon"])
        self.role_dropdown.pack(pady=10)
        self.role_dropdown.set("admin")

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(pady=10)

        label1 = ctk.CTkLabel(frame, text="Belum punya akun?", text_color="black")
        label1.pack(side="left")
        
        label2 = ctk.CTkLabel(frame, text="Daftar di sini", text_color="#1f6aa5", cursor="hand2", font=("Arial Bold", 10))
        label2.pack(side="left", padx=5)

        label2.bind("<Button-1>", lambda e: self.show_register_callback())

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()
        selected_role = self.role_dropdown.get()

        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT role FROM user WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            db_role = result[0]
            if db_role != selected_role:
                messagebox.showerror("Role Tidak Sesuai", "Role yang dipilih tidak cocok dengan data.")
                return

            messagebox.showinfo("Login Berhasil", f"Halo {db_role}!")
            self.login_success_callback(db_role)
        else:
            messagebox.showerror("Gagal", "Email atau password salah!")
