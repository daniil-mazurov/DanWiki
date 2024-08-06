### Создание парсера
```python
parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
```
### Создание аргументов
```python
parse.add_argument()
```
metavar: str | tuple[str, ...] | None = ...,  
version: str = ...,  

| Параметр                                     | Значение                                                                                                                                                                                                                                          |
| -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `'name'`                                     | Позиционный аргумент (обязательный) передаваемый при запуске                                                                                                                                                                                      |
| `'-n', '--name'`                             | Опциональный аргумент (необязательный)                                                                                                                                                                                                            |
| `required: bool`                             | Делает аргумент (чаще именованный) обязательным для введения                                                                                                                                                                                      |
| `dest: str`                                  | Имя аргумента в краткой справке                                                                                                                                                                                                                   |
| `help: str`                                  | Описание аргумента (вызывается в  help)                                                                                                                                                                                                           |
| `type: str, obj, lamda`                      | Валидация типа данных передаваемого значения аргумента                                                                                                                                                                                            |
| `default: Any`                               | Значение по умолчанию для аргумента (может быть даже функцией)                                                                                                                                                                                    |
| `const: Any`                                 | Аргумент of `add_argument()` используется для хранения постоянных значений, которые не считываются из командной строки, но требуются для различных `ArgumentParser` действий.<br>`action='store_const'` or `action='append_const'` or `nargs='?'` |
| `choices: Iterable`                          | Допустимые значения аргумента                                                                                                                                                                                                                     |
| `metavar: str \| tuple[str, ...] \| None`    | Данные отображаемые как имя аргумента в usage блоке                                                                                                                                                                                               |
| ==**ACTION**==                               | ДЕЙСТВИЕ ДЛЯ ОБРАБОТКИ АРГУМЕНТА                                                                                                                                                                                                                  |
| `action="store_true"`, `action="store_true"` | Превращает параметр в флаг (значение переменной True/False, если флаг указан) - значение аргументу передавать не нужно (exception)                                                                                                                |
| `action="store_const"`                       | Превращает параметр в флаг (значение переменной `const`, если флаг указан) - значение аргументу передавать не нужно (exception)                                                                                                                   |
| `action="count"`                             | Превращает параметр в флаг (количество флагов интерпретируется в число: -v => 1 -vv => 2 и т.д.)                                                                                                                                                  |
| `acton="append"`, `acton="extend"`           | append: '--foo 1 --foo 2' > Namespace(foo=['1', '2']) <br>extend: '--foo  f1 --foo  f2  f3  f4' > Namespace(foo=['f1', 'f2', 'f3', 'f4'])                                                                                                         |
| ==NARGS==                                    | ДЕЙСТВИЕ ДЛЯ ОБРАБОТКИ АРГУМЕНТА                                                                                                                                                                                                                  |
| `nargs=integer (N)`                          | `N` аргументов из командной строки будут собраны в список <br>'c --foo a b' >Namespace(foo=['a', 'b'])                                                                                                                                            |
| `nargs='?'`                                  | Если аргумент не вызывается, то имеет значение default<br>Если вызывается, но ему не передается значение (флаг), то имеет значение 'const'                                                                                                        |
| `nargs='*'`                                  | Аналог `acton="extend"`                                                                                                                                                                                                                           |
| `nargs='+'`                                  | Аналог `nargs='*'`, но ввод значений обязателен                                                                                                                                                                                                   |
#### Валидация различных типов данных
```python
import argparse
import pathlib

parser = argparse.ArgumentParser()
parser.add_argument('count', type=int)
parser.add_argument('distance', type=float)
parser.add_argument('street', type=ascii)
parser.add_argument('code_point', type=ord)
parser.add_argument('source_file', type=open)
parser.add_argument('dest_file', type=argparse.FileType('w', encoding='latin-1'))
parser.add_argument('datapath', type=pathlib.Path)
```
#### Комбинирование позиционных и опциональных аргументов
```python
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("square", type=int,
                    help="display a square of a given number")
parser.add_argument("-v", "--verbose", action="store_true",
                    help="increase output verbosity")
args = parser.parse_args()
answer = args.square**2
if args.verbose:
    print(f"the square of {args.square} equals {answer}")
else:
    print(answer)
```
	$ python prog.py
	usage: prog.py [-h] [-v] square
	prog.py: error: the following arguments are required: square
	$ python prog.py 4
	16
	$ python prog.py 4 --verbose
	the square of 4 equals 16
	$ python prog.py --verbose 4
	the square of 4 equals 16
#### Взаимоисключаемые аргументы
```python
parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-v", "--verbose", action="store_true") # ИСКЛЮЧАЕТ -q
group.add_argument("-q", "--quiet", action="store_true") # ИСКЛЮЧАЕТ -v
parser.add_argument("x", type=int, help="the base")
parser.add_argument("y", type=int, help="the exponent")
args = parser.parse_args()
```