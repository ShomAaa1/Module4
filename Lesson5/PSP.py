class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        raise IndexError('Стек пуст')

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None


def is_valid_bracket_sequence(sequence):
    stack = Stack()
    bracket_pairs = {'}': '{', ']': '[', ')': '('}

    for char in sequence:
        if char in '[{(':
            stack.push(char)
        elif char in ']})':
            if stack.is_empty():
                return False
            if stack.pop() != bracket_pairs[char]:
                return False

    return stack.is_empty()


input_str = input('Введите скобочную последовательность: ')
if not input_str:
    print('Пустая последовательность')
elif is_valid_bracket_sequence(input_str):
    print('Правильная скобочная последовательность')
else:
    print('Неправильная скобочная последовательность')

