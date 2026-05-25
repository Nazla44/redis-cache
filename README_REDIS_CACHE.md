# Lab Redis Cache - Weather API

Tugas ini mengimplementasikan caching sederhana menggunakan Redis untuk menyimpan hasil API call.

## Alur Program

1. User memanggil `get_weather("Jakarta")`.
2. Program membuat cache key: `weather:jakarta`.
3. Program menjalankan Redis `GET weather:jakarta`.
4. Jika data ditemukan, data langsung dikembalikan dari cache.
5. Jika data tidak ditemukan, program melakukan API call lambat dengan simulasi `time.sleep(2)`.
6. Hasil API disimpan ke Redis memakai `SETEX weather:jakarta 300 <data>`.
7. Panggilan berikutnya sebelum 300 detik akan mengambil data dari Redis.

## Cara Menjalankan di Windows dengan Docker

Pastikan Docker Desktop sudah berjalan.

### 1. Masuk ke folder project

```bash
cd Lab-05-Starter
```

Jika folder project bernama lain, sesuaikan dengan lokasi hasil ekstrak ZIP.

### 2. Jalankan container

```bash
docker compose up -d --build
```

### 3. Cek apakah container sudah berjalan

```bash
docker compose ps
```

Harus ada service `app`, `database`, dan `redis`.

### 4. Jalankan testing cache

```bash
docker compose exec app python test_cache.py
```

Contoh hasil yang diharapkan:

```text
Cache kosong, melakukan API call...
Result 1: {'city': 'Jakarta', 'temperature': 30, 'condition': 'Sunny', 'source': 'dummy-api-fallback'}
First call: 2.12s
Data diambil dari cache Redis
Result 2: {'city': 'Jakarta', 'temperature': 30, 'condition': 'Sunny', 'source': 'dummy-api-fallback'}
Second call (cached): 0.00s
Cache TTL: 299 seconds
```

## Penjelasan Expire 5 Menit

Cache disimpan menggunakan perintah Redis `SETEX`:

```python
redis_client.setex(cache_key, 300, json.dumps(weather_data))
```

Artinya data disimpan selama 300 detik atau 5 menit. Setelah 5 menit, Redis otomatis menghapus cache. Ketika fungsi `get_weather()` dipanggil lagi setelah cache kedaluwarsa, fungsi akan melakukan API call ulang dan menyimpan cache baru.

## File yang Ditambahkan/Diubah

- `weather_api.py`
- `test_cache.py`
- `requirements.txt`
- `docker-compose.yml`
