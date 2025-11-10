FROM python:3.14-slim

WORKDIR /app

# 1️⃣ Instalar uv
RUN pip install --upgrade pip && pip install -U uv

# 2️⃣ Copiar dependencias y código fuente (todo lo necesario para compilar el paquete)
COPY pyproject.toml ./
COPY src ./src

# 3️⃣ Instalar dependencias (y tu paquete local)
RUN uv sync --dev

# 4️⃣ Copiar otros archivos opcionales (scripts, configs, etc.)
COPY . .

# 5️⃣ Comando por defecto
CMD ["uv", "run", "main"]