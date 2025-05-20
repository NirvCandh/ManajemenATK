import customtkinter as ctk
from tkcalendar import DateEntry
from tkinter import messagebox
from database import connect_db


class EditPengeluaranPage(ctk.CTkToplevel):
    def __init__(self, parent, data_pengeluaran):
        super().__init__(parent)
        self.title("Edit Pengeluaran Barang")
        self.geometry("400x470")
        self.resizable(False, False)

        (
            self.id_pengeluaran,
            kode_barang,
            jml_keluar,
            tgl_keluar,
            tujuan,
            id_pemohon,
            id_petugas,
        ) = data_pengeluaran

        ctk.CTkLabel(self, text="Kode Barang:").pack(pady=(15, 5))
        self.entry_kode = ctk.CTkEntry(self)
        self.entry_kode.pack(pady=5)
        self.entry_kode.insert(0, kode_barang)

        ctk.CTkLabel(self, text="Jumlah Keluar:").pack(pady=5)
        self.entry_jml = ctk.CTkEntry(self)
        self.entry_jml.pack(pady=5)
        self.entry_jml.insert(0, str(jml_keluar))

        # Tanggal Keluar (pakai DateEntry tapi dibungkus frame supaya size mirip entry)
        ctk.CTkLabel(self, text="Tanggal Keluar:").pack(pady=5)
        frame_tgl = ctk.CTkFrame(self, corner_radius=8)
        frame_tgl.pack(pady=5, padx=20, fill="x")

        self.entry_tgl = DateEntry(
            frame_tgl,
            date_pattern="yyyy-MM-dd",
            background="blue",
            foreground="white",
            borderwidth=0,
            font=("Helvetica", 14),
            relief="flat",
            width=15,
            justify="center",
        )
        self.entry_tgl.pack(fill="x", padx=5, pady=2)
        self.entry_tgl.set_date(tgl_keluar)

        # Tujuan
        ctk.CTkLabel(self, text="Tujuan:").pack(pady=5)
        self.entry_tujuan = ctk.CTkEntry(self)
        self.entry_tujuan.pack(pady=5)
        self.entry_tujuan.insert(0, tujuan)

        # ID Pemohon
        ctk.CTkLabel(self, text="ID Pemohon:").pack(pady=5)
        self.entry_pemohon = ctk.CTkEntry(self)
        self.entry_pemohon.pack(pady=5)
        self.entry_pemohon.insert(0, id_pemohon)

        # ID Petugas
        ctk.CTkLabel(self, text="ID Petugas:").pack(pady=5)
        self.entry_petugas = ctk.CTkEntry(self)
        self.entry_petugas.pack(pady=5)
        self.entry_petugas.insert(0, id_petugas)

        # Tombol Simpan
        btn_simpan = ctk.CTkButton(
            self, text="Simpan Perubahan", command=self.update_data
        )
        btn_simpan.pack(pady=20)

    def update_data(self):
        kode = self.entry_kode.get().strip()
        try:
            jumlah = int(self.entry_jml.get().strip())
            if jumlah < 0:
                raise ValueError("Jumlah tidak boleh negatif")
        except ValueError:
            messagebox.showerror("Error", "Jumlah harus berupa angka bulat positif.")
            return

        tgl = self.entry_tgl.get_date().strftime("%Y-%m-%d")
        tujuan = self.entry_tujuan.get().strip()
        pemohon = self.entry_pemohon.get().strip()
        petugas = self.entry_petugas.get().strip()

        if not (kode and tgl and tujuan and pemohon and petugas):
            messagebox.showerror("Error", "Semua field harus diisi.")
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.callproc(
                "update_pengeluaran",
                (self.id_pengeluaran, kode, jumlah, tgl, tujuan, pemohon, petugas),
            )
            conn.commit()
            conn.close()
            messagebox.showinfo("Sukses", "Data pengeluaran berhasil diperbarui.")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update data: {str(e)}")
