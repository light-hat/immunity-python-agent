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

Конфигурирование агента:

```bash
python -m immunity_agent 127.0.0.1 80 test
```

Вызов через шелл, в качестве аргументов передаём хост и порт серверной части и имя приложения (должно быть создано на сервере).

Далее просто запустите Django-проект. Агент активируется автоматически.
