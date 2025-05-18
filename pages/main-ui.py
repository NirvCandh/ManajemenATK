from login_page import LoginApp
from dashboard.admin_dashboard import AdminDashboard
from dashboard.staff_dashboard import StaffDashboard
from dashboard.pemohon_dashboard import PemohonDashboard
import customtkinter as ctk

class MainApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.current_window = None
        self.show_login()
        ctk.CTk().mainloop()  # panggil mainloop sekali di sini

    def show_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = LoginApp(self.on_login_success)

    def on_login_success(self, role):
        if self.current_window:
            self.current_window.destroy()

        if role == "admin":
            self.current_window = AdminDashboard()
        elif role == "staff":
            self.current_window = StaffDashboard()
        elif role == "pemohon":
            self.current_window = PemohonDashboard()
        else:
            print("Role tidak dikenal:", role)
            self.show_login()
            return

if __name__ == "__main__":
    app = MainApp()
