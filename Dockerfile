# Step 1: Install OS and Python

FROM python:3.12-slim

# Step 2: 

WORKDIR /app

# 3. Donwload and Install UV

# RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# # Install uv (script puts it in /root/.local/bin)
# RUN curl -LsSf https://astral.sh/uv/install.sh | sh && \
#     mv /root/.local/bin/uv /usr/local/bin/uv && \
#     mv /root/.local/bin/uvx /usr/local/bin/uvx

# 4. Copy

COPY . .

# 5. UV SYNC 

# RUN uv sync --frozen --no-dev

# 5. Install dependencies
RUN pip install -r requirements.txt

# 6. EXPOSE PORT

EXPOSE 8000

# 7. Run the Entry Point

CMD ["uv","run","uvicorn","src.main:app","--host","0.0.0.0","--port","8000"]



