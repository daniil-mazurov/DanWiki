# Валидация различных типов данных
```python
from datetime import date
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, EmailStr

class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"
    ENGINEERING = "ENGINEERING"

class Employee(BaseModel):
    employee_id: UUID = uuid4()
    name: str
    email: EmailStr
    date_of_birth: date
    salary: float
    department: Department
    elected_benefits: bool
```
При создании объекта модели произойдет валидация переданных типов данных (согласно аннотированным).
Причем (если это возможно) будет произведено приведение типов:
```python
emp = Employee(
    name="Jack",
    email="jack@email.com",
    date_of_birth="1998-04-02",
    salary="10000",
    department="ENGINEERING",
    elected_benefits='False',
)
```
\>>>
>{'date_of_birth': datetime.date(1998, 4, 2),
 'department': <Department.ENGINEERING: 'ENGINEERING'>,
 'elected_benefits': False,
 'email': 'jack@email.com',
 'employee_id': UUID('9d386675-ef16-4923-9642-95722b808317'),
 'name': 'Jack',
 'salary': 10000.0}

> [!info] Входные данные могут быть в различных форматах
>
>```python
>Employee.model_validate() # < dict, json ...
>```

> [!info] Из модели данных можно получить json-схему параметров
>
>```python
>Employee.model_json_schema()
>```

# Расширенная валидация
```python
from datetime import date
from uuid import UUID, uuid4
from enum import Enum
from pydantic import BaseModel, EmailStr, Field

class Department(Enum):
    HR = "HR"
    SALES = "SALES"
    IT = "IT"
    ENGINEERING = "ENGINEERING"

class Employee(BaseModel):
    employee_id: UUID = Field(default_factory=uuid4, frozen=True)
    name: str = Field(min_length=1, frozen=True)
    email: EmailStr = Field(pattern=r".+@example\.com$")
    date_of_birth: date = Field(alias="birth_date", repr=False, frozen=True)
    salary: float = Field(alias="compensation", gt=0, repr=False)
    department: Department
    elected_benefits: bool
```

- **default_factory.** Значение по умолчанию. В примере выше мы задали `default_factory` равным `uuid4`. Это вызовет функцию `uuid4()` для генерации случайного UUID для `employee_id`, когда это необходимо. Вы также можете использовать лямбда-функцию для большей гибкости.
- **frozen.** Это булевский параметр, который вы можете установить, чтобы сделать ваши поля неизменяемыми.
- **min_length.** С помощью `min_length` и `max_length` можно контролировать длину строковых полей.
- **pattern.** Для строковых полей можно задать шаблон в виде regex-выражения.
- **alias.** Этот параметр можно использовать, когда вы хотите назначить псевдоним для своих полей. Например, псевдоним `birth_date` для `date_of_birth` и `compensation` для `salary`. Вы можете использовать эти псевдонимы при инстанцировании или сериализации модели.
- **gt.** Этот параметр используется для установки минимального значения для числовых полей. Буквосочетание «gt» — это сокращение от «greater than», что переводится как «больше, чем». В данном примере значение `gt=0` гарантирует, что зарплата всегда будет положительным числом. В Pydantic есть и другие [числовые ограничения](https://docs.pydantic.dev/latest/concepts/fields/#numeric-constraints), например `lt`, что означает «less than» («меньше, чем»).
- **repr.** Этот булевский параметр определяет, будет ли поле отображаться в представлении полей модели. В данном примере при печати экземпляра `Employee` вы не увидите `date_of_birth` или `salary`.

Собственная валидация настраивается следующим образом:
```python
@field_validator("param_name")
@classmethod
def check_param(cls, param_name: type):
	...
	if ...:
		raise ValueError("Bad value param")
	return param_name
```
# Валидация входных данных функции
```python
from typing import Annotated
from pydantic import PositiveFloat, Field, EmailStr, validate_call

@validate_call
def send_invoice(
    client_name: Annotated[str, Field(min_length=1)],
    client_email: EmailStr,
    items_purchased: list[str],
    amount_owed: PositiveFloat,
) -> str:
	...
```
# Валидация и считывание переменных окружения
Аннотирование типов происходит аналогично описанному выше, за исключением базового класса:
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
	...
```
Аннотированные переменные считываются при инициализации объекта класса из окружения (либо из файла `.env`)
Дополнительные настройки передаются в 
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class AppConfig(BaseSettings):
	model_config = SettingsConfigDict(
		env_file=".env", # Название файла с переменными
		env_file_encoding="utf-8", # Кодировка
		case_sensitive=True, # Чувствительность к регистру
		extra="forbid", # Запрет на дополнительные переменные
	)
```