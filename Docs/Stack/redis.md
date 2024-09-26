# Установка
```bash
sudo apt install redis-server iredis
```
# Конфигурация
**/etc/redis/redis.conf**

**requirepass** `password` - пароль пользователя при подключении

## Engine (client)
# DICT
## Проверка соединения
```python
client.ping() # > True or Exception
```
## SET (insert)
### str
```python
r.set('user:123:avatar', 'avatar.jpg')
avatar = r.get('user:123:avatar')
```

> TTL
```python
r.setex('user:123:session', timedelta(hours=1), 'active')
```
### int
```python
r.set('total_users', 1000)
```
### bytes
```python
r.set('image:123', b'\x89PNG\r\n...')
```
### dict
```python
r.hset('user:123', 'name', 'John')
name = r.hget('user:123', 'name')
```
### list
```python
r.lpush('chat:456:messages', 'Hello')
messages = r.lrange('chat:456:messages', 0, -1)
```
### set (datatype)
```python
r.sadd('group:789:members', 'user:123')
members = r.smembers('group:789:members')
```
#### sorted set
```python
r.zadd('leaderboard', {'user:123': 100, 'user:456': 80})
top_scores = r.zrange('leaderboard', 0, 2, withscores=True)
```
### TTL
```python
r.expire('user:123:session', 3600)  # Устанавливает срок действия в 1 час
```
## DELETE
```python
r.delete('user:123:avatar')
```

## PIPELINE
```python
# Создание объекта пайплайнаp
ipeline = r.pipeline()

# Добавление команд в пайплайн
pipeline.set('user:123:name', 'John')
pipeline.set('user:123:age', 30)
pipeline.get('user:123:name')
pipeline.get('user:123:age')

# Выполнение пайплайна и получение результатов
results = pipeline.execute()

# Результаты содержат значения полученных ключей
name = results[2]
age = results[3]
```

# Резервное копирование
BGSAVE
BGRESTORE