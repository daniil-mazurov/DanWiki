# Docker install
Set up Docker's apt repository. 
## Add Docker's official GPG key:  
```bash
sudo apt-get update  
sudo apt-get install ca-certificates curl  
sudo install -m 0755 -d /etc/apt/keyrings  
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc  
sudo chmod a+r /etc/apt/keyrings/docker.asc  
```
## Add the repository to Apt sources:  
```bash
echo \  
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \  
$(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \ 
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```  
```bash
sudo apt-get update  
```

> [!note]
> If you use an Ubuntu derivative distribution, such as Linux Mint, you may need to use UBUNTU_CODENAME instead of VERSION_CODENAME.  
## Install the Docker packages.  
Latest Specific version  
To install the latest version, run:  
```bash
sudo apt-get install docker-ce docker-ce-cli http://containerd.io docker-buildx-plugin docker-compose-plugin  
```
Verify that the installation is successful by running the hello-world image:  
  
```bash
sudo docker run hello-world  
```
This command downloads a test image and runs it in a container. When the container runs, it prints a confirmation message and exits.

# Docker cmd
## Информация
- Cписок контейнеров активных  
```bash
docker ps
``` 
	-a Все контейнеры  
- Список образов  
```bash
docker images 
```
- Детальная информация о контейнере
```bash
docker inspect <container name>
```
- Вывести стандартный вывод контейнера  
```bash
docker logs <container name>
```
- Статистика по контейнерам
```bash
docker container stats  
```
## Запуск
- Cкачивание (если нет) образа и его запуск  
```bash
docker run <container name> <cmd>
```
	-d Запускает контейнер в фоновом режиме 
	-i - связать стандартный ввод хоста со стандартным вводом контейнера  
	-t - связать стандартный вывод хоста со стандартным выводом контейнера  
	-p 80:5000 сопоставить порт 80 хоста порту 5000 в контейнере
	-v /opt/datadir/:/var/lib/mysql смонтировать каталог /opt/datadir/ хоста в каталог /var/lib/mysql в контейнере
	--name <container title>  

- Выполняет команду в существующем контейнере на докер хосте 
```bash
docker exec <container id or name> <command>
```  
- Прикрепляет существующий контейнер к терминалу  
```bash
docker attach <container id or name>
```
- Скачивание образа с докерхаб  
```bash
docker pull <container name>
```
- Остановить контейнер
```bash
docker stop <container name> 
```
## Удаление
- Удаление контейнера (можно писать часть id и сразу несколько)  
```bash
docker rm <container name> 
```
- удаление образов (контейнеры без образа не работают)  
```bash
docker rmi <container name> 
```
## Сборка
- собрать образ из dockerfile в каталоге
```bash
docker build . -t имя
``` 
# Dockerfile
## .dockerignore
Помогает избежать отправки лишних или конфиденциальных файлов и каталогов демону и их добавления в образ командой ADD или COPY.

Вот пример .dockerignore файла:

```shell
# comment
    */temp*
    */*/temp*
    temp?
```

Этот файл обрабатывается следующим образом при сборке:

| Правило     | Поведение                                                                                                                                                                                       |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `# comment` | Игнорируется.                                                                                                                                                                                   |
| `*/temp*`   | Исключаются файлы и каталоги имена которых начинаются с `temp` в любой поддиректории корня. К примеру, данный файл `/somedir/temporary.txt` будет исключен, как и этот каталог `/somedir/temp`. |
| `*/*/temp*` | Исключает файлы и каталоги чье название начинается с `temp` во всех каталогах второго уровня. К примеру, `/somedir/subdir/temporary.txt`.                                                       |
| `temp?`     | Исключает файлы и папки в корневой директории чьи имена отличаются на один символ от `temp`. К примеру, `/tempa` и `/tempb` будут исключены.                                                    |
## ENV
```shell
ENV <key> <value>
ENV <key>=<value> ...
```

**Первая форма**, ENV `<key> <value>`, устанавливает значение одной переменной. Вся строка после первого пробела будет рассматриваться как `<value>` - включая пробелы и кавычки.

**Вторая форма**, ENV `<key>=<value>` ..., позволяет задать сразу несколько переменных.

