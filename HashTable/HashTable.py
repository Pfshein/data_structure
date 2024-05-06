"""
Реализация через один список норм) но чаще используют два списка - одни для значений и один для ключей
Рекомендую почитать - https://www.fluentpython.com/extra/internals-of-sets-and-dicts/
"""

import doctest
from typing import Any
from collections.abc import Hashable


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
        self.table: list[tuple[Hashable, Any] | None] = [None] * capacity  # с тайпингом сильно проще понимать код

    def __setitem__(self, key: [int, str, tuple, bool, float], value: Any) -> None:  # для key лучше использовать Hashable, чтобы можно было свои типы тоже использовать
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
        >>> table = Hashtable(1)
        >>> table[1] = 'qwerty'
        >>> table[2] = 'qwerty'

        """
        index = self._index(key)
        pair = self.table[index]
        counter = 0
        counter_not_none_pair = 0

        # тут ты при добавлении элемента каждый раз итериурешься и считаешь свободные ячейки
        # при больших размерах таблицы это будет сильно замедлять работу
        # плюс если я записал по ключу None, то это сломает это место
        # Можно просто определить в init параметр size и тут его изменять один раз
        for _ in range(self.capacity):  # '_' используется, когда игнорируем значение. А тут ты его дальше используешь. Нужно дать номарльно имя
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

                if counter >= self.capacity:  # это условие никогда не выполнится
                    raise ValueError(f'Cannot add {key}: {value}, because over limit hash table')
                    break  # это не нужно, так как выше кидаешь ошибку уже

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

        >>> table['other']  # это вызывает ошибку
        ...
        """
        index = self._index(key)
        pair = self.table[index]

        while pair[0] != key:  # при поиске обходишь все элементы, даже если встретил None. То есть для таблицы с одним элементов все равно будешь смотреть все
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

        for _ in range(self.capacity):  # лишний цикл
            if self.table[_] is not None:
                counter_not_none += 1

        if counter_not_none == 0:
            return False
        else:
            while pair[0] != key and pair is not None:
                index += 1
                index %= self.capacity  # получение следующего индекса лучше вынести в одельный метод, так как повторяется в нескольких местах, что-то вроде `def _get_next_index(self, index: int) -> int:`
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

        Выше верно написал, потому что иначе ппосле удаления как понять, что это удаленный элемент, а не пустое место?
        Это моежт быть нужно, чтобы при поиске не обходить всю таблицу, а искать до первого None

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

        for _ in self.table:  # не используй `_`, если потом ссылаешься на это значение!
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
