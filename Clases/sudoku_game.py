from Clases.linkedlist import LinkedList
from Clases.stack import Stack

class SudokuGame:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.history = Stack()  # Pila para el historial de movimientos
        self.game_over = False
        self.redo_moves = Stack()  # Pila para rehacer movimientos
        self.full_history = LinkedList()  # Usar la nueva lista enlazada en lugar de una lista simple

    def load_initial_configuration(self, file_path):
        with open(file_path, 'r') as file:
            for i, line in enumerate(file):
                for j, char in enumerate(line.strip()):
                    self.board[i][j] = int(char) if char.isdigit() else 0

    def make_move(self, row, col, number):
        if not self.game_over:
            prev_board = [row[:] for row in self.board]  # Copia del tablero antes del movimiento
            if self.is_valid_move(row, col, number):
                self.board[row][col] = number
                self.history.push((prev_board, (row, col), number))
                self.full_history.append((prev_board, (row, col), number))  # Agregar movimiento al historial completo
                if self.is_game_over():
                    self.game_over = True
                return True
        return False

    def undo_move(self):
        if not self.history.is_empty():
            prev_board, (row, col), number = self.history.pop()
            self.redo_moves.push((prev_board, (row, col), number))
            self.board = prev_board
            self.game_over = False
            self.full_history.append(('undo', prev_board, (row, col), number))  # Agregar movimiento deshecho al historial completo

    def redo_move(self):
        if not self.redo_moves.is_empty():
            prev_board, (row, col), number = self.redo_moves.pop()
            self.make_move(row, col, number)
            # No se agrega el movimiento rehecho al historial completo,
            # simplemente se marca como realizada la jugada rehecha.
            return True
        return False

    def suggest_move(self, row, col):
        current_number = self.board[row][col]
        suggestions = [num for num in range(1, 10) if self.is_valid_move(row, col, num)]
        suggestions.remove(current_number) if current_number != 0 else suggestions

        # Filtrar las sugerencias que estén en redo_moves
        redo_moves_set = {(move[1][0], move[1][1], move[2]) for move in self.redo_moves.items}
        suggestions = [suggestion for suggestion in suggestions if (row, col, suggestion) not in redo_moves_set]

        return suggestions


    def is_valid_move(self, row, col, number):
        return (
            self.is_valid_row(row, number) and
            self.is_valid_col(col, number) and
            self.is_valid_region(row, col, number)
        )

    def is_valid_row(self, row, number):
        return number not in self.board[row]

    def is_valid_col(self, col, number):
        return number not in [self.board[row][col] for row in range(9)]

    def is_valid_region(self, row, col, number):
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(start_row, start_row + 3):
            for j in range(start_col, start_col + 3):
                if self.board[i][j] == number:
                    return False
        return True

    def is_game_over(self):
        for i in range(9):
            if not (self.is_valid_row(i, 0) and
                    self.is_valid_col(0, i) and
                    self.is_valid_region(i // 3 * 3, (i % 3) * 3, 0)):
                return False
        return True

    def display_board(self):
        for row in self.board:
            print(" ".join(map(str, row)))
