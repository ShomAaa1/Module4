from typing import TypeVar, Generic, List, Tuple, Optional

K = TypeVar('K')
V = TypeVar('V')


class MyDict(Generic[K, V]):
    def __init__(self) -> None:
        self._data: List[Tuple[K, V]] = []  # список пар (key, value)

    def __getitem__(self, key: K) -> Optional[V]:
        for k, v in self._data:
            if k == key:
                return v
        return None

    def __setitem__(self, key: K, value: V) -> None:
        for idx, (k, v) in enumerate(self._data):
            if k == key:
                self._data[idx] = (key, value)
                return
        self._data.append((key, value))  # если ключа нет, добавляем

    def __delitem__(self, key: K) -> None:
        for idx, (k, v) in enumerate(self._data):
            if k == key:
                del self._data[idx]
                return
        # если ключа нет, ничего не делаем

    def __contains__(self, key: K) -> bool:
        for k, _ in self._data:
            if k == key:
                return True
        return False

    def keys(self) -> List[K]:
        return [k for k, _ in self._data]

    def values(self) -> List[V]:
        return [v for _, v in self._data]

    def items(self) -> List[Tuple[K, V]]:
        return list(self._data)

    def __str__(self) -> str:
        items_str = ", ".join([f'{repr(k)}: {repr(v)}' for k, v in self._data])
        return '{' + items_str + '}'


my_dict = MyDict[str, object]()
my_dict['name'] = 'Alice'
my_dict['age'] = 30
print(my_dict['name'])  # Вернет 'Alice'
print('city' in my_dict)  # Вернет False
del my_dict['age']
print(my_dict.keys())  # Вернет ['name']
print(my_dict.values())  # Вернет ['Alice']
