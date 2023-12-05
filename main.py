from Clases.sudoku_game import SudokuGame
from Clases.sudoku_gui import SudokuGUI
import tkinter as tk

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuGUI(root)
    root.mainloop()