# iCloud Email Bot

Bot untuk membuat email iCloud secara otomatis menggunakan data acak dari RandomUser.me API.

## Deskripsi

iCloud Email Bot adalah alat otomatisasi yang dirancang untuk membantu pembuatan akun email iCloud dengan menggunakan data pengguna acak. Bot ini menggunakan Selenium WebDriver untuk mengotomatisasi proses pendaftaran di situs Apple ID dan RandomUser.me API untuk menghasilkan data pengguna yang realistis.

## Fitur

- Menghasilkan data pengguna acak (nama, tanggal lahir, dll.) menggunakan RandomUser.me API
- Mengotomatisasi proses pendaftaran akun Apple ID
- Menyimpan informasi akun yang dibuat dalam file JSON
- Mendukung pembuatan beberapa akun secara berurutan
- Opsi untuk menggunakan proxy untuk meningkatkan privasi
- Mode headless untuk menjalankan bot tanpa UI browser

## Persyaratan Sistem

- Python 3.6 atau lebih baru
- Koneksi internet yang stabil
- Chrome browser
- Sistem operasi: Windows, macOS, atau Linux

### Dependensi Python

- selenium
- webdriver-manager
- requests

## Instalasi

1. Pastikan Python 3.6+ sudah terinstal di sistem Anda
2. Clone atau download repositori ini
3. Instal dependensi yang diperlukan:

```bash
pip install selenium webdriver-manager requests
```

4. Pastikan Chrome browser sudah terinstal di sistem Anda

## Struktur Proyek

```
icloud_email_bot/
├── src/
│   ├── random_data_generator.py  # Generator data acak
│   ├── icloud_email_bot.py       # Bot utama
│   └── test_bot.py               # Skrip pengujian
├── accounts.json                 # File untuk menyimpan informasi akun
└── README.md                     # Dokumentasi
```

## Penggunaan

### Menjalankan Bot

Untuk menjalankan bot dengan konfigurasi default (membuat 1 akun):

```bash
python src/icloud_email_bot.py
```

Untuk membuat beberapa akun:

```bash
python src/icloud_email_bot.py --count 3
```

Untuk menjalankan bot dalam mode headless (tanpa UI browser):

```bash
python src/icloud_email_bot.py --headless
```

Untuk menggunakan proxy:

```bash
python src/icloud_email_bot.py --proxy socks5://127.0.0.1:9050
```

### Opsi Baris Perintah

- `--count`: Jumlah akun yang akan dibuat (default: 1)
- `--headless`: Menjalankan browser dalam mode headless
- `--proxy`: Server proxy yang akan digunakan (format: protocol://host:port)

## Keterbatasan dan Intervensi Manual

Bot ini memiliki beberapa keterbatasan yang memerlukan intervensi manual:

1. **Verifikasi Kode**: Apple mengirimkan kode verifikasi ke nomor telepon yang diberikan. Bot akan meminta Anda untuk memasukkan kode ini secara manual.

2. **CAPTCHA**: Jika Apple menampilkan CAPTCHA, Anda perlu menyelesaikannya secara manual.

3. **Deteksi Bot**: Apple mungkin mendeteksi aktivitas otomatis dan memblokir akses. Menggunakan proxy dan menambahkan jeda waktu antara pembuatan akun dapat membantu mengurangi risiko ini.

4. **Perubahan Situs**: Jika Apple mengubah struktur situs web mereka, bot mungkin perlu diperbarui.

## Pengujian

Untuk menguji fungsionalitas bot tanpa benar-benar membuat akun:

```bash
python src/test_bot.py
```

Ini akan menguji generator data acak dan komponen bot lainnya tanpa melakukan pendaftaran aktual.

## Kustomisasi

### Mengubah Sumber Data

Bot ini menggunakan RandomUser.me API sebagai sumber data acak. Jika Anda ingin menggunakan sumber data lain, Anda dapat memodifikasi kelas `RandomDataGenerator` di `src/random_data_generator.py`.

### Menyesuaikan Format Apple ID

Format Apple ID default yang dihasilkan dapat disesuaikan dengan mengedit metode `generate_apple_id()` di `src/random_data_generator.py`.

## Pemecahan Masalah

### Selenium WebDriver Error

Jika Anda mengalami masalah dengan WebDriver:

1. Pastikan Chrome browser terinstal dan up-to-date
2. Coba instal ulang webdriver-manager: `pip install --upgrade webdriver-manager`

### Masalah Koneksi API

Jika RandomUser.me API tidak dapat diakses:

1. Periksa koneksi internet Anda
2. Coba gunakan proxy alternatif
3. Tunggu beberapa saat dan coba lagi

## Catatan Keamanan

Bot ini dirancang untuk tujuan pendidikan dan pengujian. Penggunaan bot ini untuk membuat akun palsu dalam jumlah besar dapat melanggar Ketentuan Layanan Apple. Gunakan dengan bijak dan bertanggung jawab.

## Pengembangan Lebih Lanjut

Beberapa ide untuk pengembangan lebih lanjut:

- Menambahkan dukungan untuk browser lain (Firefox, Edge)
- Implementasi rotasi proxy otomatis
- Menambahkan GUI untuk memudahkan penggunaan
- Menambahkan dukungan untuk layanan email lain (Gmail, Outlook, dll.)

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](https://opensource.org/licenses/MIT).
