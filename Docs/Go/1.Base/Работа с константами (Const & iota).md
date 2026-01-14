# Обычные константы
```go
const MaxSpeed = 30
MaxSpeed = 40 // Ошибка!
```
# iota
Аналог создания констант с использованием ключевого слова iota

**iota** - используется для автоматического задания значений констант (часто групповых)

```go
const (
	Undefined = iota
	Draft
	Active
) // 0, 1, 2
```
## Сдвиг начала + пропуски
```go
const (
	Undefined = iota + 3
	_
	Draft
	Active
) // 3, 5, 6
```