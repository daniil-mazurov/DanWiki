# Установка
> [!important] Установка poetry
> Poetry всегда следует устанавливать в выделенной виртуальной среде, чтобы изолировать ее от остальной части вашей системы. Его ни в коем случае нельзя устанавливать в среде проекта, которым будет управлять Poetry. Это гарантирует, что собственные зависимости Poetry не будут случайно обновлены или удалены. (Каждый из следующих методов установки гарантирует, что Poetry будет установлен в изолированную среду.) Кроме того, изолированная виртуальная среда, в которой установлен poetry, не должна быть активирована для выполнения команд poetry.

```
pipx install poetry
```
OR
[Через установщик](https://python-poetry.org/docs/#installing-with-the-official-installer)
# Конфигурация

^ebe4a7

## poetry config

Если сразу после установки запросить перечень настроек Poetry, можно увидеть следующее:

```
poetry config --list

cache-dir = "/…/…/.cache/pypoetry"
virtualenvs.create = true
virtualenvs.in-project = null
virtualenvs.path = "{cache-dir}/virtualenvs"  # /home/astynax/.cache/pypoetry/virtualenvs
```

Poetry работает с виртуальными окружениями. При этом он изначально настроен так, что у вас будет много разных версий Python. По этой причине инструмент создает виртуальные окружения для проектов в непривычном месте — обратите внимание на настройку `virtualenvs.path`.

Можно использовать настройки по умолчанию, но Python-разработчики обычно хранят виртуальное окружение для каждого проекта в директории проекта, а именно в поддиректории `.venv`.

Вспомните, как вы создавали окружения командой `python3 -m venv .venv`. В Poetry стоит делать так же:

```
poetry config virtualenvs.in-project true
```

Теперь у каждого poetry-проекта виртуальное окружение будет при себе. Например, так можно переносить проект с одной машины на другую — достаточно просто скопировать директорию.
## pyproject.toml

Главный файл для poetry - это pyproject.toml. Все данные о проекты должны быть записаны в нём. При установке пакетов poetry берёт данные из этого файла и формирует файл с зависимостями poetry.lock (если уже есть готовый файл poetry.lock, то данные будут браться из него). Toml файл состоит из нескольких блоков, каждый из которых имеет свои особенности, рассмотрим данные блоки:

**[tool.poetry]** - содержит основную информацию о проекте, такую как:
- name - имя проекта
- version - версия проекта
- description - описание проекта
- license - лицензия проекта
- authors - список авторов проекта в формате name email
- maintainers - список менторов проекта формате name email
- readme - readme файл проекта в формате README.rst или README.md
- homepage - URL сайта проекта
- repository - URL репозитория проекта
- documentation- URL документации проекта
- keywords - список ключевых слов проекта  (макс: 5)
- classifier - список PyPI классификаторов

**[tool.poetry.dependencies]** - содержит описание всех зависимостей проекта. Каждая зависимость должна иметь название с указанием версии, также присутствует возможность скачать проекта с github с указанием ветки/версии/тэга, например:
- requests = "^2.26.0"
- requests = { git = "[https://github.com/requests/requests.git"](https://github.com/requests/requests.git") }
- requests = { git = "[https://github.com/kennethreitz/requests.git"](https://github.com/kennethreitz/requests.git"), branch = "next" }
- numpy = { git = "[https://github.com/numpy/numpy.git"](https://github.com/numpy/numpy.git"), tag = "v0.13.2" }

**[tool.poetry.scripts]** - в данном разделе можно описать различные сценарии или скрипты, которые будут выполняться при установке пакетов или при запуске приложения. Например:
- poetry = 'poetry.console:run'
- main-run = 'new_proj.main:run' (после чего достаточно запустить `poetry main-run` и будет выполнен запуск функции run в файле new_prof/main.py)

**[tool.poetry.extras]** - в данном блоке описываются группы зависимостей, которые можно устанавливать отдельно:
```
[tool.poetry.dependencies]
psycopg2 = { version = "^2.7", optional = true }
pymysql = { version = "1.0.2", optional = true }
[tool.poetry.extras]
mysql = ["pymysql"]
pgsql = ["psycopg2"]
```
Далее зависимости можно установить двумя способами:
```
poetry install --extras "mysql pgsql"
poetry install -E mysql -E pgsql
```

**[tool.poetry.urls]** - помимо основных URL, указанных в [tool.poetry], можно указывать свои URL:
- "Bug Tracker" = "[https://github.com/python-poetry/poetry/issues"](https://github.com/python-poetry/poetry/issues")
# Dict
## Создание нового проекта (Создает папку)

^281263

```
poetry new new_project
```
## Активация виртуального окружения
Poetry автоматически создает и управляет виртуальными окружениями для каждого проекта. Чтобы активировать виртуальное окружение для текущего проекта, используйте команду:
```
poetry shell
```
Показ всех виртуальных окружений:
```
poetry env list
```
Выбрать конкретную версию Python:
```
poetry env use python3.x
```
Выполнение скрипта может осуществляться без активации виртуального окружения:
```
poetry -C path/to/proj/dir run python path/script.py
```
## Инициализация проекта (в имеющихся файлах)
```
poetry init
```
- **name**: имя проекта
- **description**: описание проекта
- **author**: имя автора
- **python**: совместимые версии Python
- **dependency**: требуемый пакет с версией пакета
- **dev-dependency**: требования к разработке

После чего в проекте появится файл pyproject.toml, в котором вручную можно изменить любые данные.
## Установка зависимостей (разворачивание проекта)

^f999c7

```
poetry install
```
- **remove-untracked**: удалит старые пакеты, которые больше не используются в проекте
- **no-dev**: dev пакеты не будут устанавливаться

Poetry считывает данные из pyproject.toml, строит дерево зависимостей проекта, разрешая проблемы с версиями зависимостей, и устанавливает все пакеты.
Эта команда устанавливает все зависимости в окружение в директорию `.venv` внутри проекта. Активируется окружение командой `poetry shell`, а завершается командой `exit`
## Обновление версий зависимостей (тем самым обновив файл poetry.lock) 
```
poetry update
```
- **no-dev** : игнорирует обновление dev пакетов
- **lock** : не устанавливает и не обновляет пакеты, а только обновляет файл poetry.lock
## Добавление новой библиотеки
```
poetry add lib_name
```
- **dev** (-D): установит пакет в качестве dev зависимости
- **path**: путь к пакету (если пакет лежит локально)
- **lock** : не устанавливает зависимости, а только обновляет файл poetry.lock

Можно указывать версию пакета:
```
 poetry add "pygame>=2" 
 poetry add pygame@^2
```
Можно определить пакет в группу:
```
poetry add --group test pytest
```
## Удаление зависимости
```
poetry remove lib_name
```
## Просмотр зависимостей
```
poetry show
```
- **tree** (-t): список зависимостей в виде дерева
- **top-level** (-T): только верхнеуровневые пакеты
- **latest** (-l): показать последние версии проектов
- **outdated** (-o): показать последние версии только для устаревших пакетов
## Сборка проекта для перемещения
```
poetry build
poetry export -f requirements.txt --output dist/requirements.txt
poetry run pip download -r dist/requirements.txt -d dist/wheels
```
