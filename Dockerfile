# Python o'rnatilgan bazaviy muhit
FROM python:3.9-slim

# Tizimni yangilash va FFmpeg o'rnatish (Eng muhim joyi)
RUN apt-get update && apt-get install -y ffmpeg

# Ishchi papkani yaratish
WORKDIR /app

# Kutubxonalarni o'rnatish
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Barcha kodlarni nusxalash
COPY . .

# Papkalarni yaratib qo'yish (xatolik bo'lmasligi uchun)
RUN mkdir -p outputs static

# Serverni ishga tushirish (Render portini eshitadi)
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]
