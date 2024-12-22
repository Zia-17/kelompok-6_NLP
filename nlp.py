import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pandas as pd

# Fungsi untuk pengenalan ucapan
def recognize_speech_from_mic(recognizer, microphone):
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Mendengarkan...")
            audio = recognizer.listen(source)
              
        print("Memproses audio...")
        transcription = recognizer.recognize_google(audio, language="id-ID")
        return {"success": True, "transcription": transcription}
    except sr.RequestError as e:
        return {"success": False, "error": f"Kesalahan API: {e}"}
    except sr.UnknownValueError:
        return {"success": False, "error": "Tidak dapat mengenali ucapan. Coba lagi."}

# Fungsi untuk mencari harga barang dari dataset berdasarkan kode barang
def cari_Harga_Barang(kode_barang, dataset):
    try:
        print(f"Mencari harga untuk kode barang: {kode_barang}")
        kode_barang = str(kode_barang).lower()

        for _, row in dataset.iterrows():
            kode_barang_dataset = str(row['Kode Barang']).lower()
            if kode_barang == kode_barang_dataset:
                print(f"Harga ditemukan: Harga {row['Harga Barang']}")
                return row['Harga Barang']
            
        print("Harga tidak ditemukan.")
        return 0
    except Exception as e:
        print(f"Error saat mencari harga: {e}")
        return 0

# Fungsi yang dijalankan saat tombol diklik
def on_button_click():
    try:
        if not microphone:
            messagebox.showerror("Error", "Mikrofon tidak tersedia.")
            return

        messagebox.showinfo("Informasi", "Mulai proses pengenalan ucapan...")
        response = recognize_speech_from_mic(recognizer, microphone)

        if not response["success"]:
            messagebox.showerror("Error", response["error"])
            return

        transcription = response["transcription"]
        print(f"Transkripsi: {transcription}")
        transcription = transcription.strip().replace(' ', '')
        print(f"Transkripsi yang sudah diproses: {transcription}")
        
        harga = cari_Harga_Barang(transcription, dataset)
        if harga != 0:
            result_label.config(text=f"Harga Barang: Rp {harga}", fg="#2ECC71")
        else:
            result_label.config(text="Harga tidak ditemukan.", fg="#E74C3C")
    except Exception as e:
        print(f"Error pada fungsi on_button_click: {e}")
        messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

# Inisialisasi GUI
root = tk.Tk()
root.title("Pencarian Harga Barang")
root.geometry("600x400")
root.configure(bg="#2C3E50")

# Frame utama
main_frame = tk.Frame(root, bg="#34495E", padx=20, pady=20)
main_frame.pack(expand=True, fill=tk.BOTH)

# Label judul
title_label = tk.Label(
    main_frame, 
    text="Pencarian Harga Barang", 
    font=("Helvetica", 24, "bold"), 
    bg="#34495E", 
    fg="#1ABC9C"
)
title_label.pack(pady=10)

# Label hasil
result_label = tk.Label(
    main_frame, 
    text="Klik tombol untuk mulai pencarian.", 
    font=("Helvetica", 16), 
    bg="#34495E", 
    fg="#ECF0F1", 
    wraplength=500
)
result_label.pack(pady=20)

# Tombol pencarian
search_button = tk.Button(
    main_frame, 
    text="🔍 Cari Harga Barang", 
    command=on_button_click, 
    bg="#E67E22", 
    fg="white", 
    font=("Helvetica", 14, "bold"), 
    activebackground="#D35400", 
    activeforeground="white", 
    relief=tk.RAISED, 
    padx=20, 
    pady=10
)
search_button.pack(pady=10)

# Footer
footer_label = tk.Label(
    root, 
    text="Kelompok 6 Aplikasi Pencarian Harga Barang", 
    font=("Helvetica", 10), 
    bg="#2C3E50", 
    fg="#BDC3C7"
)
footer_label.pack(side=tk.BOTTOM, pady=10)

# Inisialisasi Speech Recognition
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Membaca dataset dari file CSV
try:
    dataset = pd.read_csv("data barang1.csv")
    print("Dataset berhasil dibaca")
    print(dataset.head())  # Menampilkan beberapa baris awal untuk memastikan data terbaca dengan benar
except Exception as e:
    print(f"Error saat membaca dataset: {e}")
    dataset = pd.DataFrame(columns=['Kode Barang', 'Harga Barang'])

# Jalankan aplikasi
root.mainloop()