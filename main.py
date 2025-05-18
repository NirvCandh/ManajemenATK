import customtkinter as ctk
from login_page import LoginApp
from dashboard.admin_dashboard import AdminDashboard
from dashboard.staff_dashboard import StaffDashboard
from dashboard.pemohon_dashboard import PemohonDashboard

class MainApp:
    def __init__(self):
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.window = None
        self.show_login()

    def show_login(self):
        if self.window:
            self.window.destroy()
        self.window = LoginApp(self.on_login_success)
        self.window.mainloop()

    def on_login_success(self, role):
        self.window.destroy()

        if role == "admin":
            self.window = AdminDashboard()
        elif role == "staff":
            self.window = StaffDashboard()
        elif role == "pemohon":
            self.window = PemohonDashboard()
        else:
            print("Role tidak dikenal")
            self.show_login()
            return

        self.window.mainloop()

if __name__ == "__main__":
    app = MainApp()
    