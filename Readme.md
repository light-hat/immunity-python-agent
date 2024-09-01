# Python agent

IAST-агент, встраиваемый в сканируемые приложения на Python. Инструментирование реализуется путём внедрения middleware для перехвата обработки запросов.

Поддерживаемые фреймворки:
- `Django`
- TODO: `Flask`

Установка агента:

```bash
pip install --index-url https://gitverse.ru/api/packages/immunity_iast/pypi/simple/ immunity-python-agent
```

Обновление установленного ранее пакета:

```bash
pip install --index-url https://gitverse.ru/api/packages/immunity_iast/pypi/simple/ immunity-python-agent --upgrade
```

Интеграция установленного агента в Django-проект:

```python
INSTALLED_APPS = [
    # ...
    'immunity_agent'
]

MIDDLEWARE = [
    # ...
    'immunity_agent.middlewares.django_middleware.ImmunityDjangoMiddleware'
]
```

Далее просто запустите Django-проект. Агент активируется автоматически.

Локальная сборка проекта:

```bash
docker build -t agent_builder .
```

Автоматическая публикация пакета с поднятием версии:

```powershell
.\deploy.ps1
```
