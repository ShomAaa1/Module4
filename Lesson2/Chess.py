from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from enum import Enum


Position = Tuple[int, int]
BoardType = List[List[Optional['ChessPiece']]]


class Color(Enum):
    """
    Перечисление возможных цветов шахматных фигур
    """
    WHITE = 'white'
    BLACK = 'black'


class ChessPiece(ABC):
    """
    Абстрактный базовый класс для шахматных фигур.

    Атрибуты:
        color (Color): Цвет фигуры (белый или черный)
        position (Position): Координаты фигуры на доске.
    """

    def __init__(self, color: Color, position: Position) -> None:
        """
        Инициализирует шахматную фигуру.
        :param color (Color): Цвет фигуры.
        :param position (Position): Начальная позиция фигуры на доске.

        Исключения:
        - ValueError: если передан не экземпляр enum Color

        Пример:
        >>> from enum import Enum
        >>> class Dummy(Rook):  # Используем существующий класс Rook
        ...     def __init__(self): super().__init__(Color.WHITE, (0, 0))
        >>> Dummy().color == Color.WHITE
        True

        >>> class InvalidPiece(ChessPiece):
        ...     def get_possible_moves(self, board): return []
        ...     def get_symbol(self): return "?"
        ...     def can_attack(self, x, y, board): return False
        >>> InvalidPiece("blue", (0, 0))
        Traceback (most recent call last):
            ...
        ValueError: The color must be white or black
        """
        if not isinstance(color, Color):
            raise ValueError('The color must be white or black')
        self.color: Color = color
        self.position: Position = position

    @abstractmethod
    def get_possible_moves(self, board: BoardType) -> List[Position]:
        """
        Возвращает список возможных ходов фигуры
        :param board: BoardType: Состояние шахматной доски.
        :return: List[Position]: Список допустимых координат ходов.
        """
        pass

    @abstractmethod
    def get_symbol(self) -> str:
        """
        Возвращает символьное представление фигуры.

        :return: str: Символ Unicode для данной фигуры.
        """
        pass

    @abstractmethod
    def can_attack(self, x: int, y: int, board: BoardType) -> bool:
        """
        Проверяет, может ли фигура атаковать заданную клетку
        :param x: int: координата х цели
        :param y: int: координата у цели
        :param board: BoardType: состояние доски
        :return: bool: True, если возможно атаковать, иначе False
        """
        pass

    def __str__(self) -> str:
        """
        Строковое представление фигуры (символ)
        :return: str: Символ фигуры
        """
        return self.get_symbol()

    def is_path_clear(self, x: int, y: int, board: BoardType, dx: int, dy: int) -> bool:
        """
        Проверяет, свободен ли путь до указанной клетки
        :param x: int, координата х цели
        :param y: int, координата у цели
        :param board: BoardType: состояние доски
        :param dx: int: изменение по х на каждом шаге
        :param dy: int: изменение по y на каждом шаге
        :return: bool: True, если путь свободен, иначе False
        """
        px, py = self.position
        cx, cy = px + dx, py + dy
        while (cx, cy) != (x, y):
            if board[cy][cx] is not None:
                return False
            cx += dx
            cy += dy
        return True


class Pawn(ChessPiece):
    """
    Класс, представляющий пешку.
    """
    def get_possible_moves(self, board: BoardType) -> List[Position]:
        """
        Возвращает список возможных ходов для пешки
        :param board: BoardType: Текущее состояние доски
        :return: List[Position]: Доступные позиции для хода.
        """
        x, y = self.position
        direction = 1 if self.color == 'white' else - 1
        moves: List[Position] = []

        # движение вперед
        if 0 <= y + direction < 8 and board[y + direction][x] is None:
            moves.append((x, y + direction))

        # Диагональные клетки для атаки
        for dx in [-1, 1]:
            nx, ny = x + dx, y + direction
            if 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target is not None and target.color != self.color:
                    moves.append((nx, ny))
        return moves

    def can_attack(self, x:int, y:int, board:BoardType) -> bool:
        """
        Проверяет, может ли пешка атаковать заданную клетку
        :param x: int: координата х цели
        :param y: int: координата у цели
        :param board: BoardType: состояние доски
        :return: bool: True, если может атаковать, иначе False
        """
        if not (0 <= x <8 and 0 <= y < 8):
            return False

        px, py = self.position
        direction = 1 if self.color == 'white' else -1
        # Проверяем, что цель по диагонали вперед
        if (x == px - 1 or x == px + 1) and (y == py + direction):
            target = board[y][x] # Получаем фигуру на клетке
            if target is not None and target.color != self.color:
                return True
        return False

    def get_symbol(self) -> str:
        """
        Символ пешки
        :return: str: '♙'  или '♟'
        """
        return '♙' if self.color == 'white' else '♟'


