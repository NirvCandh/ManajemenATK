import customtkinter as ctk
from database import connect_db


class TabelPenerimaanPage(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Data Penerimaan Barang")
        self.geometry("850x550")
        self.resizable(False, False)

        ctk.CTkLabel(
            self, text="Tabel Penerimaan Barang", font=("Arial Bold", 20)
        ).pack(pady=20)

        self.scroll_frame = ctk.CTkScrollableFrame(self, width=800, height=450)
        self.scroll_frame.pack(pady=10, padx=10)

        self.tampilkan_data()

    def tampilkan_data(self):
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.callproc("lihat_penerimaan")
            for result in cursor.stored_results():
                data = result.fetchall()
            conn.close()

            # Header tabel
            headers = [
                "ID",
                "Kode Barang",
                "ID Supplier",
                "Jumlah",
                "Tanggal",
                "Harga",
                "ID Petugas",
            ]
            for i, header in enumerate(headers):
                label = ctk.CTkLabel(
                    self.scroll_frame,
                    text=header,
                    font=("Arial", 14, "bold"),
                    anchor="w",
                )
                label.grid(row=0, column=i, padx=10, pady=8, sticky="w")

            # Data baris
            for row_num, row_data in enumerate(data, start=1):
                for col_num, cell_data in enumerate(row_data):
                    cell = ctk.CTkLabel(
                        self.scroll_frame,
                        text=str(cell_data),
                        font=("Arial", 12),
                        anchor="w",
                    )
                    cell.grid(row=row_num, column=col_num, padx=10, pady=4, sticky="w")

        except Exception as e:
            ctk.CTkLabel(
                self, text=f"Gagal mengambil data: {str(e)}", text_color="red"
            ).pack(pady=10)
