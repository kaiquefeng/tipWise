# Use uma imagem base leve do Python
FROM python:3.11-slim

# Configurar diretório de trabalho dentro do contêiner
WORKDIR /app

# Configurar variáveis de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=8080

# Instalar dependências do sistema
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        curl \
        build-essential \
        python3-dev \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Atualizar pip
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copiar o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do aplicativo para o contêiner
COPY . .

# Expor a porta que o aplicativo usará
EXPOSE 8080

# Configurar o script de inicialização
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Criar usuário não-root
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Definir comando para executar o servidor em produção
CMD ["/start.sh"]