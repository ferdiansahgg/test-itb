import base64
import pyotp
import secrets
import requests
from getpass import getpass

# === KONFIGURASI ===
USERNAME = "sister"
SHARED_SECRET = "ii2210_sister_"  # shared secret kamu, sama kayak yang di `users` dict
API_URL = "http://localhost:17787/motd"

# === INPUT MOTD DARI USER ===
motd = input("Masukkan pesan MOTD: ")

# === GENERATE OTP ===
# Encode ke base32 (wajib untuk TOTP)
key = base64.b32encode(SHARED_SECRET.encode()).decode()
totp = pyotp.TOTP(s=key, digest="SHA256", digits=8)
otp = totp.now()

# === REQUEST ke API ===
response = requests.post(
    API_URL,
    json={"motd": motd},
    auth=(USERNAME, otp),
)

# === HASIL ===
if response.status_code == 200:
    print("✅ MOTD berhasil dikirim!")
    print(response.json())
else:
    print("❌ Gagal kirim MOTD!")
    print("Status:", response.status_code)
    print("Detail:", response.text)
