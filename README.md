# 🌐 Platform Web Terintegrasi Panonpoe.id

Sebuah ekosistem aplikasi web berbasis Python (Flask) yang dikembangkan khusus untuk mendukung berbagai lini operasional bisnis PT. Panonpoe. Proyek ini menggunakan arsitektur multi-modul untuk memisahkan logika bisnis dari masing-masing subdomain agar sistem lebih terukur (*scalable*) dan mudah dipelihara.

## 🚀 Modul & Subdomain Utama

Sistem ini memayungi tiga layanan utama:

1. 📚 **Publisher (publisher.panonpoe.id)**
   * Sistem manajemen dan etalase digital yang dikhususkan untuk mempublikasikan buku-buku terbitan perusahaan.
   
2. 🛍️ **Katalog Produk (produk.panonpoe.id)**
   * Halaman dinamis untuk menampilkan dan memasarkan produk-produk komersial yang diproduksi oleh PT. Panonpoe.
   
3. 📰 **Jurnal Digital (jurnal.panonpoe.id)**
   * Modul masa depan yang dirancang untuk mewadahi publikasi jurnal, artikel, atau karya tulis terstruktur lainnya.
   * 
4. 🔭 LabFalak Panonpoe (`labfalak.panonpoe.id`)
  Sebuah subsistem terintegrasi yang didedikasikan untuk perhitungan astronomi dan Ilmu Falak. Fitur ini dirancang dengan pendekatan *native* tanpa ketergantungan pada pihak ketiga.
  
  * **Kalkulasi Ephemeris Mandiri:** Melakukan perhitungan presisi untuk posisi matahari, posisi bulan, dan visibilitas (rukyat) hilal.
  * **Algoritma Jean Meeus:** Mengimplementasikan rumus astronomi kompleks dari Jean Meeus secara manual dan *native* ke dalam sistem.
  * **100% Bebas API Pihak Ketiga:** Tidak menggunakan API eksternal atau *library* tambahan, sehingga sistem sepenuhnya mandiri, lebih cepat, dan kebal terhadap *downtime* dari layanan luar.
  * **Akurasi & Kontrol Penuh:** Memberikan kendali mutlak pada setiap fraksi derajat perhitungan yang sangat krusial dalam penentuan waktu astronomis.
    
## 🛠️ Teknologi yang Digunakan
* **Backend Framework:** Python (Flask)
* **Frontend:** HTML, CSS, dan integrasi *template engine*
* **Arsitektur:** Monorepo dengan pembagian direktori per modul layanan (`/PUBLISHER`, `/PRODUK`, `/DASHBOARD`)

## 👨‍💻 Kolaborasi & Manajemen Proyek
Proyek ini dikembangkan secara kolaboratif dalam tim menggunakan Git *version control* untuk memastikan setiap perubahan fitur atau *template* produk dapat dilacak dengan baik.

> **Catatan:** Repositori ini bersifat privat (*closed-source*) untuk melindungi aset bisnis, desain *database*, dan logika operasional PT. Panonpoe. 

---
*Maintained by: Tim Developer PT. Panonpoe*
