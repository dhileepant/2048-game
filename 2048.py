import tkinter as tk
import random
import copy
import winsound

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048 Game")
        self.board = [[0]*4 for _ in range(4)]
        self.previous_board = None
        self.score = 0
        self.previous_score = 0

        self.colors = {
            0: ("#cdc1b4", "#776e65"),
            2: ("#eee4da", "#776e65"),
            4: ("#ede0c8", "#776e65"),
            8: ("#f2b179", "#f9f6f2"),
            16: ("#f59563", "#f9f6f2"),
            32: ("#f67c5f", "#f9f6f2"),
            64: ("#f65e3b", "#f9f6f2"),
            128: ("#edcf72", "#f9f6f2"),
            256: ("#edcc61", "#f9f6f2"),
            512: ("#edc850", "#f9f6f2"),
            1024: ("#edc53f", "#f9f6f2"),
            2048: ("#edc22e", "#f9f6f2")
        }

        self.setup_ui()
        self.add_tile()
        self.add_tile()
        self.update_gui()
        self.root.bind("<Key>", self.key_handler)

    def setup_ui(self):
        self.frame = tk.Frame(self.root, bg="#bbada0")
        self.frame.grid(padx=10, pady=10)

        self.tiles = [[tk.Label(self.frame, text="", width=4, height=2, font=("Arial", 24, "bold"), bg="#cdc1b4") for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].grid(row=i, column=j, padx=5, pady=5)

        self.score_label = tk.Label(self.root, text=f"Score: {self.score}", font=("Arial", 16))
        self.score_label.grid(row=1, pady=5)

        self.undo_button = tk.Button(self.root, text="Undo", command=self.undo, font=("Arial", 12))
        self.undo_button.grid(row=2, pady=5)

    def add_tile(self):
        empty = [(i, j) for i in range(4) for j in range(4) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def update_gui(self):
        for i in range(4):
            for j in range(4):
                value = self.board[i][j]
                bg_color, fg_color = self.colors.get(value, ("#3c3a32", "#f9f6f2"))
                self.tiles[i][j].config(text=str(value) if value != 0 else "", bg=bg_color, fg=fg_color)
        self.score_label.config(text=f"Score: {self.score}")

    def key_handler(self, event):
        key = event.keysym
        direction = None
        if key == 'Up':
            direction = 'up'
        elif key == 'Down':
            direction = 'down'
        elif key == 'Left':
            direction = 'left'
        elif key == 'Right':
            direction = 'right'

        if direction:
            self.previous_board = copy.deepcopy(self.board)
            self.previous_score = self.score
            moved = self.move(direction)
            if moved:
                winsound.MessageBeep()  # Basic sound effect
                self.add_tile()
                self.update_gui()
                if self.game_over():
                    self.game_over_popup()

    def move(self, direction):
        moved = False
        for i in range(4):
            if direction in ['left', 'right']:
                row = self.board[i][:]
                if direction == 'right':
                    row.reverse()
                merged_row, gained_score = self.merge(row)
                if direction == 'right':
                    merged_row.reverse()
                if self.board[i] != merged_row:
                    self.board[i] = merged_row
                    self.score += gained_score
                    moved = True
            else:
                col = [self.board[x][i] for x in range(4)]
                if direction == 'down':
                    col.reverse()
                merged_col, gained_score = self.merge(col)
                if direction == 'down':
                    merged_col.reverse()
                if [self.board[x][i] for x in range(4)] != merged_col:
                    for x in range(4):
                        self.board[x][i] = merged_col[x]
                    self.score += gained_score
                    moved = True
        return moved

    def merge(self, tiles):
        new_tiles = [i for i in tiles if i != 0]
        score = 0
        i = 0
        while i < len(new_tiles)-1:
            if new_tiles[i] == new_tiles[i+1]:
                new_tiles[i] *= 2
                score += new_tiles[i]
                del new_tiles[i+1]
                new_tiles.append(0)
            i += 1
        return new_tiles + [0]*(4 - len(new_tiles)), score

    def game_over(self):
        for i in range(4):
            for j in range(4):
                if self.board[i][j] == 0:
                    return False
                if j < 3 and self.board[i][j] == self.board[i][j+1]:
                    return False
                if i < 3 and self.board[i][j] == self.board[i+1][j]:
                    return False
        return True

    def game_over_popup(self):
        popup = tk.Toplevel()
        popup.title("Game Over")
        tk.Label(popup, text="Game Over!", font=("Arial", 16)).pack(padx=10, pady=10)
        tk.Button(popup, text="OK", command=popup.destroy).pack(pady=5)

    def undo(self):
        if self.previous_board:
            self.board = self.previous_board
            self.score = self.previous_score
            self.update_gui()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
