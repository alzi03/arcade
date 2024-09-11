import tkinter as tk
import random
from collections import deque
from tkinter import messagebox

class Cell:
    def __init__(self, root, row, col, game):
        self.root = root
        self.row = row
        self.col = col
        self.game = game
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

        # Creating the button (representing the cell)
        self.button = tk.Button(root, width=3, height=1, font=("Arial", 12), command=self.reveal)
        self.button.bind("<Button-3>", self.flag)
        self.button.grid(row=row, column=col, sticky="nsew")

    def set_mine(self):
        """Mark this cell as a mine."""
        self.is_mine = True

    def reveal(self):
        if self.is_revealed or self.is_flagged or self.game.game_over:
            return

        self.is_revealed = True

        if self.is_mine:
            self.button.config(text="*", bg="red", fg="black")
            self.game.game_over = True
            self.game.show_mines()
            messagebox.showinfo("Game Over", "You clicked on a mine!")
        else:
            self.button.config(text=str(self.adjacent_mines) if self.adjacent_mines > 0 else "", 
                           bg="black", fg="black", disabledforeground="black")  # Set disabledforeground to black
            self.button.config(state="disabled")

            if self.adjacent_mines == 0:
                self.game.reveal_adjacent_cells(self.row, self.col)

    def flag(self, event):
        """Flags or unflags the cell."""
        if not self.is_revealed:
            if not self.is_flagged:
                self.button.config(text="F", fg="red")
                self.is_flagged = True
            else:
                self.button.config(text="")
                self.is_flagged = False
                
                
class Minesweeper:
    def __init__(self, root, size=10, mines=10):
        self.root = root
        self.size = size  # Square board
        self.mines = mines
        self.game_over = False
        self.cells = {}
        self.first_click = True  # Flag to handle the first click

        # Set up the game board
        self.create_board()
        self.place_mines()
        self.calculate_numbers()

    def create_board(self):
        """Creates the board of cells."""
        for r in range(self.size):
            for c in range(self.size):
                self.cells[(r, c)] = Cell(self.root, r, c, self)
                self.root.grid_rowconfigure(r, weight=1)  # Ensure the grid rows/columns are evenly spaced
                self.root.grid_columnconfigure(c, weight=1)

    def place_mines(self, exclude_cells=None):
        """Randomly place mines on the board, excluding specified cells."""
        exclude_cells = exclude_cells or set()
        mines_placed = 0
        while mines_placed < self.mines:
            r = random.randint(0, self.size - 1)
            c = random.randint(0, self.size - 1)
            if not self.cells[(r, c)].is_mine and (r, c) not in exclude_cells:
                self.cells[(r, c)].set_mine()
                mines_placed += 1

    def calculate_numbers(self):
        """Calculate the number of adjacent mines for each cell."""
        for r in range(self.size):
            for c in range(self.size):
                if self.cells[(r, c)].is_mine:
                    continue
                self.cells[(r, c)].adjacent_mines = self.count_adjacent_mines(r, c)

    def count_adjacent_mines(self, r, c):
        """Counts the number of adjacent mines around a cell."""
        count = 0
        for i in range(max(0, r - 1), min(r + 2, self.size)):
            for j in range(max(0, c - 1), min(c + 2, self.size)):
                if self.cells[(i, j)].is_mine:
                    count += 1
        return count

    def reveal_adjacent_cells(self, r, c):
        """Reveals all adjacent cells if they are empty (0 adjacent mines)."""
        queue = deque([(r, c)])  # Use a deque as a queue
        while queue:
            curr_r, curr_c = queue.popleft()
            cell = self.cells[(curr_r, curr_c)]
            if cell.is_revealed or cell.is_flagged:
                continue
            cell.reveal()
            if cell.adjacent_mines == 0:
                for i in range(max(0, curr_r - 1), min(curr_r + 2, self.size)):
                    for j in range(max(0, curr_c - 1), min(curr_c + 2, self.size)):
                        if (i, j) != (curr_r, curr_c):
                            queue.append((i, j))

    def show_mines(self):
        """Reveal all mines when the game is over."""
        for cell in self.cells.values():
            if cell.is_mine:
                cell.button.config(text="*", bg="red", fg="white")
                
    def handle_first_click(self, r, c):
        """Reveals a few adjacent cells around the first clicked cell, then places mines."""
        # Define the cells to reveal initially
        cells_to_reveal = [(r, c)]

        # Add cells in the immediate vicinity
        for i in range(max(0, r - 1), min(r + 2, self.size)):
            for j in range(max(0, c - 1), min(c + 2, self.size)):
                if (i, j) != (r, c):
                    cells_to_reveal.append((i, j))

        # Ensure we have a fixed number of cells to reveal (e.g., 10)
        cells_to_reveal = cells_to_reveal[:10]

        # Place mines after revealing these cells
        self.place_mines(exclude_cells=set(cells_to_reveal))

        # Calculate numbers for all cells
        self.calculate_numbers()

        # Reveal the cells
        for cell_coords in cells_to_reveal:
            self.cells[cell_coords].reveal()

        # Ensure the revealed area has a border with values
        self.reveal_border_cells(cells_to_reveal)

    def reveal_border_cells(self, revealed_cells):
        """Ensure the border around the revealed area has numbers."""
        border_cells = set()
        for r, c in revealed_cells:
            for i in range(max(0, r - 1), min(r + 2, self.size)):
                for j in range(max(0, c - 1), min(c + 2, self.size)):
                    if (i, j) not in revealed_cells and (i, j) not in border_cells:
                        border_cells.add((i, j))

        # Reveal the border cells
        for cell_coords in border_cells:
            self.cells[cell_coords].reveal()