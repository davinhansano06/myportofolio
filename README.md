Nama : Davin Tristan Hansano
NPM : 2506620513
Kelas : PBP C

## Tugas 1
1. **Penggunaan Elemen Semantik HTML5**
    Ya, saya memanfaatkan elemen semantik HTML5 seperti <section>, <header>, <nav>, dan <footer> dalam membuat tugas ini. Elemen-elemen ini  membantu saya dalam memetakan blok informasi utama seperti memisahkan area Hero/Profile, Skill, hingga Education jadi part yang lebih  rapi. Dalam konteks static web, penggunaan tag semantik ini tidak hanya membuat struktur kode HTML jauh lebih mudah dibaca dan di maintain, tetapi juga memudahkan penataan CSS karena saya bisa langsung menerapkan secara umum (seperti pengaturan scroll-margin-top pada setiap <section>) tanpa harus mengandalkan tumpukan <div> dengan nama kelas yang kadang membuat bingung.

2. **Tantangan Responsive CSS & Evaluasi Tampilan Mobile**
    Tantangan terbesar yang saya hadapi adalah mengelola tampilan pada layar kecil, terutama pada komponen sticky header dan grid layout. Di tampilan desktop, tata letak dua kolom dan header yang lebar memberi kesan luas. Tapi saat berpindah ke layar mobile, header sempat memakan terlalu banyak ruang vertikal dan beberapa elemen grid bertabrakan karena lebar kontainer yang terbatas.

    Saya mengevaluasi prioritas berdasarkan user experience membaca: informasi paling vital (seperti nama, role, dan isi utama riwayat pendidikan) harus tetap di atas tanpa perlu scrolling. Elemen yang sebelumnya berjajar secara horizontal saya sesuaikan jadi vertikal stack, sementara ukuran padding, font size, serta jarak antar menu dimampatkan biar enggak mendominasi layar hp.

3. **Batasan Static Web & Rencana Fungsionalitas Dinamis**
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

### Tugas 3

1. **Jelaskan mengapa kita menggunakan ModelForm pada Django alih-alih membuat form HTML secara manual. Selain itu, jelaskan pula mengapa kita diwajibkan menambahkan `{% csrf_token %}` pada form tersebut!**

   Saya menggunakan ModelForm karena lebih praktis dibandingkan membuat form HTML dari awal. ModelForm dapat menyesuaikan field yang ada di model sehingga saya tidak perlu membuat setiap input dan proses validasinya secara manual. Setelah data diisi dengan benar, data juga bisa langsung disimpan ke database menggunakan `form.save()`.

   `{% csrf_token %}` digunakan untuk keamanan pada form Django. Token ini membantu memastikan bahwa request yang dikirim memang berasal dari website kita dan bukan request palsu dari website lain. Hal ini penting terutama untuk form yang digunakan untuk menambahkan atau mengubah data.

2. **Pada Tutorial 03, kita membahas format data JSON dan XML. Mengapa JSON lebih disukai dalam pengembangan aplikasi web modern dibandingkan XML?**

   Menurut saya, JSON lebih banyak digunakan karena bentuk datanya lebih sederhana dan lebih ringkas dibandingkan XML. JSON menggunakan format seperti key-value dan array sehingga lebih mudah dibaca dan diproses.

   JSON juga cocok digunakan untuk komunikasi antara frontend dan backend. Selain itu, JSON dapat langsung digunakan dengan JavaScript sehingga penggunaannya cukup praktis dalam pengembangan website. Dibandingkan JSON, XML biasanya membutuhkan lebih banyak tag sehingga penulisannya bisa menjadi lebih panjang.

