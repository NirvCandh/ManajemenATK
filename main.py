import customtkinter as ctk
from login_page import LoginApp
from dashboard.admin_dashboard import AdminDashboard
from dashboard.staff_dashboard import StaffDashboard
from dashboard.pemohon_dashboard import PemohonDashboard
from register import RegisterApp


if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = StaffDashboard()
    app.mainloop()

# class MainApp:
#     def __init__(self):
#         ctk.set_appearance_mode("light")
#         ctk.set_default_color_theme("blue")

#         self.root = ctk.CTk()
#         self.root.title("ATK Manager")
#         self.root.geometry("500x500")

#         self.current_frame = None
#         self.show_login()

#         self.root.mainloop()

#     def clear_frame(self):
#         if self.current_frame:
#             self.current_frame.destroy()

#     def show_login(self):
#         self.clear_frame()
#         self.current_frame = LoginApp(self.root, self.on_login_success, self.show_register)
#         self.current_frame.pack(expand=True, fill="both")

#     def show_register(self):
#         self.clear_frame()
#         self.current_frame = RegisterApp(self.root, self.show_login)
#         self.current_frame.pack(expand=True, fill="both")

#     def on_login_success(self, role):
#         self.clear_frame()

#         if role == "admin":
#             self.current_frame = AdminDashboard(self.root)
#         elif role == "staff":
#             self.current_frame = StaffDashboard(self.root)
#         elif role == "pemohon":
#             self.current_frame = PemohonDashboard(self.root)
#         else:
#             print("Role tidak dikenal")
#             return

#         self.current_frame.pack(expand=True, fill="both")

# if __name__ == "__main__":
#     app = MainApp()
