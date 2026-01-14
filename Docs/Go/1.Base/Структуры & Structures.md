# Создание структуры
```go
// Структура немного похожа на класс
type MyStruct struct {
	myStringField string
	myIntField    int
}

myStructDefault := MyStruct{}
myStructHalfDefault := MyStruct{myIntField: 5}
myStruct1 := MyStruct{"string", 5}
myStruct2 := MyStruct{myStringField: "string", myIntField: 5}
```
# Использование структуры
```go
myString := myStruct1.myStringField
myString, myInt := myStruct1.myStringField, myStruct1.myIntField
```
# Анонимные структуры
```go
myVar := struct {
	a string
	b int
}{
	"hello",
	5,
}
```