import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class LoginApp(ctk.CTk):
    def __init__(self, login_success_callback):
        super().__init__()

        self.login_success_callback = login_success_callback

        self.title("Login - Manajemen ATK")
        self.geometry("400x450")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="ATK Manager", font=("Arial Black", 26)).pack(pady=30)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=10)

        self.role_dropdown = ctk.CTkOptionMenu(self, values=["admin", "staff", "pemohon"])
        self.role_dropdown.pack(pady=10)
        self.role_dropdown.set("admin")  # Default value

        ctk.CTkButton(self, text="Login", command=self.login).pack(pady=20)
        ctk.CTkLabel(self, text="© 2025 Instansi Lo", font=("Arial", 10)).pack(side="bottom", pady=10)

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
            self.destroy()
        else:
            messagebox.showerror("Gagal", "Email atau password salah!")

if __name__ == "__main__":
    def dummy_callback(role):
        print("Login sukses, role:", role)

    app = LoginApp(dummy_callback)
    app.mainloop()
    