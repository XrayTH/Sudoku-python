from Clases.sudoku_game import SudokuGame
from Clases.linkedlist import LinkedList
from Clases.stack import Stack
from tkinter import filedialog, messagebox
import tkinter as tk

class SudokuGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Sudoku")
        self.history_window = None  # Ventana para el historial de jugadas

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

        # Botón para mostrar el historial de jugadas
        history_button = tk.Button(frame, text="Historial de Jugadas", command=self.show_history)
        history_button.grid(row=5, column=0, columnspan=6, pady=10)

        # Widget Text para mostrar la tabla de Sudoku
        self.board_text = tk.Text(self.master, height=12, width=22, font=("Courier New", 12), bg="lightgrey")
        self.board_text.pack(pady=10)
        self.board_text.bind("<Key>", lambda e: "break")  # Deshabilita la entrada de teclado

    def load_configuration_from_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            try:
                # Cerrar la ventana del historial si está abierta
                if self.history_window and self.history_window.winfo_exists():
                    self.history_window.destroy()

                # Limpiar historial al cargar una nueva configuración
                self.game.history = Stack()
                self.game.redo_moves = Stack()
                self.game.full_history = LinkedList()

                self.game.load_initial_configuration(file_path)
                self.display_board()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cargar la configuración: {e}")

    def update_history(self):
        if self.history_window and self.history_window.winfo_exists():
            self.show_history()

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
            self.update_history()
            if(self.game.is_game_over()):
                messagebox.showinfo("Fin del Juego", "¡El juego ha terminado!")

    def undo_move(self):
        self.game.undo_move()
        self.display_board()
        self.update_history()

    def redo_move(self):
        self.game.redo_move()
        self.display_board()
        self.update_history()

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
            if suggestions:
                messagebox.showinfo("Sugerencias", f"Sugerencias para la casilla ({row}, {col}): {suggestions}")
            else:
                messagebox.showinfo("Sin sugerencias", "No hay sugerencias para esa casilla.")
        else:
            messagebox.showinfo("Fin del Juego", "¡El juego ha terminado!")

    def show_history(self):
        if self.history_window is None or not self.history_window.winfo_exists():
            self.history_window = tk.Toplevel(self.master)
            self.history_window.title("Historial de Jugadas")
            self.history_text = tk.Text(self.history_window, height=20, width=50, font=("Courier New", 12), bg="lightgrey")
            self.history_text.pack(pady=10)
            self.history_text.bind("<Key>", lambda e: "break")  # Deshabilita la entrada de teclado
            
        else:
            self.history_text.delete('1.0', tk.END)

        for move in self.game.full_history:
            if len(move) == 4:
                move_type, prev_board, (row, col), number = move
                if move_type == 'undo':
                    self.history_text.insert(tk.END, f"Jugada deshecha: ({row + 1}, {col + 1}) = {number}\n")
                elif move_type == 'redo':
                    self.history_text.insert(tk.END, f"Jugada rehecha: ({row + 1}, {col + 1}) = {number}\n")
                else:
                    self.history_text.insert(tk.END, f"Jugada hecha: ({row + 1}, {col + 1}) = {number}\n")
            else:
                prev_board, (row, col), number = move
                self.history_text.insert(tk.END, f"Jugada hecha: ({row + 1}, {col + 1}) = {number}\n")

        self.history_window.lift()

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
