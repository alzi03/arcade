import tkinter as tk
from minesweeper_game import Minesweeper  # Make sure the file name matches

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Minesweeper")

    # Initialize the Minesweeper game with a 10x10 grid and 15 mines
    game = Minesweeper(root, size=10, mines=15)

    # Force the window to be square
    for i in range(10):
        root.grid_rowconfigure(i, minsize=50)
        root.grid_columnconfigure(i, minsize=50)

    # Start the Tkinter main loop
    root.mainloop()
