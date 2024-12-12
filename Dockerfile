FROM python:3.11-slim

# Instalar wkhtmltopdf y sus dependencias
RUN apt-get update && \
    apt-get install -y wkhtmltopdf && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install -r requirements.txt

# Exponer el puerto
EXPOSE 10000

# Comando para ejecutar la aplicación
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:10000"]