Переменные окружения могут быть также использованы в других инструкциях как переменные интерпретируемые в Dockerfile. 

Переменные среды обозначаются в Dockerfile либо $variable_name, либо ${variable_name}. 
Они обрабатываются одинаково.
Пример (результат показан после #):

```shell
FROM busybox
ENV foo /bar
WORKDIR ${foo}   # WORKDIR /bar
ADD . $foo       # ADD . /bar
COPY \$foo /quux # COPY $foo /quux
```


> [!tip] Одноразовые переменные
> Для задания одноразовой переменной используйте 
> `RUN <key>=<value> <command>`.

## FROM
Инструкция FROM задает **базовый образ** для последующих инструкций. Dockerfile обязательно должен иметь инструкцию FROM. Можно использовать любой работающий образ, проще всего начать с загрузки образа из публичного репозитория.

- **FROM должен быть первой инструкцией в Dockerfile** (не считая комментариев и директив парсера).

```shell
FROM <image>
# или
FROM <image>:<tag>
# или
FROM <image>@<digest>
```
### FROM AS (много-этапные сборки)

Каждая инструкция FROM может использовать индивидуальный базовый образ и каждая из них начинает новую стадию сборки docker образа. 

Вы можете копировать необходимые артефакты из одной стадии в другую. В результате все вышеперечисленные шаги могут быть описаны вот так :

```shell
FROM golang:latest as build
COPY . .
RUN go build ./src/main.go

FROM alpine:latest as production
COPY --from=build /go/main .
CMD ["./main"]
```
## MAINTAINER

```shell
MAINTAINER Sergey Antropoff <sergey@antropoff.ru>
```

Инструкция MAINTAINER позволяет указать автора образа.

## RUN

RUN имеет две формы:

- **RUN <command>** (shell форма, команда выполняется в шеле, по умолчанию /bin/sh -c для Linux или cmd /S /C для Windows)
- **RUN ["executable", "param1", "param2"]** (exec форма)

Инструкция RUN выполняет любые команды в новом слое поверх текущего образа и делает коммит результата. Полученный после коммита образ будет использован для следующего шага в Dockerfile.
## LABEL

```shell
LABEL <key>=<value> <key>=<value> <key>=<value> ...
```

Инструкция LABEL добавляет метаданные для образа. 
Несколько примеров:

```shell
LABEL "com.example.vendor"="ACME Incorporated"
LABEL com.example.label-with-value="foo"
LABEL version="1.0"
LABEL description="This text illustrates \
that label-values can span multiple lines."
```

Образ может иметь несколько лейблов. Для этого, Docker рекомендует комбинировать лейблы в одной инструкции LABEL. **Каждая инструкция LABEL создает новый слой**, а большое количество слоев может негативно сказаться на скорости запуска образа.
## EXPOSE

```shell
EXPOSE <port> [<port>...]
```

Инструкция EXPOSE указывает Docker что контейнер слушает определенные порты после запуска. **EXPOSE не делает порты контейнера доступными для хоста.** Для этого, вы должны **использовать флаг -p** (что бы открыть диапазон портов) или флаг -P что бы открыть все порты из EXPOSE.
## ADD

ADD имеет две формы:

- **`ADD <src>... <dest>`**
- **`ADD ["<src>",... "<dest>"]`** (эта форма обязательна для путей с пробелами)

Инструкция ADD **копирует новые файлы, папки или или удаленные файлы по URLs из `<src>`** и добавляет их в файловую систему контейнера **в `<dest>`**.

`<dest>` абсолютный, или относительный путь для **WORKDIR**, куда будет произведено копирование в файловую систему контейнера.

```shell
ADD test relativeDir/  #adds "test" to `WORKDIR`/relativeDir/
ADD test /absoluteDir/ #adds "test" to /absoluteDir/
```

- Если `<src>` является URL и `<dest>` не заканчивается слешем, то файл загружается из URL и копируется в `<dest>`.
- Если `<src>`является URL и `<dest>` заканчивается слешем, то имя файла берется из URL и файл скачивается в `<dest>/<filename>`. Например, ADD http://example.com/foobar/ создаст файл /foobar. URL должен содержать имя файла, в противном случае докер не сможет загрузить его, как в этом примере (http://example.com не будет работать).
- Если `<src>` является каталогом, все содержимое каталога копируется, включая метаданные файловой системы.
> Сам каталог не копируется, только его содержимое.
- Если `<src>` является локальным tar архивом в поддерживаемом формате (gzip, bzip2 или xz), то он распаковывается как каталог. Ресурсы из удаленного URL не распаковываются. 
- Если `<src>` является файлом любого типа, он копируется вместе с метаданными. В случае, если `<dest>` заканчивается косой чертой (/), он будет считаться каталогом и содержимое `<src>` будет записано в `<dest>/base(<src>)`.
- Если задано несколько `<src>` ресурсов, или задан шаблон, то `<dest>` должен быть каталогом и заканчиваться косой чертой (/).
- Если `<dest>` не заканчивается слешем, он будет рассматриваться как обычный файл и содержимое `<src>` будет записано `<dest>`.
- Если `<dest>` не существует, то он будет создан со всеми недостающими каталогами.
## COPY

COPY имеет две формы:

- `COPY <src>... <dest>`
- `COPY ["<src>",... "<dest>"]` (эта форма используется для путей с пробелами)

Инструкция COPY копирует новые файлы или каталоги из `<src>` и добавляет их в файловую систему контейнера в `<dest>`.

> [!important] Различие между COPY и ADD
> **COPY работает только с локальными файлами, а ADD может обрабатывать удалённые URL-адреса и автоматически распаковывать tar-файлы**.
## ENTRYPOINT и CMD

ENTRYPOINT имеет две формы:

- **ENTRYPOINT ["executable", "param1", "param2"]** (exec форма, предпочтительная)
- **ENTRYPOINT command param1 param2** (shell форма)

Инструкция ENTRYPOINT позволяет настроить контейнер так что бы он работал как исполняемый файл.

Аргументы командной строки docker run `<image>` подставляются в самом конце в exec форме ENTRYPOINT и заменяются если такие же аргументы есть в инструкции CMD. Это позволяет передавать аргументы на точку входа, то есть docker run `<image>` -d передаст аргумент -d на точку входа. Вы можете заменить инструкцию ENTRYPOINT использовав флаг docker run --entrypoint.

Shell форма не позволяет командам CMD или run использовать аргументы командной строки, а также запускает ENTRYPOINT как субкоманду /bin/sh -c, которая не пропускает сигналы. Это означает что исполняемый файл не будет иметь PID 1 и не будет получать Unix сигналы - то есть не будет работать SIGTERM из docker stop `<container>`.

Только последняя инструкция ENTRYPOINT из Dockerfile будет запущена.
### Взаимодействие CMD и ENTRYPOINT

Обе инструкции CMD и ENTRYPOINT определяют какую команду выполнить при запуске контейнера. Есть несколько правил описывающих взаимодействие этих инструкций.

1. В Dockerfile следует задать хотя бы одну из команд CMD или ENTRYPOINT.
2. ENTRYPOINT должна быть задана при использовании контейнера в качестве исполняемого файла.
3. CMD используется для передачи аргументов по умолчанию для ENTRYPOINT или для выполнения специальной команды в контейнере.
4. CMD будет заменена если контейнер запускается с альтернативными аргументами.

Приведенная ниже таблица показывает как выполняются команды в зависимости от различных комбинаций ENTRYPOINT и CMD:


|                                | Без ENTRYPOINT             | ENTRYPOINT exec_entry p1_entry                            | ENTRYPOINT [“exec_entry”, “p1_entry”]          |
| ------------------------------ | -------------------------- | --------------------------------------------------------- | ---------------------------------------------- |
| **Без CMD**                    | _error, not allowed_       | /bin/sh -c exec_entry p1_entry                            | exec_entry p1_entry                            |
| **CMD [“exec_cmd”, “p1_cmd”]** | exec_cmd p1_cmd            | /bin/sh -c exec_entry p1_entry exec_cmd p1_cmd            | exec_entry p1_entry exec_cmd p1_cmd            |
| **CMD [“p1_cmd”, “p2_cmd”]**   | p1_cmd p2_cmd              | /bin/sh -c exec_entry p1_entry p1_cmd p2_cmd              | exec_entry p1_entry p1_cmd p2_cmd              |
| **CMD exec_cmd p1_cmd**        | /bin/sh -c exec_cmd p1_cmd | /bin/sh -c exec_entry p1_entry /bin/sh -c exec_cmd p1_cmd | exec_entry p1_entry /bin/sh -c exec_cmd p1_cmd |
## USER

`USER daemon`

Инструкция USER устанавливает имя пользователя (UID) от имени которого будет запущен образ, а также инструкции RUN, CMD и ENTRYPOINT содержащиеся в Dockerfile.
## WORKDIR

**WORKDIR /path/to/workdir**

Инструкция WORKDIR устанавливает рабочий каталог для всех инструкций RUN, CMD, ENTRYPOINT, COPY и ADD которые будут выполнены в Dockerfile. Если WORKDIR не задана, то она будет создана даже если в Dockerfile нет ни одной инструкции для которой это необходимо.

Инструкция может быть использована несколько раз в одном Dockerfile. Если указывается относительный путь, он будет определен относительно предыдущего значения WORKDIR. К примеру:

```shell
WORKDIR /a
WORKDIR b
WORKDIR c
RUN pwd
```

**В результате команда pwd из Dockerfile вернет значение /a/b/c.**
## ARG

**`ARG <name>[=<default value>]`**

Инструкция ARG задает переменные которые пользователь передает сборщику образа docker build с помощью флага **`--build-arg <varname>=<value>`**. Если пользователь указывает аргумент сборки, который не был определен в Dockerfile, сборка выдает ошибку.

```shell
One or more build-args were not consumed, failing build.
```

Автор Dockerfile может задать одну переменную задав ARG один раз или несколько переменных использовав ARGнесколько раз. Рассмотрим пример корректного Dockerfile:

```shell
FROM busybox
ARG user1
ARG buildno
...
```

Автор Dockerfile может опционально задать значение по умолчанию для переменной с помощью инструкции ARG:

```shell
FROM busybox
ARG user1=someuser
ARG buildno=1
...
```

Если ARG имеет значение по умолчанию и значение данной переменной не задано при сборке, сборщик использует значение по умолчанию.
## ONBUILD

`ONBUILD [INSTRUCTION]`

Инструкция ONBUILD добавляет к образу триггерную инструкцию, которая выполняется в последнюю очередь если образ используется в качестве базового для другой сборки. Триггер будет выполнен в дочернем контексте сборки, так если бы инструкция была вставлена сразу после инструкции FROM дочернего Dockerfile.
Для примера можно добавить что ни будь вроде этого:

```shell
[...]
ONBUILD ADD . /app/src
ONBUILD RUN /usr/local/bin/python-build --dir /app/src
[...]
```
# Примеры Dockerfile

Ниже вы можете увидеть некоторые примеры синтаксиса Dockerfile.

```shell
# Nginx
#
# VERSION               0.0.1

FROM      ubuntu
MAINTAINER Victor Vieux <victor@docker.com>

LABEL Description="This image is used to start the foobar executable" Vendor="ACME Products" Version="1.0"
RUN apt-get update && apt-get install -y inotify-tools nginx apache2 openssh-server
```

```shell
# Firefox over VNC
#
# VERSION               0.3

FROM ubuntu

# Install vnc, xvfb in order to create a 'fake' display and firefox
RUN apt-get update && apt-get install -y x11vnc xvfb firefox
RUN mkdir ~/.vnc
# Setup a password
RUN x11vnc -storepasswd 1234 ~/.vnc/passwd
# Autostart firefox (might not be the best way, but it does the trick)
RUN bash -c 'echo "firefox" >> /.bashrc'

EXPOSE 5900
CMD    ["x11vnc", "-forever", "-usepw", "-create"]
```

```shell
# Multiple images example
#
# VERSION               0.1

FROM ubuntu
RUN echo foo > bar
# Will output something like ===> 907ad6c2736f

FROM ubuntu
RUN echo moo > oink
# Will output something like ===> 695d7793cbe4

# You`ll now have two images, 907ad6c2736f with /bar, and 695d7793cbe4 with
# /oink.
```