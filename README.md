# 📦 FastAPI MOTD (Message of the Day) Project

## 📚 Deskripsi Singkat

Ini adalah aplikasi sederhana berbasis FastAPI yang menyimpan dan menampilkan pesan *Message of the Day (MOTD)* menggunakan SQLite sebagai database dan otentikasi menggunakan TOTP (Time-based One-Time Password).

---

## 🧰 Prasyarat

- OS: Linux (bisa jalan di Windows/Mac juga)
- Python 3.11
- Git
- Docker & Docker Compose

---

## 🐳 1. Instalasi Docker

### Ubuntu/Debian

```bash
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker
```

### Arch/CachyOS

```bash
sudo pacman -S docker docker-compose
sudo systemctl start docker
sudo systemctl enable docker
```

Pastikan user kamu tergabung dalam grup docker:

```bash
sudo usermod -aG docker $USER
```

Lalu re-login atau `newgrp docker` agar aktif.

---

## 📁 2. Struktur Proyek

```
fastapi-app-itb/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── model.py
├── static/
│   └── index.html
├── motd.db (otomatis terbuat)
├── requirements.txt
├── Dockerfile
├── top_secret.py
├── auto_post_motd.py
└── README.md
```

---

## 🧑‍💻 3. Penjelasan Kode

### `main.py`

- Menyediakan 3 endpoint:
  - `/`: menampilkan `index.html`
  - `/motd`: menampilkan pesan terakhir
  - `POST /motd`: menyimpan pesan, dengan autentikasi TOTP berbasis user

### `model.py`

```python
class MOTDBase(SQLModel):
    motd: str

class MOTD(MOTDBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    creator: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### `top_secret.py`

Men-generate OTP berdasarkan `shared_secret` untuk login:

```python
import pyotp
s = "ii2210_sister_"
totp = pyotp.TOTP(pyotp.random_base32(), digest="sha256", digits=8)
print("OTP sekarang:", totp.now())
```

### `auto_post_motd.py`

Script CLI untuk auto POST pesan dengan OTP tanpa ribet.

---

## 📦 4. Dockerfile

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 17787
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "17787"]
```

## 🐋 5. Build dan Jalankan Docker

```bash
docker build -t fastapi-motd .
docker run -d -p 17787:17787 --name motd fastapi-motd
```

Cek status:

```bash
docker ps
```

---

## 🔐 6. Deploy Key & Git

### Buat SSH Key

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
cat ~/.ssh/id_ed25519.pub
```

Copy ke GitHub (Repository > Settings > Deploy Keys)

### Inisialisasi Git

```bash
git init
git remote add origin git@github.com:username/repo.git
git add .
git commit -m "Initial commit"
git push -u origin main
```

---

## 🌐 7. Akses

- Web browser: [http://localhost:17787](http://localhost:17787)
- Endpoint:
  - `GET /motd`
  - `POST /motd` (butuh username dan OTP password)

---

## ✅ Tips Tambahan

- Untuk uji POST, bisa pakai:

```bash
curl -X POST http://localhost:17787/motd \
     -H "Content-Type: application/json" \
     -d '{"motd":"Hello from curl"}' \
     -u sister:12345678
```

- Gunakan `sqlite3 motd.db` untuk mengecek isi database.

---

## 📌 Credits

Project latihan pengembangan FastAPI untuk internal ITB, dengan fitur TOTP dan Docker.

Referensi

\- Docker

\- [https://docs.docker.com/engine/install/](https://docs.docker.com/engine/install/)

\- [https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-do](https://docs.docker.com/get-started/docker-concepts/building-images/writing-a-do)

ckerfile/

\- Git basics

\- [https://www.w3schools.com/git/](https://www.w3schools.com/git/)

\- Github deploy key

\- [https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managin](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/managin)

g-deploy-keys

\- FastAPI

\- [https://fastapi.tiangolo.com/learn/](https://fastapi.tiangolo.com/learn/)

\- [https://fastapi.tiangolo.com/deployment/docker/](https://fastapi.tiangolo.com/deployment/docker/)

\- [https://sqlmodel.tiangolo.com/learn/](https://sqlmodel.tiangolo.com/learn/)
