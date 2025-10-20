FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHON_VERSION=3.8.18

# --- Базовые зависимости для сборки Python ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    libffi-dev \
    liblzma-dev \
    tk-dev \
    wget \
    make \
    ca-certificates \
    # --- Добавляем зависимости для OpenCV ---
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src

# --- Сборка Python 3.8 из исходников ---
RUN wget https://www.python.org/ftp/python/${PYTHON_VERSION}/Python-${PYTHON_VERSION}.tgz && \
    tar xvf Python-${PYTHON_VERSION}.tgz && \
    cd Python-${PYTHON_VERSION} && \
    ./configure --enable-optimizations && \
    make -j$(nproc) && \
    make altinstall && \
    cd /usr/src && \
    rm -rf Python-${PYTHON_VERSION} Python-${PYTHON_VERSION}.tgz

# --- Установка системных библиотек для проекта ---
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# --- Виртуальное окружение ---
RUN python3.8 -m venv /opt/venv38
ENV PATH="/opt/venv38/bin:$PATH"

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

ENV ENVIRONMENT=production

# --- Запуск приложения ---
CMD ["sh", "-c", "/opt/venv38/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 ${ENVIRONMENT:+--reload}"]
