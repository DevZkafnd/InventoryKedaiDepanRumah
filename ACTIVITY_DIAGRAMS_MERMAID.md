# Activity Diagram Mermaid

Dokumen ini berisi activity diagram versi Mermaid yang dibuat lebih dekat ke standar UML Activity Diagram untuk kebutuhan skripsi mahasiswa.

Catatan penting:
- Mermaid tidak mendukung notasi UML Activity secara 100% penuh seperti tool UML khusus.
- Untuk mendekati standar UML, diagram di bawah memakai:
  - `subgraph` sebagai swimlane/partisi aktor
  - node berbentuk rounded/stadium untuk action
  - diamond untuk decision dan merge
  - node awal dan akhir yang distyling menyerupai initial/final node
- Alur sudah disesuaikan dengan implementasi project saat ini, bukan fitur di luar cakupan skripsi.

Prinsip sistem:
- Owner hanya read-only pengawasan.
- Manajer memegang fungsi operasional penuh.
- Kasir hanya mengakses stok toko dan transfer request.
- Kelola akun pengguna tidak dimasukkan sebagai use case operasional.
- Django Admin tidak dimasukkan ke activity diagram utama karena dianggap alat konfigurasi/deployment.

## 1. Activity Diagram Utama Sistem

```mermaid
flowchart LR
    classDef initial fill:#000,stroke:#000,color:#000;
    classDef final fill:#fff,stroke:#000,stroke-width:4px,color:#fff;

    start(( )):::initial
    finish(( )):::final

    subgraph L1["Pengguna"]
        U1([Membuka aplikasi web])
        U2([Menekan tombol Login])
        U3([Mengisi username dan password])
        U4([Memilih menu sesuai role])
        U5([Logout])
    end

    subgraph L2["Sistem Web Inventory"]
        S1([Menampilkan landing page])
        S2([Menampilkan form login])
        S3([Memvalidasi kredensial])
        D1{Login valid?}
        S4([Menampilkan pesan gagal login])
        S5([Mengidentifikasi role pengguna])
        D2{Role pengguna?}
        S6([Redirect ke Dashboard])
        S7([Redirect ke Stok Toko])
        D3{Menu Owner?}
        D4{Menu Manajer?}
        D5{Menu Kasir?}
        M1{ }
        M2{ }
        M3{ }
    end

    subgraph L3["Database"]
        DB1([Mengambil data dashboard, laporan, waste, transfer, atau stok toko])
        DB2([Menyimpan perubahan operasional manajer])
        DB3([Menyimpan draft atau submit transfer kasir])
    end

    subgraph L4["Layanan AI"]
        AI1([Memproses pertanyaan AI])
    end

    start --> U1 --> S1 --> U2 --> S2 --> U3 --> S3 --> D1
    D1 -- Tidak --> S4 --> S2
    D1 -- Ya --> S5 --> D2

    D2 -- Owner --> S6 --> U4 --> D3
    D3 -- Dashboard --> DB1 --> M1
    D3 -- Laporan --> DB1 --> M1
    D3 -- Riwayat Waste --> DB1 --> M1
    D3 -- Status Transfer --> DB1 --> M1
    D3 -- AI Assistant --> AI1 --> M1
    M1 --> U5 --> finish

    D2 -- Manajer --> S6 --> U4 --> D4
    D4 -- Kelola Stok Gudang --> DB2 --> M2
    D4 -- Kelola Waste --> DB2 --> M2
    D4 -- Kelola Transfer --> DB2 --> M2
    D4 -- Import atau Export Excel --> DB2 --> M2
    D4 -- Maintenance Mode --> DB2 --> M2
    D4 -- Laporan --> DB1 --> M2
    D4 -- AI Assistant --> AI1 --> M2
    M2 --> U5 --> finish

    D2 -- Kasir --> S7 --> U4 --> D5
    D5 -- Lihat Stok Toko --> DB1 --> M3
    D5 -- Buat Draft Transfer --> DB3 --> M3
    D5 -- Submit Request Transfer --> DB3 --> M3
    M3 --> U5 --> finish
```

## 2. Activity Diagram Login dan RBAC

```mermaid
flowchart LR
    classDef initial fill:#000,stroke:#000,color:#000;
    classDef final fill:#fff,stroke:#000,stroke-width:4px,color:#fff;

    start(( )):::initial
    finish(( )):::final

    subgraph A1["Pengguna"]
        U1([Membuka halaman login])
        U2([Mengisi username dan password])
    end

    subgraph A2["Sistem"]
        S1([Memvalidasi akun])
        D1{Kredensial valid?}
        S2([Menampilkan pesan login gagal])
        D2{Melebihi batas percobaan?}
        S3([Mengaktifkan lockout sementara dengan Django Axes])
        S4([Membaca role pengguna])
        D3{Role pengguna?}
        S5([Redirect ke Dashboard])
        S6([Redirect ke Stok Toko])
    end

    start --> U1 --> U2 --> S1 --> D1
    D1 -- Tidak --> S2 --> D2
    D2 -- Ya --> S3 --> finish
    D2 -- Tidak --> U1
    D1 -- Ya --> S4 --> D3
    D3 -- Owner --> S5 --> finish
    D3 -- Manajer --> S5 --> finish
    D3 -- Kasir --> S6 --> finish
```

