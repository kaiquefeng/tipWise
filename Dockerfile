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
    && apt-get install -y --no-install-recommends gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Copiar o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do aplicativo para o contêiner
COPY . .

# Expor a porta que o aplicativo usará
EXPOSE 8080

# Configurar o script de inicialização
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Definir comando para executar o servidor em produção
CMD ["/start.sh"]