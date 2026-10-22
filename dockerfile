# Resmi Python imajını kullan
FROM python:3.10-slim

# Sistem paketlerini, g++ derleyicisini ve Docker istemcisini yüklüyoruz
RUN apt-get update && apt-get install -y g++ docker.io && rm -rf /var/lib/apt/lists/*

# Çalışma dizinini belirle
WORKDIR /app

# Gereksinimleri kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını içeri aktar
COPY . .

# Flask uygulamasının çalışacağı portu dış dünyaya açıyoruz
EXPOSE 5000

# Uygulamayı başlat
CMD ["python", "app.py"]