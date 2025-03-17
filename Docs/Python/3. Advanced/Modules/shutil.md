## Копирование файлов и директорий

Функция `shutil.copy()` позволяет копировать файлы.
```python
shutil.copy('source.txt','destination.txt')
```

Функция `shutil.copytree()` используется для копирования директорий:

```python
shutil.copytree('source_directory','destination_directory')
```
## Перемещение файлов и директорий

Для перемещения файлов и директорий используется функция `shutil.move()`:
```python
shutil.move('source.txt','destination.txt')

shutil.move('source_directory','destination_directory')
```
## Удаление файлов и директорий

Для удаления директорий используется функция `shutil.rmtree()`:
```python
shutil.rmtree('directory_to_remove')
```

Обратите внимание, что для удаления файлов следует использовать функцию `os.remove()` из модуля `os`.
## Архивирование файлов и директорий

Модуль `shutil` также предоставляет функции для работы с архивами. Вот пример создания архива:
```python
shutil.make_archive('archive_name','zip','directory_to_archive')
```
Для распаковки архивов используется функция `shutil.unpack_archive()`:
```python
shutil.unpack_archive('archive.zip','destination_directory')
```