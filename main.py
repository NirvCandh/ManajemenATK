import customtkinter as ctk
from dashboard.admin_dashboard import AdminDashboard

if __name__ == "__main__":
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    app = AdminDashboard()
    app.mainloop()
