"""
Tic-Tac-Toe 5x5 dengan AI Minimax (Alpha-Beta Pruning) + Pygame

Aturan : menang jika berhasil membuat WIN_LEN (default 4) simbol berderet
         secara horizontal, vertikal, atau diagonal.
Pemain : Manusia = 'X' (MIN), AI = 'O' (MAX)
Kontrol: klik kotak kosong untuk melangkah
         R = main ulang, D = ganti tingkat kesulitan (Mudah / Sulit)
"""
import random
import sys

import pygame

# ---------------------------------------------------------------- Konfigurasi
N = 5                 # ukuran papan
WIN_LEN = 4           # jumlah simbol berderet untuk menang
SEARCH_DEPTH = 4      # kedalaman pencarian Minimax
RANDOM_PROB = 0.25    # peluang AI melangkah acak pada mode "Mudah"
HUMAN, AI, EMPTY = "X", "O", " "
WIN_SCORE = 10_000

CELL = 120
BAR = 80
SIZE = N * CELL
WIDTH, HEIGHT = SIZE, SIZE + BAR

BG = (28, 30, 38)
GRID = (70, 74, 90)
X_COLOR = (90, 190, 255)
O_COLOR = (255, 130, 110)
WIN_COLOR = (255, 215, 80)
TEXT = (230, 232, 240)

# ------------------------------------------------- Langkah 1: logika permainan
def _build_lines():
    """Semua 'jendela' sepanjang WIN_LEN pada baris, kolom, dan diagonal."""
    lines = []
    for r in range(N):
        for c in range(N):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                cells = [(r + k * dr, c + k * dc) for k in range(WIN_LEN)]
                if all(0 <= rr < N and 0 <= cc < N for rr, cc in cells):
                    lines.append([rr * N + cc for rr, cc in cells])
    return lines


LINES = _build_lines()
LINES_BY_CELL = [[l for l in LINES if i in l] for i in range(N * N)]


def winning_line(board, idx):
    """Kembalikan garis kemenangan yang melewati sel idx (atau None)."""
    p = board[idx]
    if p == EMPTY:
        return None
    for line in LINES_BY_CELL[idx]:
        if all(board[i] == p for i in line):
            return line
    return None


def full_winner(board):
    """Cek seluruh papan (dipakai UI). Return (pemain, garis) atau (None, None)."""
    for line in LINES:
        p = board[line[0]]
        if p != EMPTY and all(board[i] == p for i in line):
            return p, line
    return None, None


def is_full(board):
    return EMPTY not in board


# ------------------------------------------------ Evaluation function (heuristik)
LINE_WEIGHTS = {0: 0, 1: 1, 2: 10, 3: 100}  # skor menurut jumlah simbol berderet


def evaluate(board):
    """Skor posisi non-terminal. Positif = menguntungkan AI, negatif = manusia."""
    score = 0
    for line in LINES:
        cells = [board[i] for i in line]
        o, x = cells.count(AI), cells.count(HUMAN)
        if o and x:          # garis terblokir, tidak bernilai
            continue
        if o:
            score += LINE_WEIGHTS[o]
        elif x:
            score -= LINE_WEIGHTS[x] * 1.1   # sedikit lebih waspada pada lawan
    return score


# ----------------------------------------------- Langkah 2: Minimax + Alpha-Beta
CENTER = (N - 1) / 2


