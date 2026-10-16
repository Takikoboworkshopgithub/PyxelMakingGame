
import pyxel

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


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        nx = self.x
        ny = self.y

        # 移動先を決める
        if pyxel.btnp(pyxel.KEY_UP):
            ny -= 1
        elif pyxel.btnp(pyxel.KEY_DOWN):
            ny += 1
        elif pyxel.btnp(pyxel.KEY_LEFT):
            nx -= 1
        elif pyxel.btnp(pyxel.KEY_RIGHT):
            nx += 1

        # 画面外に出ていないか確認
        if 0 <= nx < 16 and 0 <= ny < 16:
            # 通路なら移動する
            if maze[ny][nx] == 0:
                self.x = nx
                self.y = ny

    def draw(self):
        # プレイヤーを描画
        pyxel.rect(
            self.x * 10 + 2,
            self.y * 10 + 2,
            6,
            6,
            10
        )


class Game:
    def __init__(self):
        self.player = Player(1, 1)
        self.goal_x = 14
        self.goal_y = 14
        self.cleared = False

    def update(self):
        if not self.cleared:
            self.player.update()

            # ゴールに到達したか確認
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
                    color = 5   # 壁
                else:
                    color = 11  # 通路

                pyxel.rect(
                    x * 10,
                    y * 10,
                    10,
                    10,
                    color
                )

        # ゴールを描画
        pyxel.rect(
            self.goal_x * 10 + 2,
            self.goal_y * 10 + 2,
            6,
            6,
            8
        )

        # プレイヤーを描画
        self.player.draw()

        # クリア表示
        if self.cleared:
            pyxel.rect(35, 65, 90, 30, 0)
            pyxel.text(57, 77, "GAME CLEAR!", 10)


pyxel.init(160, 160, title="Maze")
game = Game()
pyxel.run(game.update, game.draw)
