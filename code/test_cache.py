"""
test_cache.py

Script pengujian caching Redis.

Ekspektasi:
- First call  : lambat, kurang lebih 2 detik karena cache belum ada.
- Second call : cepat, biasanya < 0.1 detik karena data diambil dari Redis.
- TTL         : menunjukkan sisa waktu cache, maksimal 300 detik.
"""

import time

from weather_api import redis_client, get_weather


CITY = "Jakarta"
CACHE_KEY = f"weather:{CITY.lower()}"


# Bersihkan cache lama agar pengujian first call benar-benar lambat.
redis_client.delete(CACHE_KEY)


# First call - should be slow (around 2 seconds)
start = time.time()
result1 = get_weather(CITY)
time1 = time.time() - start
print("Result 1:", result1)
print(f"First call: {time1:.2f}s")


# Second call - should be fast (< 0.1 second)
start = time.time()
result2 = get_weather(CITY)
time2 = time.time() - start
print("Result 2:", result2)
print(f"Second call (cached): {time2:.2f}s")


# Cek expire cache
ttl = redis_client.ttl(CACHE_KEY)
print(f"Cache TTL: {ttl} seconds")


# Third call after 5 minutes - should be slow again
# Untuk tugas ini tidak perlu benar-benar menunggu 5 menit.
# Penjelasan:
# Redis menyimpan cache menggunakan SETEX selama 300 detik.
# Setelah TTL habis, key weather:jakarta otomatis dihapus oleh Redis.
# Jika get_weather('Jakarta') dipanggil lagi setelah TTL habis,
# program akan melakukan API call lagi sehingga waktunya kembali ±2 detik.
