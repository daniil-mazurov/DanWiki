# Base
### Сопрограммы
Сопрограммы (coroutine) — это обобщенные формы подпрограмм. Они используются для кооперативных задач и ведут себя как генераторы Python.
Для определения сопрограммы асинхронная функция использует ключевое слово `await`. При его использовании сопрограмма передает поток управления обратно в цикл событий (также известный как event loop).
Для запуска сопрограммы нужно запланировать его в цикле событий. После этого такие сопрограммы оборачиваются в задачи (`Tasks`) как объекты `Future`.
### Задачи (tasks)
Задачи используются для планирования параллельного выполнения сопрограмм.
При передаче сопрограммы в цикл событий для обработки можно получить объект Task, который предоставляет способ управления поведением сопрограммы извне цикла событий.
### Циклы событий
Этот механизм выполняет сопрограммы до тех пор, пока те не завершатся. Это можно представить как цикл `while True`, который отслеживает сопрограммы, узнавая, когда те находятся в режиме ожидания, чтобы в этот момент выполнить что-нибудь другое.
Он может разбудить спящую сопрограмму в тот момент, когда она ожидает своего времени, чтобы выполниться. В одно время может выполняться лишь один цикл событий в Python.

![[Asyncio.jpg]]
## Принцип работы
**Как работает asyncio:**

- Создается **событийный цикл**, который будет управлять выполнением задач.
- Определяются сопрограммы (корутины), которые выполняют некоторую работу и могут приостанавливаться на операциях ввода-вывода с помощью ключевого слова `await`.
- Сопрограммы оборачиваются в задачи с помощью функции `asyncio.create_task()`.
- Задачи планируются для выполнения в событийном цикле с помощью функции `asyncio.run()` или добавляются в цикл вручную.
- Событийный цикл начинает выполнять задачи по очереди. Когда задача достигает операции ввода-вывода (например, `await asyncio.sleep()`), она приостанавливается, и событийный цикл переключается на другую задачу.
- Когда операция ввода-вывода завершается, задача возобновляется и продолжает выполнение до следующей операции ввода-вывода или завершения.

![[Asyncio2.jpg]]
**Пример работы:**
```python
import asyncio


async def async_func(task_no):
    print(f'{task_no}: Запуск ...')
    await asyncio.sleep(1)
    print(f'{task_no}: ... Готово!')


async def main():
    taskA = loop.create_task (async_func('taskA'))
    taskB = loop.create_task(async_func('taskB'))
    taskC = loop.create_task(async_func('taskC'))
    await asyncio.wait([taskA,taskB,taskC])


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except :
        pass
```
# DICT

