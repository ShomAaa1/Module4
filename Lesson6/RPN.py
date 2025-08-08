class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError('Попытка извлечь элемент из пустого стека')
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError('Стек пуст')
        return self.items[-1]

    def size(self):
        return len(self.items)


def evaluate_rpn(expression):
    stack = Stack()
    tokens = expression.split()

    for token in tokens:
        if token.lstrip('-').isdigit():
            stack.push(int(token))
        elif token in ['+', '-', '/', '*']:
            if stack.size() < 2:
                raise ValueError('Недостаточно операндов для выполнения операции')

            second_num = stack.pop()
            first_num = stack.pop()

            if token == '+':
                stack.push(first_num + second_num)
            elif token == '-':
                stack.push(first_num - second_num)
            elif token == '*':
                stack.push(first_num * second_num)
            elif token == '/':
                if second_num == 0:
                    raise ZeroDivisionError('Деление на ноль')
                stack.push(int(first_num/second_num))

        else:
            raise ValueError(f'Недопустимый токен: {token}')

    if stack.size() != 1:
        raise ValueError('Ошибка: в стеке должно остаться одно значение - результат')

    return stack.pop()


# ---Тестирование---
if __name__ == '__main__':
    expr = input('Введите выражение в обратной польской записи через пробел: ')
    try:
        result = evaluate_rpn(expr)
        print('Результат: ', result)
    except ValueError:
        print('Ошибка значения')
    except ZeroDivisionError:
        print('Деление на ноль')
    except IndexError:
        print('Недостаточно операндов в выражении')
