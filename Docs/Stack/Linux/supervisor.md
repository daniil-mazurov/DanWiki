# Установка
```bash
sudo apt install supervisor
```
```bash
sudo systemctl enable supervisor --now
```
# Настройка supervisor

Конфигурационный файл программы находится по адресу **/etc/supervisor/supervisord.conf**. Здесь находятся основные настройки. Для настроек запускаемых процессов лучше использовать директорию **/etc/supervisor/conf.d/**. Основной конфигурационный файл можно оставить по умолчанию.

Для каждого процесса минимально надо передать такие переменные для того чтобы он автоматически запускался и восстанавливался после падения:

- **directory** - рабочая директория;
- **command** - команда запуска процесса;
- **user** - пользователь, от имени которого будет запущен процесс;
- **autostart** - нужно ли автоматически запускать процесс;
- **autorestart** - нужно ли перезапускать процесс;

> [!tip]- Дополнительные настройки
> Однако доступных настроек намного больше, вот некоторые из них:
> 
> - **priority** - приоритет запускаемого процесса;
> - **environment** - переменные окружения, которые надо передать процессу;
> - **stdout_logfile** - куда перенаправлять вывод stdout процесса;
> - **stderr_logfile** - куда перенаправлять вывод stderr процесса;
> - **process_name** - название процесса, с возможностью подстановки номера копии;
> - **numprocs** - количество запускаемых копий процесса;
> - **startretries** - количество попыток запустить программу;
> - **redirect_stderr** - перенаправить вывод ошибок процесса в вывод supervisor;
> - **redirect_stdout** - перенаправить вывод процесса в вывод supervisor.

Пример файла `process.conf`:

```bash
sudo nano /etc/supervisor/conf.d/process.conf
```

```
[program:process]
directory=/home/sergiy/program/
command=/usr/bin/php process.php
user=sergiy
autostart=true
autorestart=true
```
Затем надо перезапустить supervisor, это можно сделать с помощью systemctl:

```bash
sudo systemctl restart supervisor
```

Или с помощью утилиты supervisorctl:

```bash
sudo supervisorctl reload
```

## Проверка статуса процесса

```bash
sudo supervisorctl status
```

> [!help] Status
> Если процесс находится в состоянии **RUNNING**, значит всё хорошо и он был запущен успешно. Однако сейчас процесс запущен в одном экземпляре, а довольно часто надо запустить несколько копий одного и того же процесса. Для этого можно воспользоваться параметрами **process_name** и **numprocs**. Первый позволяет модифицировать имя процесса, так чтобы оно содержало номер копии, а второй указывает сколько копий надо запустить.

## Параметры
- В переменную **process_name** обычно прописывается шаблон форматирования строки python, который содержит название программы и номер процесса: **%(program_name)s_%(process_num)02d**. Здесь с скобках находится имя переменной, а за ними её тип. 
	```
	[program:process]  
	directory=/home/sergiy/program/  
	command=/usr/bin/php process.php  
	user=sergiy  
	autostart=true  
	autorestart=true  
	process_name=%(program_name)s_%(process_num)02d  
	numprocs=4  
	```

- Кроме того можно сохранять всё, что выводит программа в лог файл. Для этого используются параметры stdout_logfile и stderr_logfile. Например, можно прямо в папке с программой, выводить лог файл её выполнения.

```[program:process]   
directory=/home/sergiy/program/   
command=/usr/bin/php process.php   
user=sergiy   
autostart=true  
autorestart=true  
process_name=%(program_name)s_%(process_num)02d 
numprocs=4 
stdout_logfile=/home/sergiy/program/process.log   stderr_logfile=/home/sergiy/program/process.log.error
```

После перезагрузки сервиса в папке с программой появятся логи.

- Eсли вашей программе нужны какие-либо переменные окружения, вы можете их передать с помощью параметра environment. Переменные надо записать через запятую. Например:
	`environment=DISPLAY=":1",HOME="/root"`

> [!important]
> Можно подключится к процессу и посмотреть что он выводит в stdout/stderr с помощью команды **fg**:
> `sudo supervisorctl fg process:process_00`