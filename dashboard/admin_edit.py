import customtkinter as ctk
from tkinter import messagebox
from database import connect_db

class EditUserForm(ctk.CTkToplevel):
    def __init__(self, master, user, role, refresh_callback=None):
        super().__init__(master)
        self.user = user
        self.role = role
        self.refresh_callback = refresh_callback  # Simpan callback

        self.title(f"Edit {self.role.capitalize()}")
        self.geometry("400x300")

        # Contoh input sederhana
        self.entry_nama = ctk.CTkEntry(self)
        self.entry_nama.insert(0, user["nama"])
        self.entry_nama.pack(pady=10)

        self.entry_username = ctk.CTkEntry(self)
        self.entry_username.insert(0, user["username"])
        self.entry_username.pack(pady=10)

        self.entry_email = ctk.CTkEntry(self)
        self.entry_email.insert(0, user["email"])
        self.entry_email.pack(pady=10)

        btn_save = ctk.CTkButton(self, text="Simpan", command=self.save)
        btn_save.pack(pady=20)

    def save(self):
        nama = self.entry_nama.get()
        username = self.entry_username.get()
        email = self.entry_email.get()

        if not nama or not username or not email:
            messagebox.showerror("Error", "Semua field harus diisi!")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                UPDATE user SET nama=%s, username=%s, email=%s WHERE id=%s
            """, (nama, username, email, self.user["id"]))
            conn.commit()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update data: {e}")
        else:
            messagebox.showinfo("Sukses", f"{self.role.capitalize()} berhasil diupdate")
            self.destroy()
            if self.refresh_callback:
                self.refresh_callback()
        finally:
            conn.close()
