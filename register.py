import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
from login_page import LoginApp 

class RegisterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Register - Manajemen ATK")
        self.geometry("400x500")
        self.resizable(False, False)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        ctk.CTkLabel(self, text="Daftar Akun", font=("Arial Bold", 24)).pack(pady=20)

        self.nama_entry = ctk.CTkEntry(self, placeholder_text="Nama Lengkap")
        self.nama_entry.pack(pady=8)

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username")
        self.username_entry.pack(pady=8)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email")
        self.email_entry.pack(pady=8)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Password", show="*")
        self.password_entry.pack(pady=8)

        self.role_combobox = ctk.CTkComboBox(self, values=["admin", "staff", "pemohon"])
        self.role_combobox.pack(pady=8)
        self.role_combobox.set("pemohon")

        label_frame = ctk.CTkFrame(self, fg_color="transparent")
        label_frame.pack(pady=5)

        ctk.CTkLabel(label_frame, text="Sudah punya akun?", font=("Poppins", 10)).pack(side="left")

        self.login_label = ctk.CTkLabel(
            label_frame,
            text="Login di sini",
            text_color="#1f6aa5",
            font=("Arial Bold", 10),
            cursor="hand2"
        )
        self.login_label.pack(side="left", padx=4)

        self.login_label.bind("<Enter>", lambda e: self.login_label.configure(underline=True, text_color="#144e85"))
        self.login_label.bind("<Leave>", lambda e: self.login_label.configure(underline=False, text_color="#1f6aa5"))
        self.login_label.bind("<Button-1>", lambda e: self.open_login())

    def register(self):
        nama = self.nama_entry.get()
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()
        role = self.role_combobox.get()

        if not all([nama, username, email, password]):
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        query = "INSERT INTO user (nama, username, email, password, role) VALUES (%s, %s, %s, %s, %s)"
        try:
            cursor.execute(query, (nama, username, email, password, role))
            conn.commit()
            messagebox.showinfo("Sukses", "Registrasi berhasil. Silakan login.")
            conn.close()
            self.destroy()  

            login_window = LoginApp()
            login_window.mainloop()

        except Exception as e:
            messagebox.showerror("Error", f"Gagal registrasi: {str(e)}")
            conn.close()
            
    def open_login(self):
        self.destroy()
        login = LoginApp()
        login.mainloop()

if __name__ == "__main__":
    app = RegisterApp()
    app.mainloop()
