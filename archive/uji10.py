import serial
import threading
import time
import csv
from datetime import datetime

# Konfigurasi port serial
rfid_serial_port = serial.Serial("COM8", 115200)

# Fungsi untuk membaca tag
def read_tag(stop_event):
    tag_names = {
        b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x73': "TAG 1",
        b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x76': "TAG 2"
    }
    
    while not stop_event.is_set():  # Selama stop_event belum diset
        # Perintah untuk memulai pembacaan tag
        command = b'\x02\x02\x03\x03\x00\x00\x00'
        
        # Mengirim perintah ke port serial
        rfid_serial_port.write(command)

        # Membaca data dari port serial
        data = rfid_serial_port.read(26)  # Panjang data 26 byte

        # Memproses data tag jika diterima
        if data:
            for tag, name in tag_names.items():
                if tag in data:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    print(name + " terdeteksi:", tag.hex(), " pada ", timestamp)
                    save_to_csv(timestamp, name, tag.hex())  # Simpan data ke CSV
                    break
        else:
            print("Tidak ada data diterima")
        
        time.sleep(0.1)  # Delay untuk mengurangi beban CPU

# Fungsi untuk menyimpan data ke dalam file CSV
def save_to_csv(timestamp, name, tag_id):
    with open('tag_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, name, tag_id])

# Fungsi untuk menghentikan pembacaan RFID
def stop_reading(stop_event):
    stop_event.set()  # Set stop_event untuk memberhentikan pembacaan RFID
    print("Menghentikan pembacaan RFID...")

# Membuat objek event untuk menghentikan pembacaan RFID
stop_event = threading.Event()

# Thread untuk membaca tag secara kontinu
rfid_thread = threading.Thread(target=read_tag, args=(stop_event,))
rfid_thread.start()

try:
    while True:
        time.sleep(0.1)
        data = rfid_serial_port.read_all()
        # Deteksi ID tag tertentu (contoh: E2 00 20 23 12 05 EE AA 00 01 00 73)
        tag_names = {
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x73': "TAG 1",
            b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x76': "TAG 2"
        }
        for tag, name in tag_names.items():
            if tag in data:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(name + " terdeteksi:", tag.hex(), " pada ", timestamp)
                save_to_csv(timestamp, name, tag.hex())  # Simpan data ke CSV
finally:
    # Setelah selesai, panggil fungsi untuk menghentikan pembacaan RFID
    stop_reading(stop_event)
    # Tutup port serial
    rfid_serial_port.close()
