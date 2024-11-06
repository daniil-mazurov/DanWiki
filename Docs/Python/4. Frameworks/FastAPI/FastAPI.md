- https://frontend-spectre.ru/details/41971
# Валидация данных
Валидация происходит автоматически через аннотацию типов и модели pydantic
```python
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []

@app.post("/items/")
async def create_item(item: Item) -> Item:
    return item
```
# Обработка параметров запроса

Параметры запроса являются неотъемлемой частью построения API. FastAPI предоставляет простой способ обработки параметров запроса, определяя их в качестве аргументов функции в ваших функциях маршрутизации.

```python
@app.get("/items/")
async def read_item(skip: int = 0, limit: int = 10):
    pass
```

`Query`-параметры представляют из себя набор пар ключ-значение, которые идут после знака `?` в URL-адресе, разделенные символами `&` . 

Например, в этом URL-адресе:
`http://127.0.0.1:8000/items/?skip=0&limit=10`
...параметры запроса такие:
- `skip`: со значением `0`
- `limit`: со значением `10`
## Тело запроса и параметры пути
Помимо параметров запроса, FastAPI также поддерживает **параметры пути**, которые являются частями URL-адреса, используемого для идентификации ресурсов, о чем мы упоминали ранее (`` `{параметр}` ``).

Кроме того, вы можете передавать данные через **тело запроса**, используя (обычно) запросы POST и PUT для создания или обновления ресурсов.

Когда вам необходимо отправить данные из клиента (допустим, браузера, заполнив логин/пароль или отправив HTML-форму) в ваш API, вы отправляете их как **тело запроса**.

Тело запроса - это данные, отправляемые клиентом в ваш API. Тело ответа - это данные, которые ваш API отправляет клиенту. Чтобы объявить тело запроса, необходимо использовать **модели Pydantic**.
```python
# http://localhost:4599/item/0?update_optionals=false
@app.put("/item/{item_id}")
async def update_item(
    new_values: Item, # Тело запроса
    item_id: int, # Параметр пути
    update_optionals: bool = False, # Параметр запроса
) -> Item:
	pass
```

## Разница в способах определения **Path, Query и Body** параметров запроса (Глубочайшее пояснение)

1) **Path-параметры** указывается в маршруте в фигурных скобках {}, а потом в обработчике маршрута:

```python
@app.get("/{some_param}")
async def func_with_path_param(some_param: <type>):
```
или прописываем явно:
```python
@app.get("/{some_param}")
async def func_with_path_param(some_param: Annotated[<type>, Path()]):
```

2) **Body-параметры** представлены в виде Pydantic-моделей и указываются в виде параметра обработчика маршрута с типом соответствующего класса модели (о чем рассказывалось ранее):

```python
@app.post("/")
async def func_with_body_param(user: User):
```
или прописываем явно:
```python
@app.post("/")
async def func_with_body_param(user: Annotated[User, Body()]):
```

3) **Query-параметры** представлены просто в виде параметров обработчика маршрута (объявлены не двумя предыдущими способами):

```python
@app.get("/")
async def func_with_body_param(query_param: <type>):
```
или указываем явно:
```python
@app.get("/")
async def func_with_body_param(query_param: Annotated[<type>, Query()]):
```

# Загрузка файлов
```python
from typing import Annotated
from fastapi import FastAPI, File, UploadFile


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```
Разница между File и UploadFile в том, что File загружает только содержимое файла, а UploadFile загружает также метаинформацию вместе с самим содержимым.
