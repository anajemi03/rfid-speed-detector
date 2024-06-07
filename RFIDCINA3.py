import serial
import threading
import time
import csv
from datetime import datetime

# Konfigurasi port serial
rfid_serial_port = serial.Serial("COM12", 115200)

# Fungsi untuk memformat ID tag dengan spasi
def format_tag_id(tag_id):
    return ' '.join(format(byte, '02X') for byte in tag_id)

# Fungsi untuk membaca tag
def read_tag(stop_event):
    tag_names = {
        b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x73': "TAG 1",
        b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x76': "TAG 2",
        b'\xE2\x00\x20\x23\x12\x05\xEE\xAA\x00\x01\x00\x90': "TAG 3"  # Tag baru yang ditambahkan
    }
    
    while not stop_event.is_set():
        command = b'\x43\x4D\x02\x02\x00\x00\x00\x00'  # Perintah yang benar
        rfid_serial_port.write(command)
        data = rfid_serial_port.read(26)

        if data:
            for tag, name in tag_names.items():
                if tag in data:
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    formatted_tag = format_tag_id(tag)
                    print(name + " terdeteksi:", formatted_tag, " pada ", timestamp)
                    save_to_csv(timestamp, name, formatted_tag)
                    break
        else:
            print("Tidak ada data diterima")
        
        time.sleep(0.1)

# Fungsi untuk menyimpan data ke dalam file CSV
def save_to_csv(timestamp, name, tag_id):
    with open('tag_data.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, name, tag_id])

# Fungsi untuk menghentikan pembacaan RFID
def stop_reading(stop_event):
    stop_event.set()
    print("Menghentikan pembacaan RFID...")

# Membuat objek event untuk menghentikan pembacaan RFID
stop_event = threading.Event()

# Thread untuk membaca tag secara kontinu
rfid_thread = threading.Thread(target=read_tag, args=(stop_event,))
rfid_thread.start()

try:
    while True:
        user_input = input("Ketik 'stop' untuk menghentikan pembacaan RFID: ")
        if user_input.lower() == 'stop':
            break
        time.sleep(0.1)
finally:
    # Setelah selesai, panggil fungsi untuk menghentikan pembacaan RFID
    stop_reading(stop_event)
    # Menunggu thread selesai
    rfid_thread.join()

    # Perintah untuk menghentikan operasi RFID
    stop_command = b'\x43\x4D\x03\x02\x02\x00\x00\x00\x00'
    rfid_serial_port.write(stop_command)

    # Membaca respons dari perangkat
    response = rfid_serial_port.read(10)  # Panjang respons 10 byte
    if response == b'\x43\x4D\x03\x03\x03\x00\x00\x00\x00\x00':
        print("Pembacaan RFID berhasil dihentikan.")
    else:
        print("Gagal menghentikan pembacaan RFID.")

    # Tutup port serial
    rfid_serial_port.close()
