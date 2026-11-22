# Базовый образ Python
FROM python:3.14-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Копирование файла зависимостей
COPY requirements.txt .

# Установка библиотек
RUN pip install --no-cache-dir -r requirements.txt

# Копирование файлов проекта
COPY . .

# Порт приложения
EXPOSE 8501

# Запуск приложения Streamlit
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]