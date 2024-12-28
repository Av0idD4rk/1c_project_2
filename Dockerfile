# Используем официальный Python-базовый образ (Debian-based)
FROM python:3.12-slim

# Устанавливаем нужные системные пакеты, чтобы WeasyPrint могла рендерить PDF
# - libpango, libffi, libgdk-pixbuf, libcairo, libgobject
# - wkhtmltopdf (если бы использовали pdfkit) и т.д.
# Здесь же ставим необходимые шрифты, например fonts-dejavu
RUN apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libffi7 \
    libgdk-pixbuf2.0-0 \
    libgobject-2.0-0 \
    libcairo2 \
    libxml2 \
    libpng16-16 \
    libjpeg62-turbo \
    fonts-dejavu-core fonts-dejavu-extra \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем WeasyPrint и другие Python-зависимости
# (предположим, ваш requirements.txt уже содержит weasyprint==X.X, fastapi, sqlalchemy и т.д.)
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Предположим, точка входа - uvicorn (если FastAPI).
# Либо можно прописать CMD ["python", "app/main.py"] (Flask).
# Здесь пример для uvicorn:
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]