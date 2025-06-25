import tkinter as tk
import random
from GameOfLife import *

class GameOfLifeGUI:
    CELL_SIZE = 25
    ALIVE_COLOR = 'gold'
    DEAD_COLOR = 'slategray'
    # grid = GameOfLife.__init__("input.txt")


    def __init__(self, input_file, output_file, delay=200):
        self.nexus = GameOfLife(input_file)
        rows = len(self.nexus.grid)
        cols = len(self.nexus.grid[0])
        # self.grid = self.nexus.grid.copy()
        self.delay = delay
        self.running = False
        self.output_file = output_file
        self.game = GameOfLife(input_file)
        self.generation = 0

        self.root = tk.Tk()
        self.root.title("Game of Life")
        self.root.configure(bg='slategray')
        try:
            self.root.iconbitmap("glider.ico")
        except:
            pass

        self.canvas = tk.Canvas(self.root,
                                width=self.nexus.cols * self.CELL_SIZE,
                                height=self.nexus.rows * self.CELL_SIZE,
                                highlightthickness=1,
                                highlightbackground="gold")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_click)

        self.button_frame = tk.Frame(self.root, bg='slategray')
        self.button_frame.pack(pady=5)

        self.start_button = tk.Button(self.button_frame, text="Start",
                                      foreground='gold', bg='slategray',
                                      font=('Helvetica 14 bold italic'),
                                      height=2, width=10,
                                      command=self.start)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(self.button_frame, text="Stop",
                                     foreground='gold', bg='slategray',
                                     font=('Helvetica 14 bold italic'),
                                     height=2, width=10,
                                     command=self.stop,
                                     state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        self.clear_button = tk.Button(self.button_frame, text="Clear",
                                      foreground='gold', bg='slategray',
                                      font=('Helvetica 14 bold italic'),
                                      height=2, width=10,
                                      command=self.clear_grid)
        self.clear_button.grid(row=0, column=2, padx=5)

        self.random_button = tk.Button(self.button_frame, text="Randomize",
                                       foreground='gold', bg='slategray',
                                       font=('Helvetica 14 bold italic'),
                                       height=2, width=10,
                                       command=self.randomize_grid)
        self.random_button.grid(row=0, column=3, padx=5)

        self.gen_label = tk.Label(self.root, text="Generation: 0",
                                  font=("Helvetica", 12), fg="gold",
                                  bg="slategray")
        self.gen_label.pack(pady=2)

        self.draw_grid()
        self.root.mainloop()

    def draw_grid(self):
        self.canvas.delete('all')
        for i in range(self.nexus.rows):
            for j in range(self.nexus.cols):
                color = self.ALIVE_COLOR if self.nexus.grid[i][j] else self.DEAD_COLOR
                x0 = j * self.CELL_SIZE
                y0 = i * self.CELL_SIZE
                x1 = x0 + self.CELL_SIZE
                y1 = y0 + self.CELL_SIZE
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline='dimgrey')

    def on_click(self, event):
        col = event.x // self.CELL_SIZE
        row = event.y // self.CELL_SIZE
        self.nexus.toggle_cell(row, col)
        self.draw_grid()

    def start(self):
        if not self.running:
            self.running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.update_loop()

    def stop(self):
        if self.running:
            self.running = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.nexus.save_grid_to_file(self.output_file)

    def clear_grid(self):
        self.running = False
        self.nexus.clear()
        self.generation = 0
        self.gen_label.config(text=f"Generation: {self.generation}")
        self.draw_grid()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def randomize_grid(self):
        self.running = False
        self.nexus.randomize()
        self.generation = 0
        self.gen_label.config(text=f"Generation: {self.generation}")
        self.draw_grid()
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_loop(self):
        if not self.running:
            return
        self.nexus.update()
        self.generation += 1
        self.gen_label.config(text=f"Generation: {self.generation}")
        self.draw_grid()
        self.root.after(self.delay, self.update_loop)


if __name__ == "__main__":
    GameOfLifeGUI('input.txt', 'output.txt', delay=545)