3. **Jelaskan alur yang terjadi saat kamu menggunakan fungsi view untuk mengembalikan data portofoliomu dalam bentuk JSON. Mengapa kita perlu melakukan proses serialization pada model Django sebelum datanya dikembalikan?**

   Pada project saya, data Education dan Experience disimpan di database menggunakan model Django. Ketika ingin mengambil data dalam bentuk JSON, view terlebih dahulu mengambil data tersebut menggunakan QuerySet.

   Alurnya kurang lebih adalah:

   `Database → Model/QuerySet → Serialization → JSON → Client`

   Contohnya pada `get_education_json`, data diambil menggunakan `Education.objects.all()`. Setelah itu data diubah menjadi JSON menggunakan `serializers.serialize("json", education)`. Hasilnya kemudian dikembalikan menggunakan `HttpResponse` dengan `content_type="application/json"`.

   Serialization diperlukan karena data yang diperoleh dari Django masih berupa object atau QuerySet, bukan data JSON yang bisa langsung dikirim melalui HTTP. Dengan serialization, data tersebut diubah menjadi format JSON sehingga dapat dikirim dan dibaca oleh client.

   Pada halaman Education, JSON yang sudah dibuat tersebut juga saya deserialize kembali menjadi object Django sebelum ditampilkan di halaman.


### Tugas 5

1. **Apa itu debouncing dan mengapa teknik ini penting diterapkan pada fitur pencarian yang menggunakan AJAX?**

   Debouncing adalah teknik untuk menunda eksekusi suatu fungsi sampai pengguna berhenti melakukan input selama waktu tertentu. Pada fitur pencarian menggunakan AJAX, debouncing penting agar request ke server tidak dikirim pada setiap karakter yang diketik pengguna. Dengan memberikan jeda, misalnya 300 milidetik, request hanya dikirim setelah pengguna berhenti mengetik. Hal ini dapat mengurangi jumlah request ke server dan membuat penggunaan resource menjadi lebih efisien.

2. **Apa fungsi penggunaan `await` ketika menggunakan `fetch()`? Apa yang akan terjadi jika tidak menggunakan `await`?**

   `await` digunakan untuk menunggu hasil dari operasi asynchronous seperti `fetch()` sebelum kode berikutnya dijalankan. Dengan menggunakan `await`, kita dapat memperoleh objek `Response` dari request terlebih dahulu dan kemudian memproses hasilnya, misalnya menggunakan `response.json()`. Jika tidak menggunakan `await`, `fetch()` akan langsung menghasilkan sebuah Promise sehingga kode berikutnya dapat berjalan sebelum response dari server tersedia. Akibatnya, kita perlu menangani Promise tersebut menggunakan cara asynchronous lainnya seperti `.then()`.

3. **Apa itu serangan XSS (Cross-Site Scripting) dan mengapa data yang ditampilkan melalui AJAX/JavaScript lebih rentan terhadap serangan ini daripada data yang ditampilkan langsung melalui template Django?**

   XSS (Cross-Site Scripting) adalah serangan ketika input atau data berbahaya disisipkan ke halaman web sehingga dapat dijalankan sebagai script di browser pengguna lain. Data yang ditampilkan melalui AJAX/JavaScript perlu mendapatkan perhatian khusus karena data dari server sering disisipkan secara dinamis ke dalam HTML menggunakan JavaScript. Jika nilai tersebut langsung dimasukkan menggunakan `innerHTML` tanpa escaping, HTML atau script berbahaya dapat ikut diinterpretasikan oleh browser. Oleh karena itu, pada implementasi ini digunakan `escapeHtml()` untuk melakukan escaping terhadap nilai teks sebelum dimasukkan ke HTML. Selain itu, input juga dibersihkan di sisi server menggunakan `strip_tags` melalui method `clean_<field>` pada ModelForm.

## Deklarasi Penggunaan AI

Saya menggunakan AI sebagai pendamping selama mengerjakan tugas ini, terutama untuk membantu memahami konsep Django MVT, mencari penyebab error, dan memberikan arahan ketika saya mengalami kesulitan. Saya tetap mengerjakan implementasi project secara langsung dan mempelajari setiap bagian yang digunakan, sehingga AI berperan sebagai alat bantu belajar, bukan sebagai pengganti 

### Tugas 6 — Refleksi Django REST Framework

1. **Apa yang dimaksud dengan REST dan mengapa mengembalikan JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful? Jelaskan perbedaan PUT dan PATCH!**

REST (Representational State Transfer) merupakan sebuah architectural style untuk membangun sistem komunikasi antara client dan server. REST menggunakan resource sebagai pusat interaksi, di mana setiap resource dapat diidentifikasi melalui URI dan dimanipulasi menggunakan HTTP methods seperti GET, POST, PUT, PATCH, dan DELETE.