def candidate_moves(board):
    """Hanya sel kosong yang bersebelahan dengan sel terisi (mengurangi cabang)."""
    occupied = [i for i, v in enumerate(board) if v != EMPTY]
    if not occupied:
        return [(N // 2) * N + N // 2]
    near = set()
    for i in occupied:
        r, c = divmod(i, N)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < N and 0 <= cc < N and board[rr * N + cc] == EMPTY:
                    near.add(rr * N + cc)
    # urutkan dari tengah agar pruning lebih efektif
    return sorted(near, key=lambda i: abs(i // N - CENTER) + abs(i % N - CENTER))


def minimax(board, depth, alpha, beta, maximizing, last):
    if last is not None and winning_line(board, last):
        # kemenangan lebih cepat = skor lebih tinggi
        return WIN_SCORE + depth if board[last] == AI else -(WIN_SCORE + depth)
    if is_full(board):
        return 0
    if depth == 0:
        return evaluate(board)

    if maximizing:
        best = -float("inf")
        for m in candidate_moves(board):
            board[m] = AI
            best = max(best, minimax(board, depth - 1, alpha, beta, False, m))
            board[m] = EMPTY
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    best = float("inf")
    for m in candidate_moves(board):
        board[m] = HUMAN
        best = min(best, minimax(board, depth - 1, alpha, beta, True, m))
        board[m] = EMPTY
        beta = min(beta, best)
        if beta <= alpha:
            break
    return best



def find_best_move(board, random_prob=0.0):
    empties = [i for i, v in enumerate(board) if v == EMPTY]
    if random_prob and random.random() < random_prob:
        return random.choice(empties)

    best_score, best_move = -float("inf"), None
    alpha, beta = -float("inf"), float("inf")
    for m in candidate_moves(board):
        board[m] = AI
        score = minimax(board, SEARCH_DEPTH - 1, alpha, beta, False, m)
        board[m] = EMPTY
        if score > best_score:
            best_score, best_move = score, m
        alpha = max(alpha, best_score)
    return best_move


# ---------------------------------------------------- Langkah 4: UI & game loop
def draw(screen, fonts, board, win_line, status, mode_label):
    screen.fill(BG)
    for i in range(1, N):
        pygame.draw.line(screen, GRID, (i * CELL, 0), (i * CELL, SIZE), 3)
        pygame.draw.line(screen, GRID, (0, i * CELL), (SIZE, i * CELL), 3)

    pad = CELL // 4
    for idx, v in enumerate(board):
        r, c = divmod(idx, N)
        x0, y0 = c * CELL, r * CELL
        if win_line and idx in win_line:
            pygame.draw.rect(screen, (60, 56, 30), (x0 + 4, y0 + 4, CELL - 8, CELL - 8))
        if v == HUMAN:
            col = WIN_COLOR if win_line and idx in win_line else X_COLOR
            pygame.draw.line(screen, col, (x0 + pad, y0 + pad), (x0 + CELL - pad, y0 + CELL - pad), 8)
            pygame.draw.line(screen, col, (x0 + CELL - pad, y0 + pad), (x0 + pad, y0 + CELL - pad), 8)
        elif v == AI:
            col = WIN_COLOR if win_line and idx in win_line else O_COLOR
            pygame.draw.circle(screen, col, (x0 + CELL // 2, y0 + CELL // 2), CELL // 2 - pad, 8)

    pygame.draw.rect(screen, (20, 22, 28), (0, SIZE, WIDTH, BAR))
    screen.blit(fonts[0].render(status, True, TEXT), (16, SIZE + 12))
    hint = f"R: ulang   D: mode ({mode_label})"
    screen.blit(fonts[1].render(hint, True, (150, 154, 170)), (16, SIZE + 48))
    pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Tic-Tac-Toe 5x5 - Minimax AI")
    fonts = (pygame.font.SysFont(None, 34), pygame.font.SysFont(None, 24))
    clock = pygame.time.Clock()

    easy_mode = False
    board = [EMPTY] * (N * N)
    turn, game_over, win_line = HUMAN, False, None
    status = "Giliran Anda (X)"

    while True:
        mode_label = "Mudah" if easy_mode else "Sulit"
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    board = [EMPTY] * (N * N)
                    turn, game_over, win_line = HUMAN, False, None
                    status = "Giliran Anda (X)"
                elif event.key == pygame.K_d:
                    easy_mode = not easy_mode
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1
                    and turn == HUMAN and not game_over):
                x, y = event.pos
                if y < SIZE:
                    idx = (y // CELL) * N + (x // CELL)
                    if board[idx] == EMPTY:
                        board[idx] = HUMAN
                        line = winning_line(board, idx)
                        if line:
                            win_line, game_over, status = line, True, "Anda menang! (R: main lagi)"
                        elif is_full(board):
                            game_over, status = True, "Seri! (R: main lagi)"
                        else:
                            turn, status = AI, "AI sedang berpikir..."

        draw(screen, fonts, board, win_line, status, mode_label)

        if turn == AI and not game_over:
            pygame.event.pump()
            move = find_best_move(board, RANDOM_PROB if easy_mode else 0.0)
            board[move] = AI
            line = winning_line(board, move)
            if line:
                win_line, game_over, status = line, True, "AI menang! (R: main lagi)"
            elif is_full(board):
                game_over, status = True, "Seri! (R: main lagi)"
            else:
                turn, status = HUMAN, "Giliran Anda (X)"

        clock.tick(30)


if __name__ == "__main__":
    main()