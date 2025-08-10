from typing import List, Set


class Node:
    def __init__(self, value: str) -> None:
        self.value: str = value

        self.outbound: List['Node'] = []
        self.inbound: List['Node'] = []

    def point_to(self, other: 'Node') -> None:
        self.outbound.append(other)
        other.inbound.append(self)

    def __str__(self) -> str:
        return f'Node({self.value})'


class Graph:
    def __init__(self, root: Node) -> None:
        self._root: Node = root

    def dfs(self) -> List[Node]:
        visited: List[Node] = []
        stack: List[Node] = [self._root] # очередь вершин

        while stack:
            node = stack.pop()
            if node not in visited:
                visited.append(node)
                for neighbor in reversed(node.outbound):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return visited

    def bfs(self) -> None:
        visited: Set[Node] = set()
        stack: List[Node] = [self._root]
        visited.add(self._root)

        while stack:
            node = stack.pop(0)
            print(node.value, end=' ')

            for neighbor in node.outbound:  # идем по исходящим ребрам
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)


# Пример использования:
a = Node("A")
b = Node("B")
c = Node("C")
d = Node("D")

a.point_to(b)
a.point_to(c)
b.point_to(d)
c.point_to(d)

g = Graph(a)
print("BFS обход:")
g.bfs()

a = Node('a')
b = Node('b')
c = Node('c')
d = Node('d')
e = Node('e')
f = Node('f')
g = Node('g')
h = Node('h')
i = Node('i')
k = Node('k')
a.point_to(b)
b.point_to(c)
c.point_to(d)
d.point_to(a)
b.point_to(d)
a.point_to(e)
e.point_to(f)
e.point_to(g)
f.point_to(i)
f.point_to(h)
g.point_to(k)

g = Graph(a)
print("\nBFS обход:")
g.bfs()