Mengembalikan data dalam format JSON saja belum cukup untuk menyebut sebuah API sebagai RESTful. JSON hanyalah format pertukaran data, sedangkan REST berkaitan dengan bagaimana API dirancang dan bagaimana client berinteraksi dengan resource. API perlu memperhatikan prinsip-prinsip REST, seperti penggunaan resource-based URI, HTTP methods sesuai fungsinya, stateless communication, serta representasi resource yang konsisten.

Dalam project ini, Experience API menggunakan endpoint `/api/v1/experiences/` untuk mengakses kumpulan data Experience dan `/api/v1/experiences/<id>/` untuk mengakses satu Experience berdasarkan UUID-nya. Setiap HTTP method memiliki fungsi yang berbeda:
- **GET** digunakan untuk mengambil data Experience.
- **POST** digunakan untuk menambahkan Experience baru.
- **PUT** digunakan untuk memperbarui seluruh representasi resource dengan mengirimkan seluruh field yang diperlukan.
- **PATCH** digunakan untuk memperbarui sebagian field tanpa harus mengirimkan seluruh data.
- **DELETE** digunakan untuk menghapus Experience.

Perbedaan PUT dan PATCH terletak pada cakupan pembaruannya. PUT digunakan ketika client ingin mengganti representasi resource secara keseluruhan, sedangkan PATCH digunakan ketika hanya beberapa atribut yang perlu diubah. Contohnya, jika hanya ingin mengubah judul Experience, PATCH lebih tepat karena client cukup mengirimkan field `title`, sedangkan PUT memerlukan data lengkap sesuai field yang diwajibkan serializer.

2. **Apa peran serializer pada Django REST Framework? Apa keuntungannya dibandingkan merakit dictionary secara manual dengan JsonResponse seperti pada Tutorial 05?**

Serializer pada Django REST Framework berperan sebagai perantara antara model Django dengan representasi data yang dikirim atau diterima melalui API. Serializer mengubah instance model menjadi data primitif yang dapat dirender menjadi JSON, sekaligus memvalidasi data yang dikirim oleh client sebelum data tersebut disimpan ke database. Dalam project ini, `ExperienceSerializer` menggunakan `ModelSerializer` untuk menentukan field yang dapat diakses melalui API, seperti `id`, `title`, `institution`, `period`, `description`, dan `image`. Serializer juga menyediakan computed fields, yaitu `star_count` dan `is_starred`, untuk menampilkan jumlah star dan status star pengguna yang sedang login.

Dibandingkan membuat dictionary secara manual menggunakan `JsonResponse` seperti pada Tutorial 05, serializer memiliki beberapa keuntungan:
- **Mengurangi kode berulang:** pemetaan field model ke representasi API dapat dilakukan secara otomatis melalui `ModelSerializer`.
- **Validasi terstruktur:** validasi input dapat ditempatkan langsung di serializer melalui method seperti `validate_title()` dan `validate_description()`.
- **Penanganan error yang konsisten:** apabila input tidak valid, serializer menyediakan detail kesalahan yang dapat dikembalikan sebagai HTTP 400 Bad Request.
- **Read-only fields:** field seperti `id`, `star_count`, dan `is_starred` dapat ditentukan sebagai field yang tidak boleh diubah langsung oleh client.
- **Lebih mudah dikembangkan:** ketika model atau kebutuhan API berubah, pengelolaan representasi dan validasi data menjadi lebih terpusat.

Dengan demikian, serializer membuat kode API lebih modular, konsisten, dan mudah dipelihara dibandingkan merakit dictionary secara manual pada setiap endpoint.

3. **Apa perbedaan autentikasi dan otorisasi pada Django REST Framework? Mengapa hak akses harus diperiksa dengan permission class di server, bukan hanya dengan menyembunyikan tombol di template?**

