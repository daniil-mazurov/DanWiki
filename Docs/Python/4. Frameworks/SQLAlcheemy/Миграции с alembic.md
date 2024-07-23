Миграция БД - это процесс сохранения и переноса структуры БД (==Не данных таблиц - значений строк, колонок и т.д., а именно структуры - таблицы, типы данных==) - моделей, таблиц и т.д. в новую БД (чистую БД). Перенос может быть как текущей версии (`upgrade`), так и откатом к предыдущей ревизии (`downgrade`).

Инициализация проекта **alembic** и директории со скриптами миграций
```
alembic init path/to/migrations/folder
```

Создание ревизии (миграции), обновление проекта миграций (добавление или удаление типов данных или таблиц)
```
alembic revision --autogenerate -m 'revision_name'
```

Обновление БД до какой либо ревизии (по сути это и есть сам процесс миграции)
- `head` - до последней ревизии
- `revision_name` - до конкретной

```
alembic upgrade head
alembic upgrade revision_name
```

Откат к какой-либо из прошлых ревизий
- `base` - к первоначальной
- `revision_name` - к конкретной
```
alembic downgrade base
alembic downgrade revision_name
```
## Конфигурация проекция 
В `alembic.ini` добавление папки с проектом
```
prepend_sys_path = . src
```

Настройка `env.py`
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

from config import settings # url подключения к базе
from models import ExampleTable # импорт моделей
from database import Base # импорта метаданных


config = context.config 

if config.config_file_name is not None:
	fileConfig(config.config_file_name)

config.set_main_option(
	"sqlalchemy.url", settings.DATABASE_URL_asyncpg + "?async_fallback=True"
) # url подключения к базе

target_metadata = Base.metadata # подключение метаданных

...

def run_migrations_online() -> None:
	...
  

	with connectable.connect() as connection:
	
		context.configure(
			...
			compare_server_default=True, # Включение чувствительности к изменению параметра server_default
		)

		...

...
```