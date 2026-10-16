import pyxel
import random

# 0: 通路、1: 壁
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# 上下左右の移動方向
DIRECTIONS = [
    (0, -1),
    (0, 1),
    (-1, 0),
    (1, 0),
]


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        nx = self.x
        ny = self.y

        if pyxel.btnp(pyxel.KEY_UP):
            ny -= 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            ny += 1
        elif pyxel.btnp(pyxel.KEY_LEFT):
            nx -= 1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            nx += 1

        if 0 <= nx < 16 and 0 <= ny < 16:
            if maze[ny][nx] == 0:
                self.x = nx
                self.y = ny

    def draw(self):
        pyxel.rect(
            self.x * 10 + 2,
            self.y * 10 + 2,
            6, 6, 10
        )


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timer = 0
        self.interval = random.randint(15, 45)

    def update(self):
        self.timer += 1

        if self.timer < self.interval:
            return

        self.timer = 0
        self.interval = random.randint(15, 45)

        # 移動できる方向を調べる
        possible_moves = []

        for dx, dy in DIRECTIONS:
            nx = self.x + dx
            ny = self.y + dy

            if 0 <= nx < 16 and 0 <= ny < 16:
                if maze[ny][nx] == 0:
                    possible_moves.append((nx, ny))

        # 移動可能な通路をランダムに選ぶ
        if possible_moves:
            self.x, self.y = random.choice(possible_moves)

    def draw(self):
        pyxel.rect(
            self.x * 10 + 2,
            self.y * 10 + 2,
            6, 6, 2
        )


class Game:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player = Player(1, 1)

        # 敵を3体配置
        self.enemies = [
            Enemy(8, 9),
            Enemy(13, 3),
            Enemy(5, 11),
        ]

        self.goal_x = 14
        self.goal_y = 14
        self.cleared = False
        self.game_over = False

    def update(self):
        if self.cleared or self.game_over:
            if pyxel.btnp(pyxel.KEY_R):
                self.reset()
            return

        # プレイヤーを移動
        self.player.update()

        # プレイヤーが敵に接触したか確認
        for enemy in self.enemies:
            if self.player.x == enemy.x and self.player.y == enemy.y:
                self.game_over = True
                return

        # 敵を移動
        for enemy in self.enemies:
            enemy.update()

        # 移動後の接触判定
        for enemy in self.enemies:
            if self.player.x == enemy.x and self.player.y == enemy.y:
                self.game_over = True
                return

        # ゴール判定
        if (
            self.player.x == self.goal_x
            and self.player.y == self.goal_y
        ):
            self.cleared = True

    def draw(self):
        pyxel.cls(0)

        # 迷路を描画
        for y in range(16):
            for x in range(16):
                if maze[y][x] == 1:
                    color = 5
                else:
                    color = 11

                pyxel.rect(
                    x * 10,
                    y * 10,
                    10, 10, color
                )

        # ゴール
        pyxel.rect(
            self.goal_x * 10 + 2,
            self.goal_y * 10 + 2,
            6, 6, 8
        )

        # 敵を3体描画
        for enemy in self.enemies:
            enemy.draw()

        # プレイヤー
        self.player.draw()

        if self.cleared:
            pyxel.rect(35, 65, 90, 30, 0)
            pyxel.text(57, 73, "GAME CLEAR!", 10)
            pyxel.text(53, 84, "R: RETRY", 7)

        elif self.game_over:
            pyxel.rect(30, 65, 100, 30, 0)
            pyxel.text(49, 73, "GAME OVER", 8)
            pyxel.text(53, 84, "R: RETRY", 7)


pyxel.init(160, 160, title="Enemy Maze")
game = Game()
pyxel.run(game.update, game.draw)