class Rook(ChessPiece):
    """
    Класс, представляющий ладью
    Ладья может перемещаться на любое количество клеток по горизонтали и вертикали
    Пример использования:
    >>> board = [[None for _ in range(8)] for _ in range(8)]
    >>> rook = Rook(Color.WHITE, (0, 0))
    >>> board[0][0] = rook
    >>> moves = rook.get_possible_moves(board)
    >>> (0, 1) in moves
    True
    """
    def get_possible_moves(self, board: BoardType) -> List[Position]:
        """
        Возвращает список возможных ходов ладьи
        :param board: BoardType: состояние доски
        :return: List[Position]: список координат доступных ходов

        >>> board = [[None for _ in range(8)] for _ in range(8)]
        >>> rook = Rook(Color.WHITE, (0, 0))
        >>> board[0][0] = rook
        >>> sorted(rook.get_possible_moves(board)) #doctest: +NORMALIZE_WHITESPACE
        [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0)]
        """
        x, y = self.position
        moves: List[Position] = []

        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]  # вправо, влево, вверх, вниз

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target is None:
                    moves.append((nx, ny))
                elif target.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy

        return moves

    def can_attack(self, x: int, y: int, board: BoardType) -> bool:
        """
        Проверяет возможность атаки по прямой линии
        :param x: int: координата х цели
        :param y: int: координата у цели
        :param board: BoardType: состояние доски
        :return: bool: True, если может атаковать, иначе False
        """
        px, py = self.position
        if x != px and y != py:
            return False  # Не по вертикали или горизонтали

        dx = 0 if x == px else (1 if x > px else -1)
        dy = 0 if y == py else (1 if y > py else -1)

        if not self.is_path_clear(x, y, board, dx, dy):
            return False

        target = board[y][x]
        return target is not None and target.color != self.color

    def get_symbol(self) -> str:
        """
        Символ ладьи
        :return: str: '♖' или '♜'
        """
        return '♖' if self.color == 'white' else '♜'


class Bishop(ChessPiece):
    """
    Класс, представляющий слона
    """
    def get_possible_moves(self, board: BoardType) -> List[Position]:
        """
        Возвращает возможные диагональные ходы слона
        :param board: BoardType: состояние доски
        :return: List[Position]: Список возможных координат ходов
        """
        x, y = self.position
        moves: List[Position] = []

        directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            while 0 <= nx < 8 and 0 <= ny < 8:
                target = board[ny][nx]
                if target is None:
                    moves.append((nx, ny))
                elif target.color != self.color:
                    moves.append((nx, ny))
                    break
                else:
                    break
                nx += dx
                ny += dy

        return moves

    def can_attack(self, x: int, y: int, board: BoardType) -> bool:
        """
        Проверяет возможность диагональной атаки
        :param x: int: координата х цели
        :param y: int: координата у цели
        :param board: BoardType: состояние доски
        :return: bool: True, если может атаковать, иначе False
        """
        px, py = self.position
        dx = x - px
        dy = y - py

        if abs(dx) != abs(dy):
            return False  # Не по диагонали

        step_x = 1 if dx > 0 else -1
        step_y = 1 if dy > 0 else -1

        if not self.is_path_clear(x, y, board, step_x, step_y):
            return False

        target = board[y][x]
        return target is not None and target.color != self.color

    def get_symbol(self) -> str:
        """
        Символ слона
        :return: str: '♗' или '♝'
        """
        return '♗' if self.color == 'white' else '♝'


class ChessBoard:
    """
    Класс, представляющий шахматную доску 8х8
    """
    def __init__(self) -> None:
        """
        Инициализирует пустую шахматную доску
        """
        self.board: BoardType = [[None for _ in range(8)] for _ in range(8)]

    def place_piece(self, piece: ChessPiece) -> None:
        """
        Размещает фигуру на доске по ее позиции
        :param piece: ChessPiece: Фигура для размещения
        """
        x, y = piece.position
        self.board[y][x] = piece # y- строка, x - столбец

    def move_piece(self, from_pos: Position, to_pos: Position) -> None:
        """
        Перемещает фигуру, если ход допустим
        :param from_pos: Position: Начальная позиция
        :param to_pos: Position: Целевая позиция
        """
        x1, y1 = from_pos
        x2, y2 = to_pos
        piece = self.board[y1][x1]

        if not piece:
            print('На выбранной клетке нет фигуры')
            return

        possible_moves = piece.get_possible_moves(self.board)
        if to_pos in possible_moves:
            print(f'Перемещаем {piece} из {from_pos} в {to_pos}')
            self.board[y2][x2] = piece
            self.board[y1][x1] = None
            piece.position = (x2, y2)
        else:
            print(f'{piece} не может пойти на {to_pos}')

    def display(self) -> None:
        """
        Отображает доску с фигурами в текстовом виде
        """
        print("  +---+---+---+---+---+---+---+---+")
        for y in range(7, -1, -1):
            row = f"{y+1} |"
            for x in range(8):
                piece = self.board[y][x]
                if piece is None:
                    row += ' . |'
                else:
                    row += f' {piece} |'
            print(row)
            print("  +---+---+---+---+---+---+---+---+")
        print("    a   b   c   d   e   f   g   h")


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    chessboard = ChessBoard()

    # Размещаем фигуры
    p1 = Pawn(Color.WHITE, (4, 1))
    r1 = Rook(Color.BLACK, (0, 0))
    b1 = Bishop(Color.WHITE, (2, 0))
    r2 = Rook(Color.BLACK, (5, 2))

    chessboard.place_piece(p1)
    chessboard.place_piece(r1)
    chessboard.place_piece(b1)
    chessboard.place_piece(r2)

    # Показываем доску
    chessboard.display()

    # Получаем возможные ходы и атаки
    print('\n♙ Возможные ходы пешки (е2):')
    for move in p1.get_possible_moves(chessboard.board):
        print(move)

    print('\n♜ Возможные ходы ладьи (а1):')
    for move in r1.get_possible_moves(chessboard.board):
        print(move)

    print('\n♗ Возможные ходы слона (с1):')
    for move in b1.get_possible_moves(chessboard.board):
        print(move)

    print('\n♜ Возможные ходы ладьи (f3):')
    for move in r2.get_possible_moves(chessboard.board):
        print(move)

    # Проверка атаки слона
    print('\n ♗ Может ли слон атаковать пешку на е2?')
    can_bishop_attack_pawn = b1.can_attack(4,1, chessboard.board)
    print('Да' if can_bishop_attack_pawn else 'Нет')



