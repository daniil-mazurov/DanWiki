Проблемы с относительным импортом
Внутри точки входа
```python
import os
import sys

sys.path.insert(1, os.path.dirname(os.path.abspath(__file__)))
```