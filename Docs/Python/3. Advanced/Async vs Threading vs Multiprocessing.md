В асинхронной модели несколько задач могут выполняться одновременно. Когда вызывается длительно выполняющаяся функция, она не блокирует поток выполнения программы. Вместо этого программа продолжает выполняться, а функция выполняется в фоновом режиме. Когда функция завершается, программа получает уведомление и может получить доступ к результату.
[[asyncio]]
```python
import asyncio  
  
async def download_file(url):  
	"""Download a file from a URL."""  
	with open(url, "wb") as f:  
		response = await asyncio.get(url)  
		f.write(response.content)  
  
async def main():  
	"""Download two files concurrently."""  
	tasks = [download_file("https://www.example.com/file1.txt"),  
	download_file("https://www.example.com/file2.txt")]  
	await asyncio.gather(*tasks)  
  
if __name__ == "__main__":  
	asyncio.run(main())
```
Многопоточность - это способ одновременного выполнения нескольких задач в рамках одного процесса. Это достигается путем создания нескольких потоков, каждый из которых выполняет свой собственный код.
```python
import threading  
  
def do_something_threaded():  
	"""Do something that takes a long time."""  
	time.sleep(1)  
	print("Done!")  
  
def main():  
	"""Start two threads."""  
	threads = []  
	for _ in range(2):  
		thread = threading.Thread(target=do_something_threaded)  
		threads.append(thread)  
	for thread in threads:  
		thread.start()  
	for thread in threads:  
		thread.join()  
  
if __name__ == "__main__":  
	main()
```
Многопроцессорность - это способ одновременного выполнения нескольких задач в отдельных процессах. Это достигается путем создания нескольких процессов, каждый из которых выполняет свой собственный код в своем собственном пространстве памяти.
```python
import multiprocessing  
  
def do_something_multiprocessed():  
	"""Do something that takes a long time."""  
	time.sleep(1)  
	print("Done!")  
  
def main():  
	"""Start two processes."""  
	processes = []  
	for _ in range(2):  
		process = multiprocessing.Process(target=do_something_multiprocessed)  
		processes.append(process)  
	for process in processes:  
		process.start()  
```
![[Python_async_threading_multi.jpg]]
![[1_AYX4HrL47oD441FtPDG68A.webp]]