# Используем базовый образ Python
FROM python:3.12

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем requirements.txt из ComicsLibrary
COPY ComicsLibrary/requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt
RUN apt-get update && apt-get install -y tree


# Копируем остальные файлы
COPY ComicsLibrary /app/ComicsLibrary
COPY ComicsLibrary/main.py /app/

# Указываем PYTHONPATH
ENV PYTHONPATH=/app

# Открываем порт
EXPOSE 8000

CMD tree /app && python main.py