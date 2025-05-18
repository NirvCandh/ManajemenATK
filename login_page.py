import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class LoginApp(ctk.CTk):
    def __init__(self, login_success_callback):
        super().__init__()

        self.login_success_callback = login_success_callback

        self.title("Login - Manajemen ATK")
        self.geometry("400x400")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="ATK Manager", font=("Arial Black", 26)).pack(pady=30)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)
        ctk.CTkLabel(self, text="© 2025 Instansi Lo", font=("Arial", 10)).pack(side="bottom", pady=10)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT role FROM user WHERE email=%s AND password=%s"
        cursor.execute(query, (email, password))
        result = cursor.fetchone()
        conn.close()

        if result:
            role = result[0]
            messagebox.showinfo("Login Berhasil", f"Halo {role}!")
            self.login_success_callback(role)  # Panggil callback dari MainApp
            self.destroy()
        else:
            messagebox.showerror("Gagal", "Email atau password salah!")

if __name__ == "__main__":
    def dummy_callback(role):
        print("Login sukses, role:", role)

    app = LoginApp(dummy_callback)
    app.mainloop()
