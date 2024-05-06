import doctest
from typing import Any


class Node:
    def __init__(self, node: Any, next_node: Any = None) -> None:
        self.node = node  # почему node? это value. node как то сбивает с толку тут, и код дальше читать сложнее
        self.next_node = next_node

    def __str__(self) -> str:
        return str(self.node)


class LinkedList:
    def __init__(self) -> None:
        self.head = None

    def insert_at_head(self, value: Any) -> None:
        """
        Добавляем элемент в начало списка.

        >>> linked_list = LinkedList()
        >>> linked_list.insert_at_head(5)
        >>> linked_list.insert_at_head(10)
        >>> print(linked_list)
        [10, 5]

        """
        if not self.head:
            self.head = Node(node=value)
        else:
            node = Node(node=value)
            node.next_node = self.head
            self.head = node

    def insert_at_end(self, value: Any) -> None:
        """
        Добавляем элемент в конец списка.

        >>> linked_list = LinkedList()
        >>> linked_list.insert_at_end(5)
        >>> linked_list.insert_at_end(10)
        >>> linked_list.insert_at_end(50)
        >>> linked_list.insert_at_end(100)
        >>> linked_list.insert_at_end('some')
        >>> print(linked_list)
        [5, 10, 50, 100, 'some']

        """
        if not self.head:
            self.head = Node(node=value)
        else:
            node = self.head
            while node.next_node:
                node = node.next_node
            node.next_node = Node(node=value)

    def is_empty(self) -> bool:
        """
        Проверяем пустой ли список и возвращаем True, если пустой и False, если в нем есть элементы.

        >>> linked_list = LinkedList()
        >>> linked_list.insert_at_end(5)
        >>> linked_list.is_empty()
        False
        >>> linked_list.delete(5)
        >>> linked_list.is_empty()
        True

        """
        return not self.head

    def delete(self, value: Any) -> None:
        """
        Удаляем элемент из списка.

        >>> linked_list = LinkedList()
        >>> linked_list.insert_at_end(5)
        >>> linked_list.insert_at_end(10)
        >>> linked_list.insert_at_end(50)
        >>> linked_list.insert_at_end(100)
        >>> linked_list.insert_at_end('some')
        >>> linked_list.delete('some')
        >>> print(linked_list)
        [5, 10, 50, 100]
        >>> linked_list.delete(50)
        >>> print(linked_list)
        [5, 10, 100]

        >>> linked_list.delete(123456)  # это приводит к ошибке
        >>> print(linked_list)
        [5, 10, 100]
        """
        node = self.head
        prev_node = node

        if self.head.node == value:
            self.head = self.head.next_node
        else:
            while node.node != value:
                prev_node = node
                node = node.next_node
                next_node = node.next_node  # тут берешь от предыдущего, но никак не проверяешь, что там есть следующий элемент
            node = prev_node  # этот шаг лишний, так как ничего не меняет
            node.next_node = next_node

    def delete_at_head(self) -> None:
        """
        Удаляем элемент с начала списка.

        >>> linked_list = LinkedList()
        >>> linked_list.insert_at_end(5)
        >>> linked_list.insert_at_end(10)
        >>> linked_list.insert_at_end(50)
        >>> linked_list.insert_at_end(100)
        >>> linked_list.insert_at_end('some')
        >>> print(linked_list)
        [5, 10, 50, 100, 'some']
        >>> linked_list.delete_at_head()
        >>> print(linked_list)
        [10, 50, 100, 'some']

        """
        if self.head:
            self.head = self.head.next_node
        else:
            raise ValueError('Linked List is empty')

    def search(self, value: Any) -> bool:
        """
        Ищем содержится ли элемент в списке, если да, то возваращем True. Если нет, возвращаем False
        >>> linked_list = LinkedList()

        >>> linked_list.search(50)  # будет ошибка

        >>> linked_list.insert_at_end(5)
        >>> linked_list.insert_at_end(10)
        >>> linked_list.insert_at_end(50)
        >>> linked_list.insert_at_end(100)
        >>> linked_list.insert_at_end('some')
        >>> linked_list.search(50)
        True

        """
        node = self.head
        while node.node != value:
            node = node.next_node
            if node.next_node is None:
                return False
        else:
            return True

    def __str__(self) -> str:
        node = self.head
        lst = []
        while node:
            lst.append(node.node)
            node = node.next_node
            if not node:  # не нужно, цикл и так не будет продолжаться, если node false
                break
        return str(lst)


if __name__ == '__main__':
    doctest.testmod()
