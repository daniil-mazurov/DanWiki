Зипуем файл
```
zip filename.zip folder
```
 - **-r** (Рекурсивно)

Установка смены раскладки на Alt + Shift
```
gsettings set org.gnome.desktop.wm.keybindings switch-input-source "['<Alt>Shift_L']"
```

### Выполняйте сразу несколько команд

Команды в терминале необязательно вбивать и выполнять по очереди. Их можно указывать не по одной, а сразу списком. Для этого их нужно разделить двумя амперсандами (`&&`).


```bash
mkdir second-project && cd second-project && touch index.html style.css
# создаём папку second-project,
# переходим в папку second-project
# и создаём в ней два файла: index.html и style.css 
```

# Отключение спящего режима
```bash
sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target
```

# WSL
[[WSL]]
# Cron
[[cron]]
# Supervisor
[[supervisor]]