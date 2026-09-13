Nama : Davin Tristan Hansano
NPM : 2506620513
Kelas : PBP C

## Tugas 1
1. Penggunaan Elemen Semantik HTML5
Ya, saya memanfaatkan elemen semantik HTML5 seperti <section>, <header>, <nav>, dan <footer> dalam membuat tugas ini. Elemen-elemen ini  membantu saya dalam memetakan blok informasi utama seperti memisahkan area Hero/Profile, Skill, hingga Education jadi part yang lebih  rapi. Dalam konteks static web, penggunaan tag semantik ini tidak hanya membuat struktur kode HTML jauh lebih mudah dibaca dan di maintain, tetapi juga memudahkan penataan CSS karena saya bisa langsung menerapkan secara umum (seperti pengaturan scroll-margin-top pada setiap <section>) tanpa harus mengandalkan tumpukan <div> dengan nama kelas yang kadang membuat bingung.

2. Tantangan Responsive CSS & Evaluasi Tampilan Mobile
Tantangan terbesar yang saya hadapi adalah mengelola tampilan pada layar kecil, terutama pada komponen sticky header dan grid layout. Di tampilan desktop, tata letak dua kolom dan header yang lebar memberi kesan luas. Tapi saat berpindah ke layar mobile, header sempat memakan terlalu banyak ruang vertikal dan beberapa elemen grid bertabrakan karena lebar kontainer yang terbatas.
Saya mengevaluasi prioritas berdasarkan user experience membaca: informasi paling vital (seperti nama, role, dan isi utama riwayat pendidikan) harus tetap di atas tanpa perlu scrolling. Elemen yang sebelumnya berjajar secara horizontal saya sesuaikan jadi vertikal stack, sementara ukuran padding, font size, serta jarak antar menu dimampatkan biar enggak mendominasi layar hp.

3. Batasan Static Web & Rencana Fungsionalitas Dinamis
Saat membuat informasi pada static web, batasan utama yang paling saya rasakan adalah kurangnya interaktivitas langsung dengan user sehingga masih terikat hardcoded. Jika saya ingin memperbarui riwayat proyek, menambah sertifikasi baru, atau menerima pesan dari user, saya harus mengubah file HTML secara manual.Berdasarkan batasan tersebut, fungsionalitas dinamis yang paling ingin saya persiapkan pada iterasi selanjutnya adalah fitur form kontak dinamis, supaya pesan dari user portofolio dapat terkirim langsung ke email atau database saya.


## Deklarasi Penggunaan AI
Dalam proses pengerjaan Tutorial dan Tugas 1 ini, saya menggunakan bantuan AI Gemini sebagai tempat diskusi saya dan tempat saya mencari referensi teknis. AI saya gunakan untuk membantu memberikan ide variasi layout, mereferensikan penggunaan struktur HTML/CSS yang efisien, serta membantu melakukan analisis kendala saat terjadi bug pada respon tata letak responsive design dan membantu membuat comment yang rapi. 

Seluruh kode, penyesuaian posisi dan estetika (seperti skema warna), desain layout untuk riwayat pendidikan, penyesuaian media queries, serta logika penyusunan konten portofolio ini pada akhirnya saya eksekusi, kembangkan, dan pelajari secara mandiri sesuai dengan kreativitas dan kebutuhan desain portofolio saya. 

## Tugas 2

1. Alur yang saya gunakan dimulai dari URL yang mengarahkan request ke view yang sesuai. Pada project ini, ketika pengguna membuka halaman Education melalui `/education/`, URL tersebut didefinisikan di `main/urls.py` dan diarahkan ke fungsi `show_education` di `main/views.py`.
Selanjutnya, view mengambil data Education dari database menggunakan model `Education`. Data tersebut kemudian dimasukkan ke dalam context dan dikirim ke template `education.html`. Di dalam template, Django Template Language digunakan untuk melakukan perulangan terhadap data tersebut sehingga setiap data Education dapat ditampilkan di halaman.

Jadi secara sederhana, alurnya adalah:

`URL → View → Model/Database → Context → Template → Halaman Web`

2. Menurut saya, menggunakan model lebih baik karena data tidak tercampur dengan struktur tampilan HTML. Data Education dapat disimpan dan diubah melalui database tanpa harus mengubah kode HTML secara langsung. Selain itu, penggunaan model membuat website lebih mudah dikembangkan. Misalnya, jika saya ingin menambahkan riwayat pendidikan baru, saya cukup menambahkan data baru ke database. Template yang sama akan otomatis menampilkan data tersebut menggunakan perulangan. Kalau data ditulis langsung di HTML, setiap perubahan data mengharuskan saya mengubah kode template sehingga kurang fleksibel dan lebih sulit untuk dikelola.

3. `makemigrations` digunakan untuk membuat file migration berdasarkan perubahan yang dilakukan pada model. File tersebut berisi instruksi perubahan struktur database. Sedangkan `migrate` digunakan untuk benar-benar menerapkan migration tersebut ke database. Jadi, `makemigrations` membuat atau mencatat perubahan dari model, sedangkan `migrate` menjalankan perubahan tersebut pada database.

## Deklarasi Penggunaan AI

Saya menggunakan AI sebagai pendamping selama mengerjakan tugas ini, terutama untuk membantu memahami konsep Django MVT, mencari penyebab error, dan memberikan arahan ketika saya mengalami kesulitan. Saya tetap mengerjakan implementasi project secara langsung dan mempelajari setiap bagian yang digunakan, sehingga AI berperan sebagai alat bantu belajar, bukan sebagai pengganti pengerjaan tugas.