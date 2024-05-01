import doctest
from typing import Any


class Hashtable:
    def __init__(self, capacity: int) -> None:
        """
        capacity -> устанавливаем размер хэш таблицы
        self.table -> создаем хэш таблицу нужного размера

        >>> table = Hashtable(20)
        >>> table.size
        20

        """
        self.capacity = capacity
        self.table = [None] * capacity

    def __setitem__(self, key: [int, str, tuple, bool, float], value: Any) -> None:
        """
        Добавляем элемент в таблицу.
        Проблему с коллизией решил было трудно решить и скорее всего решение костыльное.
        Если элемент по расчитанному в _index хэшу уже существует, то мы ищем следующую ячейку и кладем туда пару.

        Как я понял, то если хэштаблица полная, то записать новый элемент мы не можем.
        Возможно стоило реализовать рейсайз таблицы, но не уверен, что это нужно в задаче.
        По крайней мере в ТЗ не сказано об этом. А четкого определения хэштаблицы именно с ресайзом не нашел.
        Поэтому мы поднимаем исключение ValueError, если таблица полная и пытаемся добавить новую пару.

        >>> table = Hashtable(5)
        >>> table[1] = 'qwerty'
        >>> 1 in table
        True
        >>> table[1] = 'some'
        >>> table[1]
        'some'

        """
        index = self._index(key)
        pair = self.table[index]
        counter = 0
        counter_not_none_pair = 0

        for _ in range(self.capacity):
            if self.table[_] is not None:
                counter_not_none_pair += 1

        if counter_not_none_pair > 0:
            while pair is not None and pair[0] != key:
                index += 1
                index %= self.capacity
                pair = self.table[index]
                counter += 1
                if counter == self.capacity:
                    break
            else:
                self.table[index] = (key, value)

        else:
            while self.table[index] is not None:
                index += 1
                index %= self.capacity

                if counter >= self.capacity:
                    raise ValueError(f'Cannot add {key}: {value}, because over limit hash table')
                    break

            else:
                self.table[index] = (key, value)

    def __getitem__(self, key: [int, str, tuple, bool, float]) -> Any:
        """
        Получаем значение по ключу.
        Метод реализован через цикл, как я считаю костыльно, но другого решения не смог придумать.
        Сложность заключается в обходе коллизии.

        Возвращаем значение из пары.

        >>> table = Hashtable(5)
        >>> table['start'] = 194
        >>> table['start']
        194

        """
        index = self._index(key)
        pair = self.table[index]

        while pair[0] != key:
            index += 1
            index %= self.capacity
            pair = self.table[index]

        return pair[1]

    def __contains__(self, key: [int, str, tuple, bool, float]) -> bool:
        """
        На вход принимаем ключ и возвращаем True или False взависимости от того есть у нас этот ключ в таблице или нет.

        >>> table = Hashtable(5)
        >>> table['start'] = 194
        >>> 'start' in table
        True

        """
        index = self._index(key)
        pair = self.table[index]
        counter_index = 0
        counter_not_none = 0

        for _ in range(self.capacity):
            if self.table[_] is not None:
                counter_not_none += 1

        if counter_not_none == 0:
            return False
        else:
            while pair[0] != key and pair is not None:
                index += 1
                index %= self.capacity
                pair = self.table[index]
                counter_index += 1
                if counter_index == self.capacity:
                    return False
                    break

        return pair[1]

    def __delitem__(self, key: [int, str, tuple, bool, float]) -> None:
        """
        На вход принимаем ключ и удаляем пару из таблицы.

        По ТЗ удаленное значение должно быть заменено на EMPTY. Не придумал, как это сделать.
        Видел, что такое реализуется через создание EMPTY = object(), но сюда уместить не смог.

        >>> table = Hashtable(5)
        >>> table['start'] = 194
        >>> 'start' in table
        True
        >>> del table['start']
        >>> 'start' in table
        False

        """
        index = self._index(key)
        pair = self.table[index]
        counter = 0

        while pair[0] != key:
            index += 1
            index %= self.capacity
            pair = self.table[index]
            counter += 1
            if counter == self.capacity:
                return False

        self.table[index] = None

    def _index(self, key: [int, str, tuple, bool, float]) -> int:
        """
        Рассчитываем хэш для ключа.
        """
        return hash(key) % self.capacity

    @property
    def size(self) -> int:
        """
        Возвращаем вместимость хэш таблицы

        """
        return len(self.table)

    @property
    def keys(self) -> list:
        """
        Возвращаем ключи из хэш таблицы в виде списка.
        """
        table_keys = []

        for _ in self.table:
            if _ is None:
                table_keys.append(_)
            else:
                table_keys.append(_[0])

        return table_keys

    @property
    def values(self) -> list:
        """
        Возвращаем значения из хэш таблицы в виде списка.
        """
        table_keys = []

        for _ in self.table:
            if _ is None:
                table_keys.append(_)
            else:
                table_keys.append(_[1])

        return table_keys

    def __str__(self) -> str:
        return str(self.table)


if __name__ == '__main__':
    doctest.testmod()
