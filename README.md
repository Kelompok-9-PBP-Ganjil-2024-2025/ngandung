## Ngandung (Ngemil di Bandung)

### Daftar Isi

1. [Nama-nama anggota kelompok](#1-nama-nama-anggota-kelompok)
2. [Deskripsi aplikasi](#2-deskripsi-aplikasi)
3. [Daftar modul aplikasi](#3-daftar-modul-aplikasi)
4. [Sumber _intial_ dataset](#4-sumber-intial-dataset)
5. [_Role_ pengguna berdasarkan deskripsinya](#5-_Role_-pengguna-berdasarkan-deskripsinya)
6. [URL _deployment_ PWS](#6-url-deployment-pws)

### 1. Nama-nama anggota kelompok

-   Ahmad Dzulfikar As Shavy (2306152374) - `AhmadDzulfikar`
-   Muhammad Radhiya Arshq (2306275885) - `arshqiii`
-   Christian Raphael Heryanto (2306152323) - `papaChick`
-   Rayhan Syahdira Putra (2306275903) - `RayhanSP`
-   Daffa Abhipraya Putra (2306245131) - `absolutepraya`

### 2. Deskripsi aplikasi

Ngandung adalah aplikasi berbasis web yang menyediakan informasi lengkap tentang makanan dan toko-toko di kota tertentu. Aplikasi ini dirancang untuk memudahkan pengguna yang baru pindah atau berkunjung ke kota tersebut dalam menemukan berbagai jenis makanan dan tempat membelinya. Pengguna dapat mencari makanan berdasarkan kategori, melihat daftar rekomendasi, memberikan rating serta ulasan untuk toko, dan menyimpan toko favorit mereka. Admin memiliki kemampuan untuk menambahkan dan mengelola data makanan dan toko yang tersedia, sementara pengguna biasa dapat mengakses informasi dan memberikan ulasan. Ngandung bertujuan untuk memberikan solusi praktis dalam mencari makanan di kota baru dengan mudah dan cepat.

### 3. Daftar modul aplikasi

#### a. Modul wajib:

-   _**Authentication**_ **and** _**Authorization**_  
    Modul ini berfungsi untuk mengatur _authentication_ pengguna. Pengguna dapat mendaftar, masuk, dan keluar dari aplikasi.

#### b. Modul/fitur aplikasi:

-   **Daftar Makanan Rekomendasi**  
    Modul ini berfungsi untuk menampilkan daftar makanan yang tersedia. Pengguna dapat melihat informasi makanan yang diinginkan.

    **_Dikerjakan oleh:_** ...

-   **_Rating_ & _Review_ Toko**  
    Modul ini berfungsi untuk memberikan _rating_ & _review_ ke toko yang tersedia.

    **_Dikerjakan oleh:_** ...

-   **Toko Favorit**  
    Modul ini berfungsi untuk menyimpan toko yang disukai oleh pengguna.

    **_Dikerjakan oleh:_** ...

-   **Pencarian Makanan**  
    Modul ini berfungsi untuk mencari makanan yang diinginkan oleh pengguna.

    **_Dikerjakan oleh:_** ...

-   **Tambah Toko & Makannya**  
    Modul ini berfungsi untuk menambahkan toko dan makanan yang tersedia di toko tersebut.

    **_Dikerjakan oleh:_** ...

### 4. Sumber _intial_ dataset

[Open Data Kota Bandung](https://opendata.bandung.go.id/dataset/data-rumah-makan-restoran-cafe-di-kota-bandung)

### 5. **Role** pengguna (_User_ dan _Admin_)

| No. | Modul                      | _Permission User_                                                                                             | _Permission Admin_                                                                                                                   |
| --- | -------------------------- | ------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| 1   | Daftar Makanan Rekomendasi | Pengguna dapat mengakses informasi makanan yang tersedia di aplikasi, tanpa dapat mengubah atau menghapusnya. | Admin dapat mengakses informasi makanan yang tersedia di aplikasi, dan dapat menambahkan, mengubah, atau menghapus makanan tersebut. |
| 2   | Rating & Review Toko       | Pengguna dapat memberikan rating dengan range 1-5 dan review berupa teks singkat ke toko yang tersedia.       | Admin dapat melihat rating dan review dari toko yang tersedia.                                                                       |
| 3   | Toko Favorit               | Pengguna dapat menyimpan toko yang disukai ke 'Toko Favorit' yang dimiliki setiap akun pengguna.              | Admin tidak dapat menyimpan toko yang disukai ke 'Toko Favorit'.                                                                     |
| 4   | Pencarian Makanan          | Pengguna dapat mencari makanan yang diinginkan di aplikasi melalui search bar.                                | Admin dapat mencari makanan yang diinginkan di aplikasi melalui search bar.                                                          |
| 5   | Tambah Toko & Makannya     | Pengguna tidak dapat menambahkan toko dan makanan yang tersedia di toko tersebut.                             | Admin dapat menambahkan toko dan makanan yang tersedia di toko tersebut.                                                             |

### 6. URL _deployment_ PWS

http://daffa-abhipraya-ngandung.pbp.cs.ui.ac.id/
