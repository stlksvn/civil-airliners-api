FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

WORKDIR /avia-api

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-install-project

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "main:app", "--app-dir", "app", "--host", "0.0.0.0", "--port", "8000"]
