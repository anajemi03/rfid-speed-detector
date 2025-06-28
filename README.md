# 🚦 Railway Speed Monitoring and Braking Prototype

🎓 Proyek Tugas Akhir – Teknik Fisika, Telkom University  
📅 Periode: Oktober 2023 – Juli 2024

## 🎯 Tujuan Proyek
Merancang sistem monitoring kecepatan dan pengereman otomatis berbasis sensor untuk meningkatkan keselamatan pada sistem transportasi rel. Prototipe ini mengimplementasikan pemantauan kecepatan dan posisi secara real-time, serta mampu melakukan pengereman otomatis jika kecepatan melebihi batas yang diizinkan.

## 🧪 Sistem yang Dibangun
Proyek ini terdiri dari dua sistem terpisah:
1. **Sistem Monitoring Kecepatan Tinggi** – Diuji pada kendaraan mobil (bukan kereta), menggunakan radar dan RFID untuk mencatat kecepatan dan lokasi.
2. **Sistem Pengereman Otomatis** – Diuji pada mobil robotic skala kecil untuk simulasi pengereman otomatis berdasarkan kecepatan maksimum yang diizinkan.

## 🧩 Komponen & Teknologi
- Jetson Nano (mikrokontroler)
- Radar Sensor (pengukur kecepatan)
- RFID Reader (penanda lokasi statis)
- Motor DC + L298N + PCA9685 (penggerak aktuator)
- Sensor IR/Encoder (pengukur RPM)
- Flask Web Dashboard (tampilan HMI real-time)
- Kalibrasi kecepatan & pengujian lapangan

## 👩‍💻 Peran Saya
- Pemrograman RFID Reader untuk pembacaan posisi
- Kontrol motor DC berbasis pengaturan PWM
- Penghitungan kecepatan menggunakan encoder
- Kalibrasi kecepatan dan pengujian fungsi sistem
- Integrasi antarmuka monitoring berbasis Flask

## 📁 Struktur File 
- `RFIDmotor.py` → Integrasi RFID dan penggerak motor
- `RFIDCINA.py` → Uji coba awal RFID Reader
- `RFIDfix.py` → Versi final RFID
- `OK.py` → Pengujian sederhana RFID Reader

## 📌 Catatan
Sistem ini bersifat **prototipe** dan belum diuji pada kereta sebenarnya. Pengujian dilakukan secara terbatas menggunakan kendaraan simulasi skala kecil.
⚠️ : Beberapa file pada folder `archive/` merupakan hasil eksperimen. Karena pengembangan dilakukan bertahap, tidak semua file memiliki status final. Namun seluruh file menggambarkan proses perancangan sistem yang telah dilakukan secara langsung.

## 📫 Kontak
- Email: anajemifikra3@gmail.com  
- LinkedIn: [Ana Jemi Fikra](https://www.linkedin.com/in/anajemifikra03/)
