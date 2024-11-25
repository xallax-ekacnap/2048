import random
import sys

try:
    import tty, termios
except ImportError:
    # Probably Windows.
    try:
        import msvcrt
    except ImportError:
        # FIXME what to do on other platforms?
        # Just give up here.
        raise ImportError('getch not available')
    else:
        getch = msvcrt.getch
else:
    def getch():
        """getch() -> key character

        Read a single keypress from stdin and return the resulting character. 
        Nothing is echoed to the console. This call will block if a keypress 
        is not already available, but will not wait for Enter to be pressed. 

        If the pressed key was a modifier key, nothing will be detected; if
        it were a special function key, it may return the first character of
        of an escape sequence, leaving additional characters in the buffer.
        """
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
    
def add_new_value(board, r=None):
    if not r:
        r = random.randint(0, 9)
    if r == 0:
        index = (random.randint(0, 3), random.randint(0, 3))
        if board[index[0]][index[1]] == 0:
            board[index[0]][index[1]] = Cell(4)
        else:
            add_new_value(board, r)
    else:
        index = (random.randint(0, 3), random.randint(0, 3))
        if board[index[0]][index[1]] == 0:
            board[index[0]][index[1]] = Cell(2)
        else:
            add_new_value(board, r)

# check, rest = row[0], row[1:]

def move_row_left(row):
    for i in range(1, 4):
        for j in reversed(range(i)):
            row[j], row[j + 1] = check_pair(row[j], row[j + 1])
    for item in row:
            item.combined = False
    return row


def move_board_left(board):
    for i in range(4):
        board[i] = move_row_left(board[i])
    return board

def move_board_right(board):
    for i, row in enumerate(board):
        board[i] = move_row_left(row[::-1])[::-1]
    return board

def move_board_up(board):
    new_board = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            new_board[i].append(board[j][i])
    new_board = move_board_left(new_board)
    for i in range(4):
        for j in range(4):
            board[j][i] = new_board[i][j]
    return board

def move_board_down(board):
    new_board = [[], [], [], []]
    for i in range(4):
        for j in range(4):
            new_board[i].append(board[j][i])
    new_board = move_board_right(new_board)
    for i in range(4):
        for j in range(4):
            board[j][i] = new_board[i][j]
    return board
def check_pair(a, b):
    if a == b and not a.combined and not b.combined and a != 0: #combining
        return Cell(a * 2, True), Cell(0) 
    if a == 0 and b != 0: #moving left
        return b, Cell(0)
    return a, b
            

def display(board):
    for i in range(4):
        for j in range(4):
            print(board[i][j], end=' ')
        print()
    print()

class Cell(int):
    def __new__(cls, value, *args, **kwargs):
        # Ensure the value is converted to an integer
        return super().__new__(cls, value)

    def __init__(self, value, combined=False):
        # You can add additional initialization if needed
        self.value = int(value)
        self.combined = combined

    def __str__(self):
        return f"{self.value}"


# board = [[Cell(0) for i in range(4)] for j in range(4)]

board = [[Cell(0), Cell(2), Cell(2), Cell(4)], [Cell(0), Cell(2), Cell(2), Cell(0)], [Cell(2), Cell(2), Cell(2), Cell(4)], [Cell(8), Cell(2), Cell(4), Cell(4)]]

while True:
    keyboard = getch()
    if keyboard == 'w':
        board = move_board_up(board)
    elif keyboard == 'a':
        board = move_board_left(board)
    elif keyboard == 's':
        board = move_board_down(board)
    elif keyboard == 'd':
        board = move_board_right(board)
    elif keyboard == 'q':
        break

    add_new_value(board)
    display(board)

# assert move_row_left([0, 0, 0, 0]) == [0, 0, 0, 0]
# assert move_row_left([0, 0, 0, 2]) == [2, 0, 0, 0]
# assert move_row_left([2, 2, 4, 0]) == [4, 4, 0, 0]
# assert move_row_left([8, 4, 2, 2]) == [8, 4, 4, 0]
# assert move_row_left([2, 2, 2, 2]) == [4, 4, 0, 0]