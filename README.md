## Ngandung

### Table of contents

1. [Nama-nama Anggota Kelompok](#nama-nama-anggota-kelompok)
2. [Deskripsi aplikasi](#deskripsi-aplikasi)
3. [Daftar modul aplikasi](#daftar-modul-aplikasi)
4. [Sumber _intial_ dataset](#sumber-intial-dataset)
5. [_Role_ pengguna berdasarkan deskripsinya](#role-pengguna-berdasarkan-deskripsinya)
6. [URL _deployment_ PWS](#url-deployment-pws)

### Nama-nama Anggota Kelompok

-   Ahmad Dzulfikar As Shavy (2306152374) - `AhmadDzulfikar`
-   Muhammad Radhiya Arshq (2306275885) - `arshqiii`
-   Christian Raphael Heryanto (2306152323) - `papaChick`
-   Rayhan Syahdira Putra (2306275903) - `RayhanSP`
-   Daffa Abhipraya Putra (2306245131) - `absolutepraya`

### Deskripsi aplikasi

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec auctor, nunc nec askdbajdbas asjdbasjk jasdnakjsd ajkkjasndkj kjahd kjas kjasnd kjasnd asd

### Daftar modul aplikasi

#### a. Modul wajib:

-   _**Authentication**_ and _**Authorization**_  
    Modul ini berfungsi untuk mengatur _authentication_ pengguna. Pengguna dapat mendaftar, masuk, dan keluar dari aplikasi.

#### b. Modul/fitur aplikasi:

-   **Daftar Makanan Rekomendasi**  
    Modul ini berfungsi untuk menampilkan daftar makanan yang tersedia. Pengguna dapat melihat informasi makanan yang diinginkan.

    | Role  | Permission                                                                                                                           |
    | ----- | ------------------------------------------------------------------------------------------------------------------------------------ |
    | User  | Pengguna dapat mengakses informasi makanan yang tersedia di aplikasi, tanpa dapat mengubah atau menghapusnya.                        |
    | Admin | Admin dapat mengakses informasi makanan yang tersedia di aplikasi, dan dapat menambahkan, mengubah, atau menghapus makanan tersebut. |

-   **_Rating_ & _Review_ Toko**  
    Modul ini berfungsi untuk memberikan _rating_ & _review_ ke toko yang tersedia.

    | Role  | Permission                                                                                                  |
    | ----- | ----------------------------------------------------------------------------------------------------------- |
    | User  | Pengguna dapat memberikan _rating_ dengan range 1-5 dan _review_ berupa teks singkat ke toko yang tersedia. |
    | Admin | Admin dapat melihat _rating_ dan _review_ dari toko yang tersedia.                                          |

-   **Toko Favorit**  
    Modul ini berfungsi untuk menyimpan toko yang disukai oleh pengguna.

    | Role  | Permission                                                                                       |
    | ----- | ------------------------------------------------------------------------------------------------ |
    | User  | Pengguna dapat menyimpan toko yang disukai ke "Toko Favorit" yang dimiliki setiap akun pengguna. |
    | Admin | Admin tidak dapat menyimpan toko yang disukai ke "Toko Favorit".                                 |

-   **Pencarian Makanan**  
    Modul ini berfungsi untuk mencari makanan yang diinginkan oleh pengguna.

    | Role  | Permission                                                                       |
    | ----- | -------------------------------------------------------------------------------- |
    | User  | Pengguna dapat mencari makanan yang diinginkan di aplikasi melalui _search bar_. |
    | Admin | Admin dapat mencari makanan yang diinginkan di aplikasi melalui _search bar_.    |

-   **Tambah Toko & Makannya**
    Modul ini berfungsi untuk menambahkan toko dan makanan yang tersedia di toko tersebut.

    | Role  | Permission                                                                        |
    | ----- | --------------------------------------------------------------------------------- |
    | User  | Pengguna tidak dapat menambahkan toko dan makanan yang tersedia di toko tersebut. |
    | Admin | Admin dapat menambahkan toko dan makanan yang tersedia di toko tersebut.          |

### Sumber _intial_ dataset

TBA

### _Role_ pengguna berdasarkan deskripsinya

| Role  | Deskripsi                                                                                                                                                                                                                 |
| ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Admin | Admin adalah pengguna yang memiliki hak akses penuh terhadap aplikasi. Admin dapat menambahkan, menghapus, dan mengubah data yang ada di aplikasi.                                                                        |
| User  | User adalah pengguna yang memiliki hak akses terbatas terhadap aplikasi. User dapat melihat informasi makanan di toko yang tersedia, memberikan _rating_ ke toko tersebut, dan menyimpan toko tersebut ke "Toko Favorit". |

### URL _deployment_ PWS

TBA