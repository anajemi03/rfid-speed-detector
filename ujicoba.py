import csv
import serial
import time

test_serial = serial.Serial('COM3', 115200, timeout=0.1)
INVENTORY = 'BB 00 22 00 00 22 7E'

# Tambahkan kamus untuk konversi ID ke kata-kata
id_to_words = {
    "6C DC B9 33": "Blok 1",
    "88 DD 43 D1": "Blok 1",
    "40 DD EA 99": "Blok 1",
    # Tambahkan ID dan kata-kata lainnya sesuai kebutuhan
}

def send_cmd(cmd):
    data = bytes.fromhex(cmd)
    test_serial.write(data)
    response = test_serial.read(1000)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    
    if hex_space == 'BB 01 FF 00 01 15 16 7E':
        return "no respon"
    elif hex_space.startswith('BB 02 22 00'):
        return hex_space.split()[-6:-2]  # Ambil ID saja
    else: 
        return None

def convert_id_to_words(tag_id):
    if tag_id == "no respon":
        return "No respon"
    elif tag_id in id_to_words:
        return id_to_words[tag_id]
    else:
        return "ID Tidak Dikenali"

try:
    with open('rfid_data.csv', 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        
        # Header file CSV
        csv_writer.writerow(['Timestamp', 'Tag ID', 'Nama'])

        while True:
            timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            tag_id = send_cmd(INVENTORY)
            if tag_id: 
                if isinstance(tag_id, list):  # Cek apakah tag_id adalah list (ID ditemukan)
                    id_str = ' '.join(tag_id)
                    name = convert_id_to_words(id_str)
                    csv_writer.writerow([timestamp, id_str, name])
                else:
                    name = convert_id_to_words(tag_id)
                    csv_writer.writerow([timestamp, tag_id, name])
            time.sleep(0.1)
                
except KeyboardInterrupt:
    print("Proses pembacaan dihentikan.")
    test_serial.close()