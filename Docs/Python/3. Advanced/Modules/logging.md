# Base
## Уровни логирования
- `Debug (10)`: самый низкий уровень логирования, предназначенный для отладочных сообщений, для вывода диагностической информации о приложении.
- `Info (20)`: этот уровень предназначен для вывода данных о фрагментах кода, работающих так, как ожидается.
- `Warning (30)`: этот уровень логирования предусматривает вывод предупреждений, он применяется для записи сведений о событиях, на которые программист обычно обращает внимание. Такие события вполне могут привести к проблемам при работе приложения. Если явно не задать уровень логирования — по умолчанию используется именно `warning`.
- `Error (40)`: этот уровень логирования предусматривает вывод сведений об ошибках — о том, что часть приложения работает не так как ожидается, о том, что программа не смогла правильно выполниться.
- `Critical (50)`: этот уровень используется для вывода сведений об очень серьёзных ошибках, наличие которых угрожает нормальному функционированию всего приложения. Если не исправить такую ошибку — это может привести к тому, что приложение прекратит работу.
## Когда?
1. В начале операции (подключение к чему-то, что-то запустилось и т.д.)
2. При достигнутом прогрессе (что-то успешно, что-то получено)
3. При завершении операции (все прошло круто или что-то не получилось)

==Лог должен нести информацию, которую **_можно_** использовать.==
Пример:

| **Сообщение**                           | **Понимание картины**               | **Контекст**                                                                                          |
| --------------------------------------- | ----------------------------------- | ----------------------------------------------------------------------------------------------------- |
| `Connecting to AWS`                     | Началась операция с AWS             | Атрибуты лога должны позволить мне выяснить, кто его вызвал                                           |
| `Retrieved instances from all regions`  | Был достигнут существенный прогресс | -                                                                                                     |
| `Connection to AWS has been successful` | Операция с AWS завершилась          | Атрибуты лога должны позволить мне найти сущности, на которые операция произвела положительный эффект |
Пример логов об ошибках

| **Сообщение**                                                                            | **Понимание картины**                                                                      | **Контекст**                                                                                            |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------- |
| `Connecting to AWS`                                                                      | Началась операция с AWS                                                                    | Атрибуты лога должны позволить мне выяснить, кто его вызвал                                             |
| `Failed to retrieve instances from regions af-south-1 when connecting to AWS for user X` | Операция AWS не завершена, произошел сбой в регионе _af-south-1_, пострадал пользователь X | Я должен иметь возможность увидеть трассировку стека ошибки, чтобы понять, почему извлечение не удалось |

В обоих случаях, я могу отследить, когда произошло какое-то событие (в логах есть отметки о времени), что именно произошло и кто от этого пострадал.
# Dict
- **Логгер** - локальный объект создания лога
```python
logger = logging.getLogger(__name__)
```
- **Форматтеры** вызываются для вывода конечного сообщения и отвечают за него преобразование в конечную строку.
```ini config
[formatter_default]
format=%(asctime)s - [%(levelname)-8s] - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```
	2024-07-31 16:53:20 - [INFO    ] - (_main.py).main(17) - An INFO
	2024-07-31 16:53:20 - [WARNING ] - (_main.py).main(18) - A WARNING
	2024-07-31 16:53:20 - [ERROR   ] - (_main.py).main(19) - An ERROR
	2024-07-31 16:53:20 - [CRITICAL] - (_main.py).main(20) - A message of CRITICAL severity
- **Обработчики** (хэндлеры) представляют из себя комбинации форматтеров, выходных данных (потоков) и фильтров.
```ini config
[handler_console]
class=logging.StreamHandler
level=DEBUG
formatter=console
args=(sys.stdout,)
```

> [!tip]- Дополнительный пример
>
>```python
>import logging
>
>_log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
>
>def get_file_handler():    
>	file_handler = logging.FileHandler("x.log")    
>	file_handler.setLevel(logging.WARNING)    
>	file_handler.setFormatter(logging.Formatter(_log_format))    
>	return file_handler
>
>def get_stream_handler():    
>	stream_handler = logging.StreamHandler()    
>	stream_handler.setLevel(logging.INFO)    
>	stream_handler.setFormatter(logging.Formatter(_log_format))    
>	return stream_handler
>
>def get_logger(name):    
>	logger = logging.getLogger(name)    
>	logger.setLevel(logging.INFO)    
>	logger.addHandler(get_file_handler())    
>	logger.addHandler(get_stream_handler())    
>	return logger
>```

- **Сообщения в лог**
```python
logger.debug("A DEBUG Message")
logger.info("An INFO")
logger.warning("A WARNING")
logger.error("An ERROR")
logger.critical("A message of CRITICAL severity")
```

## Логирование исключений ^0dba98
1. `logger.error`
```python
try:
	printf("text")
except NameError as err:
	logger.error(err, exc_info=True)
```
	2024-08-01 15:57:13 - [ERROR   ] - (template_1.py).func(17) name 'printf' is not defined
	Traceback (most recent call last):
	  File "C:\code\project_template\.\src\template_1.py", line 14, in func 
		  printf("text")
	NameError: name 'printf' is not defined
2. `logger.exception`
```python
try:
	printf("text")
except Exception:
	logger.exception(Exception)
```
	2024-08-01 16:00:10 - [ERROR   ] - (template_1.py).func(18) <class 'Exception'>
	Traceback (most recent call last):
		File "C:\code\project_template\.\src\template_1.py", line 14, in func
			printf("text")
	NameError: name 'printf' is not defined
==Пример с известным исключением== ^ce793c
```python
import logging

LOG = logging.getLogger()

class MyBigException(Exception): ...
class MyLocalException(MyBigException):
	def __init__(self, var) -> None:
	self.var = var
	super().__init__(f"my text with {var=}")
	
# LOCAL	
def func():
	try:
		...
		raise MyLocalException(1)
		...
    except MyBigException:
        LOG.exception('local error')
        raise
```
==Пример с неизвестным исключением==
```python
try:
	...
except Exception as e:
	LOG.exception(f'local error: {e}')
	raise
	# raise MyBigException from e
```
# Extra
Реализация логирования значений переменных через кастомный форматтер

```ini config
[formatter_default]
class=config.ExtraFormatter
format=%(asctime)s - [%(levelname)-8s] - (%(filename)s).%(funcName)s(%(lineno)d) %(message)s
datefmt=%Y-%m-%d %H:%M:%S
```

```python
class ExtraFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        self._style._fmt = self._fmt

        default_attrs = logging.LogRecord(*[None] * 7).__dict__.keys()
        extras = set(record.__dict__.keys()) - default_attrs - {"message"}

        if extras:
            format_str = "\n" + "\n".join(f"{val}: %({val})s" for val in sorted(extras))
            self._style._fmt += format_str

        return super().format(record)
```

```python
logging.info("MAIN START", extra={"key123": "value123", "1": 2, "sdfsdf": 234324})
```
	2024-08-01 12:44:16 - [INFO    ] - (_main.py).<module>(25) MAIN START
	1: 2
	key123: value123
	sdfsdf: 234324
