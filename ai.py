import math
import random

BLACK = 1
WHITE = 2

board = [
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 1, 2, 0, 0],
    [0, 0, 2, 1, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

def can_place_x_y(board, stone, x, y):
    """
    石を置けるかどうかを調べる関数。
    board: 2次元配列のオセロボード
    x, y: 石を置きたい座標 (0-indexed)
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    return: 置けるなら True, 置けないなら False
    """
    if board[y][x] != 0:
        return False  # 既に石がある場合は置けない

    opponent = 3 - stone  # 相手の石 (1なら2、2なら1)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        found_opponent = False

        while 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == opponent:
            nx += dx
            ny += dy
            found_opponent = True

        if found_opponent and 0 <= nx < len(board[0]) and 0 <= ny < len(board) and board[ny][nx] == stone:
            return True  # 石を置ける条件を満たす

    return False

def can_place(board, stone):
    """
    石を置ける場所を調べる関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    for y in range(len(board)):
        for x in range(len(board[0])):
            if can_place_x_y(board, stone, x, y):
                return True
    return False

def random_place(board, stone):
    """
    石をランダムに置く関数。
    board: 2次元配列のオセロボード
    stone: 現在のプレイヤーの石 (1: 黒, 2: 白)
    """
    while True:
        x = random.randint(0, len(board[0]) - 1)
        y = random.randint(0, len(board) - 1)
        if can_place_x_y(board, stone, x, y):
            return x, y

class TeamtaidaAI(object):
    def __init__(self):
        # 序盤の評価値表
        self.early_game_table = [
            [100, -20, 10, 10, -20, 100],
            [-20, -50, 1, 1, -50, -20],
            [10, 1, 5, 5, 1, 10],
            [10, 1, 5, 5, 1, 10],
            [-20, -50, 1, 1, -50, -20],
            [100, -20, 10, 10, -20, 100],
        ]
        # 中盤の評価値表
        self.mid_game_table = [
            [50, -20, 5, 5, -20, 50],
            [-20, -40, 3, 3, -40, -20],
            [5, 3, 1, 1, 3, 5],
            [5, 3, 1, 1, 3, 5],
            [-20, -40, 3, 3, -40, -20],
            [50, -20, 5, 5, -20, 50],
        ]
        # 終盤の評価値表
        self.late_game_table = [
            [10, 5, 2, 2, 5, 10],
            [5, 1, 1, 1, 1, 5],
            [2, 1, 1, 1, 1, 2],
            [2, 1, 1, 1, 1, 2],
            [5, 1, 1, 1, 1, 5],
            [10, 5, 2, 2, 5, 10],
        ]

    def face(self):
        return "🐰"

    def evaluate_phase(self, board):
        """
        ゲームの進行状況を評価する。
        序盤: 石が20個未満
        中盤: 石が20〜50個
        終盤: 石が50個以上
        """
        stone_count = sum(row.count(BLACK) + row.count(WHITE) for row in board)
        if stone_count < 20:
            return "early"
        elif stone_count < 50:
            return "mid"
        else:
            return "late"

    def get_evaluation_table(self, phase):
        """
        ゲームフェーズに応じた評価値表を取得する。
        """
        if phase == "early":
            return self.early_game_table
        elif phase == "mid":
            return self.mid_game_table
        else:  # "late"
            return self.late_game_table

    def place(self, board, stone):
        # 現在のフェーズを取得
        phase = self.evaluate_phase(board)
        evaluation_table = self.get_evaluation_table(phase)

        best_score = float('-inf')  # 最小のスコアから開始
        best_move = None

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    score = evaluation_table[y][x]
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        if best_move:
            return best_move
        else:
            raise Exception("No valid moves available")
