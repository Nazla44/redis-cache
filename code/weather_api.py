"""
weather_api.py

Implementasi caching sederhana menggunakan Redis untuk menyimpan hasil API call.

Alur:
1. Cek cache Redis terlebih dahulu berdasarkan nama kota.
2. Jika cache ada, data langsung dikembalikan dari Redis sehingga cepat.
3. Jika cache tidak ada, lakukan API call yang disimulasikan lambat selama 2 detik.
4. Simpan hasil API call ke Redis dengan expire 300 detik atau 5 menit.
"""

import json
import os
import time
from typing import Any, Dict

import redis
import requests


# Konfigurasi Redis.
# Saat dijalankan memakai Docker Compose, REDIS_HOST akan bernilai "redis".
# Saat dijalankan langsung di Windows, default-nya "localhost".
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
CACHE_EXPIRE_SECONDS = 300  # 5 menit


redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=0,
    decode_responses=True,  # supaya data string JSON langsung terbaca sebagai str
)


def _call_weather_api(city: str) -> Dict[str, Any]:
    """
    Fungsi ini mensimulasikan API call yang lambat.

    time.sleep(2) digunakan sesuai skenario tugas agar panggilan pertama
    terasa lambat, sedangkan panggilan kedua cepat karena mengambil cache.

    Catatan:
    URL https://api.example.com/weather/... hanya contoh. Jika endpoint tidak
    bisa diakses, fungsi tetap mengembalikan data dummy agar testing cache tetap
    dapat berjalan.
    """
    time.sleep(2)

    url = f"https://api.example.com/weather/{city}"

    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        # Fallback agar tugas tetap bisa dites tanpa koneksi API asli.
        return {
            "city": city,
            "temperature": 30,
            "condition": "Sunny",
            "source": "dummy-api-fallback",
        }


def get_weather(city: str) -> Dict[str, Any]:
    """
    Mengambil data cuaca berdasarkan kota dengan caching Redis.

    Redis command yang digunakan:
    - GET   : mengecek data cache
    - SETEX : menyimpan cache beserta waktu kedaluwarsa/expire
    """
    city = city.strip()
    cache_key = f"weather:{city.lower()}"

    # 1. Cek cache terlebih dahulu.
    cached_weather = redis_client.get(cache_key)

    if cached_weather is not None:
        print("Data diambil dari cache Redis")
        return json.loads(cached_weather)

    # 2. Jika cache kosong, panggil API.
    print("Cache kosong, melakukan API call...")
    weather_data = _call_weather_api(city)

    # 3. Simpan hasil API ke Redis selama 300 detik.
    redis_client.setex(
        cache_key,
        CACHE_EXPIRE_SECONDS,
        json.dumps(weather_data),
    )

    return weather_data


if __name__ == "__main__":
    print(get_weather("Jakarta"))
