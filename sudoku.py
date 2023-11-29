from tkinter import filedialog, messagebox
import tkinter as tk

class Stack:
    def __init__(self):
        self.items = []
        self.current = -1

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.current += 1
        self.items = self.items[:self.current]
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            item = self.items.pop()
            self.current -= 1
            return item
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[self.current]
        return None

    def size(self):
        return len(self.items)


class SudokuGame:
    def __init__(self):
        self.board = [[0] * 9 for _ in range(9)]
        self.history = Stack()  # Usando la pila para guardar el historial de movimientos
        self.redo_stack = Stack()  # Pila para rehacer movimientos
        self.game_over = False

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
                if not self.redo_stack.is_empty():
                    self.redo_stack = Stack()  # Limpiar la pila de rehacer al realizar un nuevo movimiento
                if self.is_game_over():
                    self.game_over = True
                return True
        return False

    def undo_move(self):
        if not self.history.is_empty():
            prev_board, (row, col), _ = self.history.pop()
            self.redo_stack.push((prev_board, (row, col), self.board[row][col]))
            self.board = prev_board
            self.game_over = False

    def redo_move(self):
        if not self.redo_stack.is_empty():
            prev_board, (row, col), number = self.redo_stack.pop()
            self.board = prev_board
            self.make_move(row, col, number)
            return True
        return False

    def suggest_move(self, row, col):
        current_number = self.board[row][col]
        suggestions = [num for num in range(1, 10) if self.is_valid_move(row, col, num)]
        suggestions.remove(current_number) if current_number != 0 else suggestions
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


class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")

        self.create_widgets()

        self.game = SudokuGame()

    def create_widgets(self):
        # Configuración de la ventana principal
        self.master.geometry("400x550")
        self.master.resizable(False, False)

        # Marco para organizar widgets
        frame = tk.Frame(self.master)
        frame.pack(pady=10)

        # Botón para cargar configuración
        load_button = tk.Button(frame, text="Cargar Sudoku", command=self.load_configuration_from_file)
        load_button.grid(row=0, column=0, columnspan=3, pady=10)

        # Etiquetas y entradas para fila, columna y número
        tk.Label(frame, text="Fila:").grid(row=1, column=0, padx=5)
        self.row_entry = tk.Entry(frame, width=5)
        self.row_entry.grid(row=1, column=1, padx=5)

        tk.Label(frame, text="Columna:").grid(row=1, column=2, padx=5)
        self.col_entry = tk.Entry(frame, width=5)
        self.col_entry.grid(row=1, column=3, padx=5)

        tk.Label(frame, text="Número:").grid(row=1, column=4, padx=5)
        self.num_entry = tk.Entry(frame, width=5)
        self.num_entry.grid(row=1, column=5, padx=5)

        # Botones para realizar una jugada, deshacer y rehacer movimientos
        make_move_button = tk.Button(frame, text="Hacer Mov", command=self.make_move)
        make_move_button.grid(row=2, column=0, columnspan=6, pady=10)

        undo_button = tk.Button(frame, text="Deshacer Mov", command=self.undo_move)
        undo_button.grid(row=3, column=0, pady=10)

        redo_button = tk.Button(frame, text="Rehacer Mov", command=self.redo_move)
        redo_button.grid(row=3, column=1, pady=10)

        # Botón para sugerir movimientos
        suggest_button = tk.Button(frame, text="Sugerir Movimientos", command=self.suggest_move_for_entry)
        suggest_button.grid(row=4, column=0, columnspan=6, pady=10)

        # Widget Text para mostrar la tabla de Sudoku
        self.board_text = tk.Text(self.master, height=12, width=22, font=("Courier New", 12), bg="lightgrey")
        self.board_text.pack(pady=10)

    def load_configuration_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                self.game.load_initial_configuration(file_path)
                self.display_board()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la configuración: {e}")

    def make_move(self):
        try:
            row = int(self.row_entry.get())
            col = int(self.col_entry.get())
            number = int(self.num_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor ingresa números válidos.")
            return

        if not (1 <= row <= 9 and 1 <= col <= 9 and 1 <= number <= 9):
            messagebox.showerror("Error", "Por favor ingrese un número entre 1 y 9.")
            return

        if self.game.make_move(row - 1, col - 1, number):
            self.display_board()

    def undo_move(self):
        self.game.undo_move()
        self.display_board()

    def redo_move(self):
        self.game.redo_move()
        self.display_board()

    def suggest_move_for_entry(self):
            try:
                row = int(self.row_entry.get())
                col = int(self.col_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa números válidos para fila y columna.")
                return

            if not (1 <= row <= 9 and 1 <= col <= 9):
                messagebox.showerror("Error", "Por favor ingrese números entre 1 y 9 para fila y columna.")
                return

            current_number = self.game.board[row - 1][col - 1]

            if current_number != 0:
                messagebox.showerror("Error", "Esa casilla ya tiene un número.")
                return

            suggestions = self.game.suggest_move(row - 1, col - 1)

            if suggestions != ['Game Over']:
                messagebox.showinfo("Sugerencias", f"Sugerencias para la casilla ({row}, {col}): {suggestions}")
            else:
                messagebox.showinfo("Fin del Juego", "¡El juego ha terminado!")

    def display_board(self):
        # Limpiamos el contenido actual en el widget Text
        self.board_text.delete("1.0", tk.END)
        # Insertamos la tabla de Sudoku en el widget Text
        for index, row in enumerate(self.game.board):
            row_text = " ".join(map(str, row))
            count = 0
            modified_row_text = ""
            for i, char in enumerate(row_text):
                if char == ' ':
                    count += 1
                    if count % 3 == 0:
                        modified_row_text += ' | '
                    else:
                        modified_row_text += char
                else:
                    modified_row_text += char
            
            self.board_text.insert(tk.END, modified_row_text + "\n")
            
            # Reemplazar cada tercera línea por "="
            if index + 1  == 3 or index + 1  == 6:  # Si es la tercera línea (empezando desde 1)
                self.board_text.insert(tk.END, "----------------------\n")
            else:
                self.board_text.insert(tk.END, "")

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()