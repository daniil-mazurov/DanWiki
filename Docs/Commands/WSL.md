```
wsl --install
```
# DNS сервер
**/etc/wsl.conf**

```
[network]
generateResolvConf = false
```

**/etc/resolv.conf**

```
nameserver 8.8.8.8
```

Однако по какой-то причине мой `resolv.conf` продолжает воссоздаваться при каждой загрузке.

Поэтому мне пришлось сделать его неизменяемым, вот так:

```bash
sudo chattr +i /etc/resolv.conf
```