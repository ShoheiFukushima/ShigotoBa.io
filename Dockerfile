# Multi-stage build for smaller image
FROM python:3.10-slim as builder

WORKDIR /app

# システムパッケージのインストール（build stage）
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Pythonパッケージのインストール
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.10-slim

WORKDIR /app

# Python packages from builder
COPY --from=builder /root/.local /root/.local

# システムパッケージ（runtime only）
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# PATH環境変数の更新
ENV PATH=/root/.local/bin:$PATH

# アプリケーションファイルのコピー
COPY . .

# Cloud Run用の環境変数
ENV PORT=8080
ENV STREAMLIT_SERVER_PORT=8080
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Streamlitの設定（最適化）
RUN mkdir -p ~/.streamlit && \
    echo '[general]\nemail = ""' > ~/.streamlit/credentials.toml && \
    echo '[server]\nport = 8080\nenableCORS = false\nenableXsrfProtection = false\nrunOnSave = false\n\n[browser]\ngatherUsageStats = false\n\n[client]\nshowSidebarNavigation = false\ntoolbarMode = "minimal"' > ~/.streamlit/config.toml

# ポートを公開
EXPOSE 8080

# ヘルスチェック
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:$PORT/_stcore/health || exit 1

# アプリケーション起動（最適化）
CMD streamlit run app.py \
    --server.port=$PORT \
    --server.address=0.0.0.0 \
    --server.runOnSave=false \
    --server.allowRunOnSave=false \
    --browser.gatherUsageStats=false