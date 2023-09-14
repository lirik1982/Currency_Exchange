# образ на основе которого создаём контейнер
FROM python:3.11-slim

# рабочая директория внутри проекта
WORKDIR /app

# переменные окружения для python
# Переменная окружения 'PYTHONDONTWRITEBYTECODE' - Python не будет создавать файлы кэша .pyc
# 'PYTHONUNBUFFERED' - не помещает в буфер потоки stdout и stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# устанавливаем зависимости
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# копируем содержимое текущей папки в контейнер
COPY . .