## 3. Activity Diagram Kelola Stok Gudang

```mermaid
flowchart LR
    classDef initial fill:#000,stroke:#000,color:#000;
    classDef final fill:#fff,stroke:#000,stroke-width:4px,color:#fff;

    start(( )):::initial
    finish(( )):::final

    subgraph B1["Manajer"]
        U1([Membuka halaman stok gudang])
        U2([Memilih aksi tambah, ubah, atau hapus item])
        U3([Mengisi atau mengubah data item])
        U4([Memilih item yang akan dihapus])
    end

    subgraph B2["Sistem"]
        S1([Mengambil data item])
        S2([Menampilkan tabel stok gudang])
        D1{Aksi yang dipilih?}
        S3([Memvalidasi input item])
        D2{Input valid?}
        S4([Menampilkan pesan error])
        M1{ }
        S5([Melakukan soft delete item])
        S6([Menampilkan notifikasi berhasil])
    end

    subgraph B3["Database"]
        DB1([Membaca data item])
        DB2([Menyimpan item baru])
        DB3([Memperbarui item beserta expiry date])
        DB4([Mengubah status item menjadi nonaktif])
    end

    start --> U1 --> S1 --> DB1 --> S2 --> U2 --> D1
    D1 -- Tambah --> U3 --> S3 --> D2
    D1 -- Ubah --> U3 --> S3 --> D2
    D1 -- Hapus --> U4 --> S5 --> DB4 --> S6 --> finish
    D2 -- Tidak --> S4 --> U3
    D2 -- Ya, Tambah --> DB2 --> M1
    D2 -- Ya, Ubah --> DB3 --> M1
    M1 --> S6 --> finish
```

## 4. Activity Diagram Waste Management

```mermaid
flowchart LR
    classDef initial fill:#000,stroke:#000,color:#000;
    classDef final fill:#fff,stroke:#000,stroke-width:4px,color:#fff;

    start(( )):::initial
    finish(( )):::final

    subgraph C1["Manajer"]
        U1([Membuka halaman Waste Management])
        U2([Memilih item, sumber, qty, alasan, dan tanggal])
    end

    subgraph C2["Sistem"]
        S1([Menampilkan form waste dan riwayat waste])
        S2([Memvalidasi data waste])
        D1{Data valid?}
        S3([Menampilkan pesan error])
        S4([Memuat ulang riwayat waste])
        S5([Menampilkan notifikasi berhasil])
    end

    subgraph C3["Database"]
        DB1([Membaca data waste sebelumnya])
        DB2([Menyimpan catatan waste baru])
    end

    start --> U1 --> S1 --> DB1 --> U2 --> S2 --> D1
    D1 -- Tidak --> S3 --> U2
    D1 -- Ya --> DB2 --> S4 --> S5 --> finish
```

## 5. Activity Diagram Transfer Barang

```mermaid
flowchart LR
    classDef initial fill:#000,stroke:#000,color:#000;
    classDef final fill:#fff,stroke:#000,stroke-width:4px,color:#fff;

    start(( )):::initial
    finish(( )):::final

    subgraph D1["Kasir"]
        K1([Membuka halaman transfer])
        K2([Memilih SKU dan jumlah])
        K3([Menekan tombol Tambah])
        K4([Menekan tombol Submit])
    end

    subgraph D2["Sistem"]
        S1([Menampilkan katalog barang transfer])
        S2([Memvalidasi input transfer])
        D3{Input valid?}
        S3([Menampilkan pesan error])
        S4([Memeriksa maintenance mode])
        D4{Maintenance aktif?}
        S5([Menampilkan request menunggu verifikasi])
        S6([Menolak transfer sementara])
        S7([Menampilkan daftar transfer ordered])
        D5{Keputusan manajer}
        S8([Memvalidasi ketersediaan stok gudang])
        D6{Stok cukup?}
        S9([Menampilkan gagal approve])
        S10([Menampilkan transfer berhasil])
        S11([Menampilkan transfer dibatalkan])
    end

    subgraph D3["Database"]
        DB1([Menyimpan draft transfer Ordered = NO])
        DB2([Mengubah draft menjadi Ordered = YES])
        DB3([Mengurangi stok gudang])
        DB4([Menambah stok toko])
        DB5([Menyelesaikan atau menghapus data transfer])
    end

    subgraph D4["Manajer"]
        MGR1([Membuka daftar transfer])
        MGR2([Memilih approve atau cancel])
    end

    start --> K1 --> S1 --> K2 --> K3 --> S2 --> D3
    D3 -- Tidak --> S3 --> K2
    D3 -- Ya --> DB1 --> K4 --> S4 --> D4
    D4 -- Ya --> S6 --> finish
    D4 -- Tidak --> DB2 --> S5 --> MGR1 --> S7 --> MGR2 --> D5
    D5 -- Approve --> S8 --> D6
    D6 -- Tidak --> S9 --> finish
    D6 -- Ya --> DB3 --> DB4 --> DB5 --> S10 --> finish
    D5 -- Cancel --> DB5 --> S11 --> finish
```

