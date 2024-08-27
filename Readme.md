# Python agent

IAST-агент, встраиваемый в сканируемые приложения на Python. Инструментирование реализуется путём внедрения middleware для перехвата обработки запросов.

Поддерживаемые фреймворки:
- `Django`
- `Flask`

Локальная сборка проекта:

```bash
docker build -t agent_builder .
```

Автоматическая публикация пакета с поднятием версии:

```powershell
.\deploy.ps1
```

Установка пакета:

```bash
pip install --index-url https://gitverse.ru/api/packages/immunity_iast/pypi/simple/ immunity-python-agent
```
