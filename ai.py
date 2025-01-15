import math

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


class TeamtaidaAI(object):
    def face(self):
        return "🐰"

   def place(self, board, stone):
        # ゲーム進行状況に応じた評価値表の定義
        early_table = [
            [120, -20, 10, 10, -20, 120],
            [-20, -40, -5, -5, -40, -20],
            [10,  -5,   5,  5,  -5,  10],
            [10,  -5,   5,  5,  -5,  10],
            [-20, -40, -5, -5, -40, -20],
            [120, -20, 10, 10, -20, 120],
        ]

        mid_table = [
            [100, -50,  20,  20, -50, 100],
            [-50, -80, -10, -10, -80, -50],
            [20,  -10,  15,  15, -10,  20],
            [20,  -10,  15,  15, -10,  20],
            [-50, -80, -10, -10, -80, -50],
            [100, -50,  20,  20, -50, 100],
        ]

        late_table = [
            [500, -200, 50,  50, -200, 500],
            [-200, -300, -50, -50, -300, -200],
            [50,   -50,   0,   0,  -50,   50],
            [50,   -50,   0,   0,  -50,   50],
            [-200, -300, -50, -50, -300, -200],
            [500, -200, 50,  50, -200, 500],
        ]

        # ゲーム進行状況を判断（石の数をカウント）
        total_stones = sum(row.count(BLACK) + row.count(WHITE) for row in board)
        if total_stones < 20:  # 序盤
            evaluation_table = early_table
        elif total_stones < 40:  # 中盤
            evaluation_table = mid_table
        else:  # 終盤
            evaluation_table = late_table

        # 最適な手を探索
        best_score = float('-inf')
        best_move = None

        for y in range(len(board)):
            for x in range(len(board[0])):
                if can_place_x_y(board, stone, x, y):
                    # 評価値を取得
                    score = evaluation_table[y][x]
                    if score > best_score:
                        best_score = score
                        best_move = (x, y)

        # 最適な手を返す
        if best_move:
            return best_move
        else:
            raise ValueError("No valid moves available")

