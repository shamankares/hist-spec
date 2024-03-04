# API

HTTP POST /process

### _Request Body_

Untuk mengirimkan _request_, Anda harus memakai `multipart/form-data` sebagai isi header `Content-Type`.

| Nama           | Tipe                  | Keterangan |
| -------------- | --------------------- | ---------- |
| `inputImage`   | `file`                | Gambar yang ingin diolah. Gambar ini akan dicocokkan histogramnya dengan gambar referensi. Ukuran gambar harus kurang dari 2MB. |
| `desiredImage` | `file`                | Gambar referensi untuk pengolahan. Histogram gambar ini menjadi acuan gambar masukkan. Ukuran gambar harus kurang dari 2MB. |

### _JSON Response_

Catatan: _Response_ ini akan dikembalikan jika pengolahan tidak sukses.

| Nama         | Keterangan |
| ------------ | ---------- |
| `statusCode` | Kode _response_. |
| `status`     | Status _response_. |
| `message`    | Pesan _response_. |

#### _Success_ 200

Data yang dikembalikan adalah gambar bertipe `image/png`.

#### _Error_ 4xx

| Kode _Error_       | Keterangan |
| ------------------ | ---------- |
| `400`              | Dikembalikan jika _payload_ tidak mengandung properti yang dibutuhkan, tipe properti tidak benar, atau _file_ bukan berupa _file_ gambar. |
| `413`              | Dikembalikan jika ukuran gambar lebih dari 2MB. |
