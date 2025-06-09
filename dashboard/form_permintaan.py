import customtkinter as ctk
from tkinter import messagebox
from database import connect_db
import datetime


class FormPermintaanPage(ctk.CTkToplevel):
    def __init__(self, id_permintaan, id_petugas, nama_petugas, refresh_callback):
        super().__init__()
        self.title("Form Proses Permintaan")
        self.geometry("400x400")
        self.resizable(False, False)
        self.id_permintaan = id_permintaan
        self.id_petugas = id_petugas
        self.nama_petugas = nama_petugas
        self.refresh_callback = refresh_callback

        ctk.CTkLabel(self, text="Form Proses Permintaan", font=("Arial Bold", 18)).pack(
            pady=10
        )

        self.kelas_entry = self.create_labeled_entry("Kelas Tujuan")
        self.status_option = self.create_status_dropdown()

        ctk.CTkButton(self, text="Proses", command=self.proses_permintaan).pack(pady=20)

    def create_labeled_entry(self, label_text):
        ctk.CTkLabel(self, text=label_text).pack(pady=(10, 0))
        entry = ctk.CTkEntry(self)
        entry.pack(pady=5)
        return entry

    def create_status_dropdown(self):
        ctk.CTkLabel(self, text="Status").pack(pady=(10, 0))
        dropdown = ctk.CTkOptionMenu(self, values=["Disetujui", "Ditolak"])
        dropdown.set("Disetujui")
        dropdown.pack(pady=5)
        return dropdown

    def proses_permintaan(self):
        kelas = self.kelas_entry.get().strip()
        status = self.status_option.get()
        tanggal = datetime.date.today()

        if not kelas:
            messagebox.showwarning("Input Error", "Kelas tujuan tidak boleh kosong.")
            return

        conn = connect_db()
        cursor = conn.cursor()

        try:
            # Update status permintaan
            cursor.execute(
                """
                UPDATE permintaan
                SET status = %s, id_petugas = %s, tgl_setuju = %s
                WHERE id_permintaan = %s
            """,
                (status, self.id_petugas, tanggal, self.id_permintaan),
            )

            cursor.execute(
                """
                SELECT dp.kode_barang, dp.jumlah, p.id_pemohon
                FROM detail_permintaan dp
                JOIN permintaan p ON p.id_permintaan = dp.id_permintaan
                WHERE dp.id_permintaan = %s
            """,
                (self.id_permintaan,),
            )
            detail = cursor.fetchall()

            cursor.execute("SELECT MAX(id_pengeluaran) FROM pengeluaran")
            last_id = cursor.fetchone()[0]
            new_id = 1 if last_id is None else last_id + 1

            for kode_barang, jumlah, id_pemohon in detail:
                cursor.execute(
                    """
                    INSERT INTO pengeluaran (id_pengeluaran, kode_barang, jml_keluar, tgl_keluar, tujuan, id_pemohon, id_petugas)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                    (
                        new_id,
                        kode_barang,
                        jumlah,
                        tanggal,
                        kelas,
                        id_pemohon,
                        self.id_petugas,
                    ),
                )
                new_id += 1

            conn.commit()
            messagebox.showinfo(
                "Sukses",
                "Permintaan berhasil diproses dan dicatat sebagai pengeluaran.",
            )
            self.destroy()
            self.refresh_callback()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error", f"Gagal memproses permintaan:\n{e}")
        finally:
            conn.close()
