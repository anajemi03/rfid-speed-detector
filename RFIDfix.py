import serial 
import time
test_serial = serial.Serial('COM10', 115200, timeout=0.1)

INVENTORY = 'BB 00 22 00 00 22 7E'

def send_cmd(cmd):
    data = bytes.fromhex(cmd)
    test_serial.write(data)
    response = test_serial.read(512)
    response_hex = response.hex().upper()
    hex_list = [response_hex[i:i+2] for i in range(0, len(response_hex), 2)]
    hex_space = ' '.join(hex_list)
    print(hex_space)

try:
    while True:
        send_cmd(INVENTORY)
        time.sleep(0.1)  # Tunggu 1 detik sebelum membaca lagi
except KeyboardInterrupt:
    print("Proses pembacaan dihentikan.")
    test_serial.close()