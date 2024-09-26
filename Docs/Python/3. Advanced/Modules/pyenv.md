# Установка
> [!important] Установка на Windows
> ```
>Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"; &"./install-pyenv-win.ps1" 
>```

> [!important] Установка на Linux
> `sudo apt install curl`
> `curl https://pyenv.run | bash`
> И после установки обновить **bashrc**, добавив строки:
> ```
> export PATH="~/.pyenv/bin:$PATH"
> eval "$(pyenv init -)"
> eval "$(pyenv virtualenv-init -)"
> ```
# Dict
- **Доступные версии Python**
(Выводится в виде списка)
```
pyenv install -l
```
- Установка python ^5f7c1f
```
pyenv install 3.x.x
```

> [!tip]- Проблемы при установке на Ubuntu
> ```bash
> sudo apt-get install build-essential zlib1g-dev libffi-dev libssl-dev libbz2-dev libreadline-dev libsqlite3-dev liblzma-dev libncurses-dev tk-dev openssl
> ```
- Вывод установленных версий
```
pyenv versions
```
- Установка глобального интерпретатора
(Глобальным он является только для `pyenv`, а не для всей системы)
```
pyenv global 3.x.x
```
