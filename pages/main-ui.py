import customtkinter as ctk
import login_page 
from dashboard.admin_dashboard import AdminDashboard
from dashboard.staff_dashboard import StaffDashboard
from dashboard.pemohon_dashboard import PemohonDashboard

class MainApp:
    def __init__(self):
        self.current_window = None
        self.show_login()

    def show_login(self):
        if self.current_window:
            self.current_window.destroy()
        self.current_window = login_page(self.on_login_success)
        self.current_window.mainloop()

    def on_login_success(self, role):
        self.current_window.destroy()
        if role == "admin":
            self.current_window = AdminDashboard()
        elif role == "staff":
            self.current_window = StaffDashboard()
        elif role == "pemohon":
            self.current_window = PemohonDashboard()
        else:
            # fallback kalau role gak dikenali
            print("Role tidak dikenal:", role)
            self.show_login()
            return
        self.current_window.mainloop()

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    app = MainApp()
