import doctest
from typing import Any


class Node:
    def __init__(self, node: Any, prev_node: Any = None, next_node: Any = None):
        self.prev_node = prev_node
        self.node = node  # почему node? это value. node как то сбивает с толку тут, и код дальше читать сложнее
        self.next_node = next_node

    def __str__(self) -> str:
        return str(self.node)

    def get_next(self) -> Any | None:
        if not self.node:
            return

        return self.next_node

    def get_prev(self) -> Any | None:
        if not self.node:
            return

        return self.prev_node


class DoubleLinkedList:
    def __init__(self):
        self.head = None

    def insert_at_head(self, value: Any) -> None:
        """
        Вставляем элемент в начало списка.

        >>> new_list = DoubleLinkedList()
        >>> new_list.insert_at_head(5)
        >>> new_list.insert_at_head(10)
        >>> print(new_list)
        [10, 5]

        """
        if not self.head:
            self.head = Node(node=value)
        else:
            node = Node(node=value)
            node.next_node = self.head
            self.head.prev_node = node
            self.head = node

    def insert_at_end(self, value: Any) -> None:
        """
        Вставляем элемент в конец списка.

        >>> new_list = DoubleLinkedList()
        >>> new_list.insert_at_end(5)
        >>> new_list.insert_at_end(10)
        >>> print(new_list)
        [5, 10]

        """
        if not self.head:
            self.head = Node(node=value)
            return
        node = self.head
        while node.next_node:
            node = node.next_node
        new_node = Node(node=value)
        node.next_node = new_node
        new_node.prev_node = node

    def is_empty(self) -> bool:
        """
        Проверяем пустой ли список и возвращаем True, если пустой и False, если в нем есть элементы.

        >>> new_list = DoubleLinkedList()
        >>> new_list.insert_at_end(5)
        >>> new_list.is_empty()
        False
        >>> new_list.delete(5)
        >>> new_list.is_empty()
        True

        """
        return not self.head

    def delete_at_head(self) -> None:
        """
        Удаляем элемент в начале списка.

        >>> new_list = DoubleLinkedList()
        >>> new_list.insert_at_end(5)
        >>> new_list.insert_at_end(10)
        >>> new_list.delete_at_head()
        >>> print(new_list)
        [10]

        """
        if not self.head:
            print("The list has no element to delete")
            return
        if not self.head.next_node:
            self.head = None
            return
        self.head = self.head.next_node
        self.head.prev_node = None

    def delete(self, value: Any) -> None:
        """
        Удаляем элемент в списке.

        >>> new_list = DoubleLinkedList()
        >>> new_list.insert_at_end(5)
        >>> new_list.insert_at_end(10)
        >>> new_list.insert_at_end(100)
        >>> new_list.delete(10)
        >>> print(new_list)
        [5, 100]

        """
        if not self.head:
            print("List is empty")
            return

        if not self.head.next_node:  # можно объединить со следующим if
            if self.head.node == value:
                self.head = None
            return

        if self.head.node == value:
            self.head = self.head.next_node
            self.head.prev_node = None
            return

        node = self.head
        while node.next_node:
            if node.node == value:
                break
            node = node.next_node

        if node.next_node:
            node.prev_node.next_node = node.next_node
            node.next_node.prev_node = node.prev_node
        else:
            if node.node == value:
                node.prev_node.next_node = None
            else:
                print("Element not found")

    def search(self, value: Any) -> bool:
        """
        Находим элемент в списке

        >>> new_list = DoubleLinkedList()
        >>> new_list.insert_at_end(5)
        >>> new_list.insert_at_end(10)
        >>> new_list.insert_at_end(100)
        >>> new_list.search(10)
        True
        >>> new_list.delete(10)
        >>> new_list.search(10)
        False

        """
        if not self.head:
            return False
        node = self.head
        while node.node != value:
            node = node.next_node
            if node.next_node is None:
                return False
        else:
            return True

    def get_next(self) -> Any | None:
        """
        Берем следующий элемент из списка
        """
        if not self.head:
            return

        return self.head.next_node

    def get_prev(self) -> Any | None:  # у head никогда не будет previous. Метод не нужен
        """
        Берем предыдущий элемент из списка
        """
        if not self.head:
            return

        return self.head.prev_node

    def __str__(self) -> str:
        """
        Формируем список для print
        """
        node = self.head
        lst = []
        while node:
            lst.append(node.node)
            node = node.next_node
            if not node:  # не нужно
                break
        return str(lst)


if __name__ == '__main__':
    doctest.testmod()