^968f42
## Tasks
```python
asyncio.create_task(coro, *, name=None, context=None)
```
- **name** - имя задачи (вы также можете задать имя после создания объекта task через `Task.set_name(name)`, а затем получить имя задачи через `Task.get_name()`)
- **context** - позволяет присвоить задаче [контекстную переменную](https://superfastpython.com/asyncio-context-variables/) для реализации локального хранилища внутри задачи

Помимо простого ожидания завершения задачи, вы также можете отменить ее с помощью `Task.cancel()`, добавить функцию обратного вызова, которая будет вызываться по завершении задачи с помощью `Task.add_done_callback(cb)`, вручную проверить, выполнена ли сопрограмма с помощью `Task.done()`, или получить результат завершенной сопрограммы по завершении задачи с помощью `Task.result()`; ознакомьтесь с полным списком [методов задачи в документации Python](https://docs.python.org/3/library/asyncio-task.html#asyncio.Task).

```python
import asyncio 
async def my_function():     
	return "Hello World!"

async def main():     
	task = asyncio.create_task(my_function())         
	print(task.done())  # Will print False     
	await task     
	print(task.done())  # Will print True         
	print(task.result())  # Will print Hello World! 


asyncio.run(main())
```
## Waiting
### wait_for
```python
asyncio.wait_for(aw, timeout)
```
Эта функция принимает один ожидаемый объект (она автоматически оборачивает сопрограммы в объект задачи, чтобы его можно было запустить в цикле событий) и ожидает, пока это будет выполнено. Но в отличие от простого `await`, это также позволяет вам добавить тайм-аут - если выполнение задачи занимает больше времени, чем отведено для завершения, `TimeoutError` будет поднятa, и задача внутри `wait_for` отменяется.
```python
async def slow_function():
    await asyncio.sleep(100)

async def main():
    try:
        await asyncio.wait_for(slow_function(), timeout=5.0)
    except TimeoutError:
        print(‘Function was too slow :(‘)

asyncio.run(main())
```
### wait
```python
asyncio.wait(collection_of_tasks, *, timeout=None, return_when=ALL_COMPLETED)
```
Эта функция возвращает кортеж, содержащий два набора; первый набор - это завершенные задачи, а второй - те, которые еще не выполнены. Задачи, которые завершены до истечения времени ожидания или `return_when` директивы, входят в набор готовых задач, а те, которые не завершены, помещаются во второй набор, часто вызываемый `pending` or `_`, если вы не планируете их использовать. Однако, в отличие от `asyncio.wait,` незавершенные задачи не отменяются по истечении времени ожидания.

`return_when` Аргумент позволяет указать `asyncio.wait`, что нужно вернуться, когда произойдет одно из следующих трех событий:

- `FIRST_COMPLETED` возвращается, когда первая задача завершается или отменяется.
- `FIRST_EXCEPTION` возвращается, когда одна из задач вызывает исключение или все они завершаются.
- `ALL_COMPLETED` используется по умолчанию и вернется, когда все фьючерсы будут завершены или отменены.

```python
import asyncio
import random

async def job():
    await asyncio.sleep(random.randint(1, 5))

async def main():
    tasks = [
        asyncio.create_task(job(), name=index)
        for index in range(1, 5)
    ]

    done, pending = await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    print(f’The first task completed was {done.pop().get_name()}’)

asyncio.run(main())
```
### gather
```python
asyncio.gather(*aws, return_exceptions=False)
```

> [!info]- Дополнительно
> Принимает любое количество задач, будущих или даже объектов сопрограммы в качестве набора позиционных аргументов. Однако любые объекты сопрограммы, передаваемые в функцию, автоматически планируются как объекты задачи, чтобы они могли выполняться в цикле событий. 
> Еще одна приятная особенность `gather` заключается в том, что это единственная из трех функций, которая может корректно возвращать исключения. Если для `return_exceptions` аргумента ключевого слова установлено значение `True`, возвращаемый список будет содержать любое исключение, вызванное задачами, вместо того, где должно было быть значение результата задачи.
> Последняя особенность `asyncio.gather` заключается в том, что точно так же, как вы можете отменить отдельную задачу с помощью `Task.cancel()`, объект, который `gather` возвращает (для последующего ожидания), имеет свой собственный `cancel()` метод, который будет перебирать все задачи, которыми он управляет, и отменять их все.

После завершения всех задач все возвращаемые значения, полученные с помощью `Task.result()`, возвращаются в виде единого списка. Одна из самых приятных особенностей `gather` заключается в том, что возвращаемый список содержит задачи в точном порядке, в котором они были переданы в функцию!

```python
import asyncio
import random

async def job(id):
    print(f’Starting job {id}’)
    await asyncio.sleep(random.randint(1, 3))
    print(f’Finished job {id}’)
    return id

async def main():
    # create a list of worker tasks
    coros = [job(i) for i in range(4)]
    
    # gather the results of all worker tasks
    results = await asyncio.gather(*coros)
    
    # print the results
    print(f’Results: {results}’)

asyncio.run(main())
```
### as_completed
```python
asyncio.as_completed(aws, *, timeout=None)
```
Возвращает повторяющийся объект, который позволяет обрабатывать результаты по мере их завершения.

```python
import asyncio

async def my_task(id):
    return f’I am number {id}’


async def main():
    tasks = [my_task(id) for id in range(5)]
    
    for coro in asyncio.as_completed(tasks):
        result = await coro
        print(result)

asyncio.run(main())
```
### TaskGroup
`asyncio.TaskGroup` гарантирует, что в случае сбоя одной задачи в группе все остальные задачи будут отменены.

Вы можете использовать метод `tg.create_task()` для добавления задач в группу задач. При первом сбое какой-либо из задач группы задач все остальные задачи в группе будут отменены. Затем в сопрограмме появится исключение с группой задач в качестве `ExceptionGroup` или `BaseExceptionGroup`.

```python
import asyncio

async def do_something():
    return 1

async def do_something_else():
    return 2

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(do_something())
        task2 = tg.create_task(do_something_else())

    print(f’Everything done: {task1.result()}, {task2.result()}’)

asyncio.run(main())
```
### Запись в файл

```python
import aiofiles 
async with aiofiles.open(file, "a") as f:     
	for p in res:         
		await f.write(f"{url}\t{p}\n")
```
### Выполнять http-запросы
Используйте [`aiohttp`](https://lyz-code.github.io/blue-book/aiohttp/) библиотеку