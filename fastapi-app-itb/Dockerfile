# Gunakan image python yang ringan
FROM python:3.11-slim

# Buat workdir di dalam container
WORKDIR /app

# Copy semua file dari project lokal ke container
COPY . .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 17787 (port internal container)
EXPOSE 17787

# Jalankan uvicorn di port 17787
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "17787"]
