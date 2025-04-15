# Flappy Bird Game

Sebuah implementasi sederhana dari game Flappy Bird menggunakan Python dan Pygame.

## Persyaratan Sistem

- Python 3.x
- Pygame

## Instalasi

1. Pastikan Python sudah terinstal di komputer Anda. Jika belum, download dan install dari [python.org](https://www.python.org/downloads/)

2. Install Pygame menggunakan pip:
   ```
   pip install pygame
   ```

## Cara Menjalankan Game

1. Clone atau download repository ini
2. Buka terminal atau command prompt
3. Pindah ke direktori game:
   ```
   cd path/to/FlappyBirdGame
   ```
4. Jalankan game:
   ```
   python flappy_bird.py
   ```

## Cara Bermain

- Tekan SPASI untuk membuat burung melompat/terbang ke atas
- Hindari pipa-pipa hijau
- Jika burung menabrak pipa atau menyentuh batas atas/bawah layar, permainan berakhir
- Tekan SPASI untuk memulai permainan baru ketika game over

## Fitur

- Sistem high score yang tersimpan
- Animasi rotasi burung berdasarkan kecepatan
- Latar belakang langit biru
- Tampilan skor real-time

## Catatan

- Game akan secara otomatis menyimpan high score ke dalam file `high_score.txt`
- Jika file sprite burung (`bird.svg`) tidak ditemukan, game akan menggunakan kotak biru sebagai pengganti
