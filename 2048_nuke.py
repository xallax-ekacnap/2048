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

def move_board_up(board):
    new_board = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            new_board[i][j] = board[j][i]
    new_board = move_board_left(new_board)
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[j][i] = new_board[i][j]
    return board

def move_board_down(board):
    new_board = [[0 for _ in range(len(board[0]))] for _ in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[0])):
            new_board[i][j] = board[j][i]
    new_board = move_board_right(new_board)
    for i in range(len(board)):
        for j in range(len(board[0])):
            board[j][i] = new_board[i][j]
    return board
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
    print("before movement")
    # display(st.session_state.board)
    
    if name == 'Left':
        st.session_state.board = move_board_left(st.session_state.board)
    if name == 'Right':
        st.session_state.board = move_board_right(st.session_state.board)
    if name == 'Up':
        st.session_state.board = move_board_up(st.session_state.board)
    if name == 'Down':
        st.session_state.board = move_board_down(st.session_state.board)
    
    print("after movement")
    # display(st.session_state.board)
    st.session_state.board = add_new_value(st.session_state.board)
    
    print("after adding new value")
    # display(st.session_state.board)


# board = [[Cell(0) for i in range(4)] for j in range(4)]

edge_num = 4


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

for i, col in enumerate([col1, col2, col3, col4]):
    with col:
        if st.button(label=arrows[i], key=names[i]):
            decide_direction(names[i])

add_keyboard_shortcuts({
    'A': "←",
    'D': "→",
    'W': "↑",
    'S': "↓"
})

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
    board = [[Cell(0) for i in range(edge_num)] for j in range(edge_num)]
    board = add_new_value(board)
    st.session_state.board = board

cols = board_cont.columns(edge_num, gap="small")
# for i, col in enumerate(cols):
#     with col:
#         for j in range(4):
#             var = st.session_state.board[j][i]
#             with stylable_container(
#                 key="box",
#                 css_styles=" {background-color: grey; max-width: 100px;}"
#                 ):
#                 box = st.container(height=100,border=True)
            
#             box.write(f'<span style="color: {colors[var]}; font-size: 2em;">{str(var)}</span>', unsafe_allow_html=True)
for i, col in enumerate(cols):
    with col:
        for j in range(edge_num):
            var = st.session_state.board[j][i]
            color = colors[var]
            st.write(
                f"""
                <div style="
                    height: {680 / edge_num}px; 
                    width: {680 / edge_num}px; 
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