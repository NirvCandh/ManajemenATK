import customtkinter as ctk
from login_page import LoginApp
from dashboard.admin_dashboard import AdminDashboard
from dashboard.staff_dashboard import StaffDashboard
from dashboard.pemohon_dashboard import PemohonDashboard
from register import RegisterPage


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        self.title("Manajemen ATK")
        self.geometry("700x500")
        self.resizable(False, False)

        self.show_register()

    def show_register(self):
        self.clear_widgets()
        register_frame = RegisterPage(self, self.show_login)
        register_frame.pack(expand=True, fill="both")

    def show_login(self):
        self.clear_widgets()
        login_frame = LoginApp(self, self.login_success, self.show_register)
        login_frame.pack(expand=True, fill="both")

    def login_success(self, role, id_pengguna, nama_lengkap):
        self.clear_widgets()
        if role == "Admin":
            dashboard = AdminDashboard()
        elif role == "Petugas":
            dashboard = StaffDashboard(
                id_petugas=id_pengguna, nama_petugas=nama_lengkap
            )
        elif role == "Pemohon":
            dashboard = PemohonDashboard(current_pengguna_id=id_pengguna)
        else:
            ctk.CTkLabel(self, text="Role tidak dikenal").pack()
            return

        dashboard.mainloop()

    def clear_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
