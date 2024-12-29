# Use uma imagem base leve do Python
FROM python:3.10-slim

# Configurar diretório de trabalho dentro do contêiner
WORKDIR /app

# Copiar o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código do aplicativo para o contêiner
COPY . .

# Expor a porta que o aplicativo usará
EXPOSE 8000

# Definir comando para executar o servidor em produção
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]