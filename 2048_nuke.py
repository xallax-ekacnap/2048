import random
import sys
import streamlit as st

from streamlit_shortcuts import add_keyboard_shortcuts
from streamlit_extras.stylable_container import stylable_container
    
def add_new_value(board, r=None):
    spots = []
    for i, row in enumerate(board):
        for j, item in enumerate(row):
            if item == 0:
                spots.append((i, j))
    if len(spots) == 0:
        if is_game_over():
            game_over()
        return board
    index = random.choice(spots)
    if random.randint(0, 9) == 0:
        board[index[0]][index[1]] = Cell(4)
    else:
        board[index[0]][index[1]] = Cell(2)
    return board
        

# check, rest = row[0], row[1:]

def move_row_left(row):
    for i in range(1, len(row)):
        for j in reversed(range(i)):
            row[j], row[j + 1] = check_pair(row[j], row[j + 1])
    for item in row:
            item.combined = False
    return row


def move_board_left(board):
    for i in range(len(board)):
        board[i] = move_row_left(board[i])
    return board

def move_board_right(board):
    for i, row in enumerate(board):
        board[i] = move_row_left(row[::-1])[::-1]
    return board


def rotate_board(board):
    new_board = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            new_board[i][j] = board[j][i]
    return new_board

def unrotate_board(board):
    new_board = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            new_board[j][i] = board[i][j]
    return new_board


def move_board_up(board):
    return unrotate_board(move_board_left(rotate_board(board)))

def move_board_down(board):
    return unrotate_board(move_board_right(rotate_board(board)))

def check_pair(a, b):
    if a == b and not a.combined and not b.combined and a != 0: #combining
        new_value = a * 2
        st.session_state.score += new_value
        return Cell(new_value, True), Cell(0) 
    if a == 0 and b != 0: #moving left
        return b, Cell(0)
    return a, b
            

# def display(board):
#     for i in range(4):
#         for j in range(4):
#             print(board[i][j], end=' ')
#         print()
#     print()

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

def decide_direction(name):
    # display(st.session_state.board)
    
    if name == 'Left':
        st.session_state.board = move_board_left(st.session_state.board)
    if name == 'Right':
        st.session_state.board = move_board_right(st.session_state.board)
    if name == 'Up':
        st.session_state.board = move_board_up(st.session_state.board)
    if name == 'Down':
        st.session_state.board = move_board_down(st.session_state.board)
    
    # display(st.session_state.board)
    for i in range(st.session_state.new_value):
        st.session_state.board = add_new_value(st.session_state.board)
    # display(st.session_state.board)

def reinitialize_board():
    board = [[Cell(0) for i in range(st.session_state.edge)] for j in range(st.session_state.edge)]
    for i in range(st.session_state.new_value):
        board = add_new_value(board)
    st.session_state.score = 0
    st.session_state.board = board

def is_game_over():
    print("is game over")
    print(st.session_state.board)
    print(rotate_board(st.session_state.board))
    for row in st.session_state.board:
        for i, val in enumerate(row[1:], 1):
            print(i, val, row[i-1])
            if val == row[i - 1]:
                print("false1")
                return False
    
    for row in rotate_board(st.session_state.board):
        for i, val in enumerate(row[1:], 1):
            if val == row[i - 1]:
                print("fals2")
                return False
    print("true")
    return True

            

def game_over():
    print("game over")
    game_over = st.sidebar.container(border=False)
    with game_over:
        st.markdown("<h1 style='text-align: center;'>Game Over</h1>", unsafe_allow_html=True)
        st.button("Restart", on_click=reinitialize_board)
    del game_over



# board = [[Cell(0) for i in range(4)] for j in range(4)]


board_cont = st.container(border=False)

if "score" not in st.session_state:
    st.session_state.score = 0

with st.container():
    st.markdown('<div class="board-container"></div>', unsafe_allow_html=True)



col1, col2, col3, col4 = st.columns(4)
names = ['Left', 'Right','Up', 'Down']
arrows = ['←', '→', '↑','↓']

# for i, col in enumerate([col1, col2, col3, col4]):
#     with col:
#         st.button(label=arrows[i], key=names[i], on_click=decide_direction(names[i]))

with st.sidebar:

    st.markdown(f"<h1 style='text-align: center;'>Score: {st.session_state.score}</h1>", unsafe_allow_html=True)

    st.number_input(label="Edge", key="edge", value=4, min_value=3, max_value=16, step=1, on_change=reinitialize_board)
    st.number_input(label="New Values Each Move", key='new_value', value=st.session_state.edge // 4, min_value=1, max_value=st.session_state.edge**2)

direction_dict = {'A': "←", 'D': "→", 'W': "↑", 'S': "↓"}

for i, col in enumerate([col1, col2, col3, col4]):
    with col:
        if st.button(label=arrows[i] + "\t" + {direct: key for key, direct in direction_dict.items()}[arrows[i]], key=names[i]):
            decide_direction(names[i])

add_keyboard_shortcuts(direction_dict)

#colors in hex values on a gradient
colors = {
0: "#b3d1e6",  # Light blue
    2: "#9fc6e0",  # Soft blue
    4: "#8bbbd9",  # Cool blue
    8: "#77b0d2",  # Aqua blue
    16: "#63a5cb", # Cyan
    32: "#4f99c4", # Blue-green
    64: "#3b8ebd", # Teal
    128: "#2a84a3",# Deep teal
    256: "#1b7990",# Sea green
    512: "#0e6f7e",# Forest green
    1024: "#066566",# Dark teal
    2048: "#00514d" # Deep green
}



if "board" not in st.session_state:
    reinitialize_board()

cols = board_cont.columns(st.session_state.edge, gap="small")

for i, col in enumerate(cols):
    with col:
        for j in range(st.session_state.edge):
            var = st.session_state.board[j][i]
            color = colors[var]
            st.write(
                f"""
                <div style="
                    height: {680 / st.session_state.edge}px; 
                    width: {680 / st.session_state.edge}px; 
                    background-color: {color}; 
                    display: flex; 
                    align-items: center; 
                    justify-content: center; 
                    border-radius: 10px;
                    margin: 5px;
                    ">
                    <span style="color: white; font-size: 2em;">{str(var) if var != 0 else ''}</span>
                </div>
                """,
                unsafe_allow_html=True
            )