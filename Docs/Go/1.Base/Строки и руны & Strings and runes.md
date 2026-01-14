- Руна = int32
- Например:

1. Символ Q = 0x51 (1 байт)
2. Символ ↯ = 0xE286AF (3 байта)

- Когда мы итерируемся по руне, мы итерируемся по байтам
- Строка = массив рун
```go
// Создание рун и строк
myRune := 'Q'
fmt.Println(myRune) // Выведет 81, что в 16-тиричной ситеме равно 0x51
myString := "This is my string"
fmt.Println(myString) // Выведет "This is my string"
myRawString := `This is my raw \nstring`
fmt.Println(myRawString) // Выведет "This is my raw \nstring" (проигнорирует символ переноса)
```