Autentikasi (authentication) adalah proses untuk memverifikasi identitas pengguna yang mengakses aplikasi. Sementara itu, otorisasi (authorization) adalah proses untuk menentukan tindakan apa saja yang boleh dilakukan oleh pengguna setelah identitasnya diketahui.
Dalam project ini, autentikasi menggunakan `SessionAuthentication`, sehingga identitas pengguna dikenali melalui session login Django. Setelah itu, permission class `IsPortfolioOwnerOrEditorOrReadOnly` digunakan untuk menentukan hak akses terhadap Experience API.

Project ini memiliki empat jenis pengguna dengan hak akses berbeda:
- **Anonymous:** hanya dapat membaca data Experience.
- **Regular User:** dapat membaca data dan melakukan star/unstar.
- **Editor:** dapat membaca, melakukan star/unstar, serta memperbarui Experience menggunakan PUT atau PATCH.
- **Portfolio Owner (Superuser):** memiliki akses penuh untuk membaca, menambahkan, memperbarui, menghapus, dan melakukan star/unstar.

Pemeriksaan permission harus dilakukan di sisi server karena menyembunyikan tombol pada template hanya memengaruhi tampilan antarmuka, bukan keamanan endpoint. Pengguna tetap dapat mengirim HTTP request secara langsung menggunakan browser developer tools, Postman, atau program lain meskipun tombol tertentu tidak ditampilkan. Oleh karena itu, permission class diperlukan untuk memastikan setiap request diperiksa berdasarkan identitas dan hak akses pengguna. Dengan demikian, pengguna yang tidak memiliki izin tetap akan ditolak oleh server meskipun mencoba mengakses endpoint secara langsung.

4. **Mengapa permintaan yang mengubah data tetap memerlukan token CSRF ketika API memakai SessionAuthentication? Mengapa test yang memakai force_authenticate tidak cukup untuk membuktikan bahwa perlindungan CSRF berjalan?**

CSRF (Cross-Site Request Forgery) merupakan jenis serangan yang memanfaatkan autentikasi pengguna yang masih aktif di browser untuk mengirimkan request tanpa persetujuan pengguna. Pada Django, session authentication menggunakan cookie sebagai salah satu mekanisme pengenalan identitas pengguna. Browser dapat mengirimkan cookie tersebut secara otomatis ketika melakukan request ke server. Hal ini menimbulkan risiko apabila aplikasi tidak memeriksa apakah request yang mengubah data benar-benar berasal dari interaksi yang sah. Oleh karena itu, request yang mengubah state, seperti POST, PUT, PATCH, dan DELETE, perlu dilindungi menggunakan CSRF token.

Pada project ini, setiap request yang mengubah data melalui Experience API menyertakan header `X-CSRFToken` yang nilainya diperoleh dari cookie `csrftoken`. Django REST Framework melalui `SessionAuthentication` akan memeriksa token tersebut untuk request dari pengguna yang terautentikasi. Jika token tidak tersedia atau tidak valid, request akan ditolak. Pengujian menggunakan `force_authenticate()` saja tidak cukup untuk membuktikan perlindungan CSRF berjalan karena metode tersebut secara langsung menetapkan pengguna yang telah terautentikasi pada request test. Metode ini melewati proses autentikasi session yang sebenarnya, sehingga tidak menguji mekanisme CSRF sebagaimana yang terjadi pada browser.

Untuk membuktikan perlindungan CSRF berjalan, project ini menggunakan `APIClient(enforce_csrf_checks=True)` dan login melalui mekanisme session. Pengujian dilakukan dengan mengirimkan request POST tanpa CSRF token dan memastikan request ditolak. Selanjutnya, request dikirim kembali dengan CSRF token yang valid dan dipastikan berhasil. Dengan pengujian tersebut, perlindungan CSRF dapat diverifikasi melalui mekanisme session authentication yang sesungguhnya, bukan hanya melalui simulasi identitas pengguna.

## Deklarasi Penggunaan AI

Saya menggunakan AI sebagai pendamping selama mengerjakan tugas ini, terutama untuk membantu memahami konsep Django REST Framework, mencari penyebab error, dan memberikan arahan ketika saya mengalami kesulitan. Saya tetap mengerjakan implementasi project secara langsung dan mempelajari setiap bagian yang digunakan, sehingga AI berperan sebagai alat bantu belajar, bukan sebagai pengganti 