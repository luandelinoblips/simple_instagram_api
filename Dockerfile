# Etapa 1: Build com base Alpine
FROM python:3.10-alpine as builder

# Definindo diretório de trabalho
WORKDIR /app

# Atualizando o pip e instalando dependências essenciais
RUN apk update && apk add --no-cache \
    build-base \
    libffi-dev \
    openssl-dev \
    git \
    python3-dev \
    musl-dev && \
    pip install --upgrade pip

# Instalando as dependências do FastAPI, Requests e Uvicorn diretamente via pip
RUN pip install --no-cache-dir --timeout=300 --retries=5 fastapi[standard] requests uvicorn instaloader

# Copiando o código da aplicação para a imagem de build
COPY ./app ./app

# Etapa 2: Imagem Final com Alpine
FROM python:3.10-alpine

# Diretório de trabalho
WORKDIR /app

# Instalando dependências mínimas de runtime
RUN apk add --no-cache \
    libffi \
    openssl \
    && rm -rf /var/cache/apk/*

# Copiando dependências da etapa de build
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin/uvicorn /usr/local/bin/uvicorn

# Copiando o código da aplicação
COPY ./app ./app

# Expondo a porta do servidor
EXPOSE 8000

# Comando para inicializar o servidor FastAPI com Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
