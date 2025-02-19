import tkinter  # tk-interface (graphical user interface library)

# ------------------- Helper Functions ------------------- #

def update_status_label(text, color="white"):
    """Update the status label with the given text and color."""
    label.config(text=text, foreground=color)


def set_tile(row, column):
    global current_player, game_over

    if board[row][column]["text"] != "" or game_over:
        # Spot is already taken or game is over
        return

    # Mark the board with the current player's symbol
    board[row][column]["text"] = current_player

    # Check for a winner after the move
    check_winner()

    # Switch the current player if the game is still ongoing
    if not game_over:
        current_player = playerX if current_player == playerY else playerY
        update_status_label(f"{current_player}'s turn")


def check_winner():
    """Check if there is a winner or the game ends in a tie."""
    global game_over

    # Check rows, columns, and diagonals for a winner
    for row in range(3):
        if board[row][0]["text"] == board[row][1]["text"] == board[row][2]["text"] and board[row][0]["text"] != "":
            highlight_winner([(row, 0), (row, 1), (row, 2)])
            return

    for col in range(3):
        if board[0][col]["text"] == board[1][col]["text"] == board[2][col]["text"] and board[0][col]["text"] != "":
            highlight_winner([(0, col), (1, col), (2, col)])
            return

    if board[0][0]["text"] == board[1][1]["text"] == board[2][2]["text"] and board[0][0]["text"] != "":
        highlight_winner([(0, 0), (1, 1), (2, 2)])
        return

    if board[0][2]["text"] == board[1][1]["text"] == board[2][0]["text"] and board[0][2]["text"] != "":
        highlight_winner([(0, 2), (1, 1), (2, 0)])
        return

    # Check for a tie (if all tiles are filled and no winner)
    if all(board[row][col]["text"] != "" for row in range(3) for col in range(3)):
        update_status_label("It's a tie!", color="orange")
        game_over = True


def highlight_winner(winning_tiles):
    """Highlight the winning tiles and display the winner message."""
    global game_over

    winner = board[winning_tiles[0][0]][winning_tiles[0][1]]["text"]
    update_status_label(f"{winner} is the winner!", color=color_yellow)

    for row, col in winning_tiles:
        board[row][col].config(foreground=color_yellow, background=color_light_grey)

    game_over = True


def new_game():
    """Reset the game board for a new game."""
    global current_player, game_over, turns

    current_player = playerX
    game_over = False
    update_status_label(f"{current_player}'s turn")

    for row in range(3):
        for col in range(3):
            board[row][col].config(text="", foreground=color_blue, background=color_grey)


# ------------------- Game Setup ------------------- #

# Players
playerX = "X"
playerY = "O"
current_player = playerX

# Colors
color_blue = "#4584b6"
color_yellow = "#ffde57"
color_grey = "#343434"
color_light_grey = "#646464"

# Game state
game_over = False

# Create a 3x3 board
board = [[None for _ in range(3)] for _ in range(3)]

# ------------------- GUI Setup ------------------- #

# Window setup
window = tkinter.Tk()
window.title("TIC TAC TOE")
window.resizable(False, False)

# Frame to hold the board and status label
frame = tkinter.Frame(window)

# Status label
label = tkinter.Label(
    frame, text=f"{current_player}'s turn", font=("Consolas", 20), background=color_grey, foreground="white"
)
label.grid(row=0, column=0, columnspan=3, sticky="we")

# Create the 3x3 grid of buttons
for row in range(3):
    for col in range(3):
        board[row][col] = tkinter.Button(
            frame,
            text="",
            font=("Consolas", 50, "bold"),
            background=color_grey,
            foreground=color_blue,
            width=4,
            height=1,
            command=lambda row=row, col=col: set_tile(row, col),
        )
        board[row][col].grid(row=row + 1, column=col)

# New game button
restart_button = tkinter.Button(
    frame, text="Restart", font=("Consolas", 20), background=color_grey, foreground="white", command=new_game
)
restart_button.grid(row=4, column=0, columnspan=3, sticky="we")

frame.pack()

# Center the window on the screen
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

window_x = int((screen_width / 2) - (window_width / 2))
window_y = int((screen_height / 2) - (window_height / 2))

window.geometry(f"{window_width}x{window_height}+{window_x}+{window_y}")

# Start the game loop
window.mainloop()