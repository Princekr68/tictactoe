import streamlit as st
from game_logic import (
    new_board,
    check_winner,
    winning_line,
    best_move,
    HUMAN,
    AI,
    EMPTY
)

st.set_page_config(page_title="Neon Tic-Tac-Toe", page_icon="🎮", layout="centered")

if st.query_params:
    st.query_params.clear()

# -----------------------------
# Session state
# -----------------------------
if "board" not in st.session_state:
    st.session_state.board = new_board()
if "game_over" not in st.session_state:
    st.session_state.game_over = False
if "result" not in st.session_state:
    st.session_state.result = None
if "you_score" not in st.session_state:
    st.session_state.you_score = 0
if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0
if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0


# -----------------------------
# Game functions
# -----------------------------
def restart_game():
    st.session_state.board = new_board()
    st.session_state.game_over = False
    st.session_state.result = None


def reset_score():
    st.session_state.you_score = 0
    st.session_state.ai_score = 0
    st.session_state.draw_score = 0
    restart_game()


def finish_game(result):
    st.session_state.game_over = True
    st.session_state.result = result
    if result == HUMAN:
        st.session_state.you_score += 1
    elif result == AI:
        st.session_state.ai_score += 1
    elif result == "Draw":
        st.session_state.draw_score += 1


def play_move(index):
    if st.session_state.game_over:
        return
    board = st.session_state.board
    if board[index] != EMPTY:
        return

    # Human move
    board[index] = HUMAN
    result = check_winner(board)
    if result:
        finish_game(result)
        return

    # AI move
    ai_index = best_move(board)
    if ai_index is not None:
        board[ai_index] = AI
    result = check_winner(board)
    if result:
        finish_game(result)


# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
<style>
.stApp {
    background: radial-gradient(circle at 50% 5%, #35105f 0%, #130622 45%, #05020b 100%);
    color: white;
}
.block-container { max-width: 380px; padding-top: 1rem; padding-bottom: 0.5rem; }
.block-container > [data-testid="stVerticalBlock"] { gap: 0.5rem; }
header { visibility: hidden; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

/* Title */
.title {
    text-align: center; font-size: 28px; font-weight: 900; letter-spacing: 3px; color: white;
    text-shadow: 0 0 8px white, 0 0 18px #8b3dff, 0 0 35px #8b3dff;
}
.subtitle { text-align: center; color: #bcaed2; font-size: 10px; letter-spacing: 2px; margin: 2px 0 8px 0; }

/* Score */
.score { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-bottom: 8px; }
.score-box {
    text-align: center; padding: 5px; border-radius: 12px;
    background: rgba(17, 7, 32, 0.9); border: 1px solid #583473;
}
.score-label { color: #9585a8; font-size: 9px; letter-spacing: 2px; }
.score-number { font-size: 22px; font-weight: 900; }
.you-score { color: #55eaff; text-shadow: 0 0 8px #00cfff; }
.ai-score { color: #ff5267; text-shadow: 0 0 8px #ff003c; }
.draw-score { color: #ddd1eb; }

/* Status */
.status {
    text-align: center; padding: 7px; border-radius: 12px;
    background: rgba(91, 43, 137, 0.22); border: 1px solid #704497;
    color: #ded4e9; font-size: 12px; font-weight: 700;
}

/* Game board */
.st-key-board {
    position: relative; gap: 6px; padding: 10px; border-radius: 20px;
    background: rgba(6, 2, 14, 0.96); border: 2px solid #7738ad;
    box-shadow: 0 0 15px rgba(130, 50, 255, 0.45);
}
.st-key-board [data-testid="stHorizontalBlock"] { gap: 6px; flex-wrap: nowrap !important; }
.st-key-board [data-testid="stColumn"], .st-key-board [data-testid="column"] {
    flex: 1 1 0 !important; min-width: 0 !important; width: auto !important;
}

/* Cells */
.st-key-board [data-testid="stElementContainer"], .st-key-board [data-testid="stButton"], .st-key-board .stButton { width: 100% !important; }
.st-key-board .stButton > button {
    width: 100%; aspect-ratio: 1 / 1; height: auto; min-height: 0; padding: 0;
    background: linear-gradient(145deg, #17082a, #0b0316);
    border: 2px solid #8f56bd; border-radius: 10px; color: white; transition: 0.15s;
}
.st-key-board .stButton > button p { font-size: 40px; font-weight: 900; line-height: 1; }
.st-key-board .stButton > button:hover:not(:disabled) {
    background: #211039; border-color: #d7aaff;
    box-shadow: 0 0 10px #a34cff, 0 0 20px rgba(163, 76, 255, 0.5);
}
.st-key-board .stButton > button:disabled { opacity: 1; cursor: default; }

/* X and O */
[class*="st-key-x_"] button p, [class*="st-key-wx"] button p {
    color: #55eaff !important; text-shadow: 0 0 7px #55eaff, 0 0 16px #009cff, 0 0 30px #009cff;
}
[class*="st-key-o_"] button p, [class*="st-key-wo"] button p {
    color: #ff596a !important; text-shadow: 0 0 7px #ff596a, 0 0 16px #ff003c, 0 0 30px #ff003c;
}

/* Winning cells + winning line (line har jeetne wale cell ke andar banti hai) */
[class*="st-key-wx"] button, [class*="st-key-wo"] button { position: relative; border-color: white !important; background: #241035 !important; }
[class*="st-key-wx"] button { --lc: #55eaff; }
[class*="st-key-wo"] button { --lc: #ff596a; }
[class*="st-key-wx"] button::after, [class*="st-key-wo"] button::after {
    content: ""; position: absolute; left: 50%; top: 50%; z-index: 5;
    background: var(--lc); border-radius: 4px; pointer-events: none;
    box-shadow: 0 0 6px var(--lc), 0 0 12px var(--lc);
}
[class*="st-key-wxh"] button::after, [class*="st-key-woh"] button::after { width: calc(100% + 10px); height: 4px; transform: translate(-50%, -50%); }
[class*="st-key-wxv"] button::after, [class*="st-key-wov"] button::after { width: 4px; height: calc(100% + 10px); transform: translate(-50%, -50%); }
[class*="st-key-wxa"] button::after, [class*="st-key-woa"] button::after { width: calc(141% + 14px); height: 4px; transform: translate(-50%, -50%) rotate(45deg); }
[class*="st-key-wxb"] button::after, [class*="st-key-wob"] button::after { width: calc(141% + 14px); height: 4px; transform: translate(-50%, -50%) rotate(-45deg); }

/* Buttons */
.st-key-restart_btn button, .st-key-reset_btn button {
    width: 100%; padding: 6px 0; border-radius: 11px; font-weight: 800;
}
.st-key-restart_btn button p, .st-key-reset_btn button p { font-size: 11px; font-weight: 800; }
.st-key-restart_btn button {
    color: white; background: linear-gradient(90deg, #6321a8, #963bd8);
    border: 1px solid #d08cff; box-shadow: 0 0 10px rgba(150, 59, 216, 0.4);
}
.st-key-reset_btn button { color: #d0c5db; background: #150a25; border: 1px solid #604773; }

/* Footer */
.footer { text-align: center; color: #746780; font-size: 9px; }
</style>
""",
    unsafe_allow_html=True
)


# -----------------------------
# Title + Score + Status
# -----------------------------
if st.session_state.game_over:
    if st.session_state.result == HUMAN:
        status_text = "🏆 YOU WIN!"
    elif st.session_state.result == AI:
        status_text = "🤖 AI WINS!"
    else:
        status_text = "🤝 IT'S A DRAW!"
else:
    status_text = "⚡ YOUR TURN — CHOOSE A CELL"

header_html = (
    '<div class="title">🎮 TIC-TAC-TOE</div>'
    '<div class="subtitle">NEON EDITION • MINIMAX AI</div>'
    '<div class="score">'
    '<div class="score-box"><div class="score-label">YOU</div>'
    f'<div class="score-number you-score">{st.session_state.you_score}</div></div>'
    '<div class="score-box"><div class="score-label">DRAW</div>'
    f'<div class="score-number draw-score">{st.session_state.draw_score}</div></div>'
    '<div class="score-box"><div class="score-label">AI</div>'
    f'<div class="score-number ai-score">{st.session_state.ai_score}</div></div>'
    '</div>'
    f'<div class="status">{status_text}</div>'
)
st.markdown(header_html, unsafe_allow_html=True)


# -----------------------------
# Board
# -----------------------------
board = st.session_state.board
win_line = winning_line(board) or []

direction = ""
if win_line:
    direction = {2: "h", 6: "v", 8: "a", 4: "b"}.get(win_line[-1] - win_line[0], "")

with st.container(key="board"):
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            index = row * 3 + col
            value = board[index]
            winning = index in win_line

            if value == HUMAN:
                kind = f"wx{direction}" if winning else "x"
            elif value == AI:
                kind = f"wo{direction}" if winning else "o"
            else:
                kind = "e"

            label = "\u2800" if value == EMPTY else str(value)

            with cols[col]:
                st.button(
                    label,
                    key=f"{kind}_{index}",
                    on_click=play_move,
                    args=(index,),
                    disabled=(value != EMPTY or st.session_state.game_over)
                )


# -----------------------------
# Action buttons
# -----------------------------
left, right = st.columns(2)

with left:
    st.button("🔄RESTART GAME", key="restart_btn", on_click=restart_game)

with right:
    st.button("🧹RESET SCORE", key="reset_btn", on_click=reset_score)


