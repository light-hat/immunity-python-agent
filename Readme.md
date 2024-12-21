# Python agent

IAST-агент, встраиваемый в сканируемые приложения на Python. Инструментирование реализуется путём внедрения middleware для перехвата обработки запросов.

Поддерживаемые фреймворки:
- `Django`
- `Flask`

## Установка

Выполните команду в терминале:

```bash
pip install --index-url https://gitverse.ru/api/packages/immunity_iast/pypi/simple/ immunity-python-agent
```

## Обновление

Выполните команду в терминале:

```bash
pip install --index-url https://gitverse.ru/api/packages/immunity_iast/pypi/simple/ immunity-python-agent --upgrade
```

## Конфигурирование

Выполните команду в терминале:

```bash
python3 -m immunity_agent 127.0.0.1 80 test
```

В качестве аргументов передаём хост и порт серверной части и имя проекта, ранее созданного на сервере.

## Интеграция в Django

Измените `settings.py`:

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

После перезапуска агент будет активирован автоматически.

## Интеграция в Flask

Укажите в `app.py`:

```python
app = flask.Flask(__name__)
app.wsgi_app = ImmunityFlaskMiddleware(app.wsgi_app, app.root_path)

# ...
```

После перезапуска агент будет активирован автоматически.
