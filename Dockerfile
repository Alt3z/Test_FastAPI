FROM python:3.11-slim

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файлы проекта
COPY . /app

# Установите зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Укажите команду для запуска приложения
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
