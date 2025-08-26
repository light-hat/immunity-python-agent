# syntax=docker/dockerfile:1
FROM python:3.12-slim AS build

# Опционально: ускорим и сделаем сборку чище
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app
# Сначала только метаданные — лучше кэшируются
COPY setup.cfg setup.py* ./
COPY README.md LICENSE ./
# Затем исходники
COPY immunity_agent_python ./immunity_agent_python

# Обновим инструменты сборки и соберём пакет
RUN python -m pip install --upgrade pip build \
 && python -m build

# Этап рантайма — чистый образ
FROM python:3.12-slim AS runtime
ENV PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
WORKDIR /app

# Устанавливаем собранный wheel
COPY --from=build /app/dist/*.whl /tmp/
RUN python -m pip install /tmp/*.whl \
 && rm -rf /tmp/*.whl

# Небольшой smoke-тест: импорт и версия
RUN python - <<'PY'
import sys
print("Python:", sys.version)
import immunity_agent_python as mod
try:
    from immunity_agent_python.version import __version__
    print("immunity_agent_python version:", __version__)
except Exception as e:
    print("Installed, but cannot read version attr:", e)
PY

# По умолчанию просто выходим
CMD ["python", "-c", "import immunity_agent_python; print('OK')"]
