
> [!important]
> - `map` не упорядочен, соответственно при итерировании получается случайная последовательность
> - при итерировании через `range` на выход подаются два значения: **ключ-значение** (аналог `dict.items()`)
# Создание мапы через make
```go
myMap := make(map[string]int) // map[]
```
# Создание непустой мапы
```go
myFilledMap := map[int]string{0: "Zero", 1: "One", 2: "Two"}

fmt.Println(myMap)
fmt.Println(myFilledMap) // map[0:Zero 1:One 2:Two]
```
# Операции с мапами
## 1. Добавить элемент
```go
myMap["One"] = 1 // map[One:1]
myMap["Two"] = 2 // map[One:1, Two:2]
```
## 2. Получить значение по ключу
```go
one := myMap["One"] // 1
```
## 3. Удалить пару по ключу
```go
delete(myMap, "One") // map[Two:2]
```
## 4. Проверить наличие ключа в мапе
```go
item, found := myMap["Two"] // item: 2, found: true
if !found {
	fmt.Println("item not found")
	return
}
item, found = myMap["One"] // item: 0, found: false
```
# Итерация по элементам мапы
```go
for key, value := range myFilledMap {
	fmt.Println(key, value) 
} // 2 Two, 0 Zero, 1 One
```