## 6. Activity Diagram AI Assistant

```mermaid
flowchart LR
    classDef initial fill:#000,stroke:#000,color:#000;
    classDef final fill:#fff,stroke:#000,stroke-width:4px,color:#fff;

    start(( )):::initial
    finish(( )):::final

    subgraph E1["Owner / Manajer"]
        U1([Membuka halaman AI Assistant])
        U2([Mengetik pertanyaan atau meminta insight])
    end

    subgraph E2["Sistem"]
        S1([Memeriksa role pengguna])
        D1{Role diizinkan?}
        S2([Menampilkan permission denied])
        S3([Memeriksa kuota per jam])
        D2{Kuota tersedia?}
        S4([Menampilkan Rate Limit Exceeded])
        S5([Mengirim permintaan ke layanan AI])
        S6([Menerima jawaban AI])
        S7([Menampilkan jawaban atau insight])
    end

    subgraph E3["Layanan AI"]
        AI1([Memproses pertanyaan inventory])
    end

    start --> U1 --> U2 --> S1 --> D1
    D1 -- Tidak --> S2 --> finish
    D1 -- Ya --> S3 --> D2
    D2 -- Tidak --> S4 --> finish
    D2 -- Ya --> S5 --> AI1 --> S6 --> S7 --> finish
```

## 7. Activity Diagram Import Excel

```mermaid
flowchart LR
    classDef initial fill:#000,stroke:#000,color:#000;
    classDef final fill:#fff,stroke:#000,stroke-width:4px,color:#fff;

    start(( )):::initial
    finish(( )):::final

    subgraph F1["Manajer"]
        U1([Membuka fitur import data])
        U2([Memilih file Excel])
    end

    subgraph F2["Sistem"]
        S1([Memvalidasi tipe file dan struktur sheet])
        D1{Format valid?}
        S2([Menampilkan pesan gagal upload])
        S3([Membaca sheet Warehouse Stock])
        S4([Memetakan kolom ke field item])
        S5([Memvalidasi isi data])
        D2{Data dapat diproses?}
        S6([Menampilkan pesan gagal import])
        S7([Menampilkan hasil import])
    end

    subgraph F3["Database"]
        DB1([Menambah atau memperbarui data item])
    end

    start --> U1 --> U2 --> S1 --> D1
    D1 -- Tidak --> S2 --> finish
    D1 -- Ya --> S3 --> S4 --> S5 --> D2
    D2 -- Tidak --> S6 --> finish
    D2 -- Ya --> DB1 --> S7 --> finish
```

## 8. Activity Diagram Maintenance Mode

```mermaid
flowchart LR
    classDef initial fill:#000,stroke:#000,color:#000;
    classDef final fill:#fff,stroke:#000,stroke-width:4px,color:#fff;

    start(( )):::initial
    finish(( )):::final

    subgraph G1["Manajer"]
        U1([Membuka konfigurasi aplikasi])
        U2([Memilih aktifkan atau nonaktifkan maintenance mode])
    end

    subgraph G2["Sistem"]
        D1{Aksi yang dipilih}
        S1([Menampilkan status maintenance aktif])
        S2([Menampilkan status maintenance nonaktif])
        S3([Memeriksa status maintenance saat kasir submit transfer])
        D2{Maintenance aktif?}
        S4([Menolak transfer])
        S5([Mengizinkan proses transfer])
    end

    subgraph G3["Database"]
        DB1([Menyimpan edit_lock = true])
        DB2([Menyimpan edit_lock = false])
    end

    subgraph G4["Kasir"]
        K1([Mencoba submit transfer])
    end

    start --> U1 --> U2 --> D1
    D1 -- Aktifkan --> DB1 --> S1 --> K1 --> S3 --> D2
    D1 -- Nonaktifkan --> DB2 --> S2 --> K1 --> S3 --> D2
    D2 -- Ya --> S4 --> finish
    D2 -- Tidak --> S5 --> finish
```

## Catatan Penggunaan

- Untuk BAB III skripsi, diagram yang paling aman dipakai:
  - Diagram utama sistem
  - Diagram login dan RBAC
  - Diagram stok gudang
  - Diagram waste management
  - Diagram transfer
  - Diagram AI Assistant
- Diagram import Excel dan maintenance mode bisa dipakai sebagai diagram tambahan untuk menegaskan fitur wajib pada pengujian sistem.
- Jika rekanmu ingin hasil yang lebih “UML murni”, diagram ini sebaiknya dijadikan acuan alur lalu digambar ulang di draw.io, StarUML, atau Visual Paradigm dengan simbol UML Activity bawaan.
