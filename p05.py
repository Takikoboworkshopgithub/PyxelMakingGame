import pyxel


# 共通する機能を持つ親クラス
class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def update(self):
        pass

    def draw(self):
        pyxel.rect(self.x, self.y, 10, 10, self.color)


# WASDキーで動く子クラス
class WASDPlayer(Player):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def update(self):
        if pyxel.btn(pyxel.KEY_A):
            self.x -= 1
        if pyxel.btn(pyxel.KEY_D):
            self.x += 1
        if pyxel.btn(pyxel.KEY_W):
            self.y -= 1
        if pyxel.btn(pyxel.KEY_S):
            self.y += 1


# 矢印キーで動く子クラス
class ArrowPlayer(Player):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 1


class Game:
    def __init__(self):
        self.player1 = WASDPlayer(30, 50, 7)
        self.player2 = ArrowPlayer(120, 50, 8)
        self.state = "playing"

    def collision(self):
        # 2人のプレイヤーが重なったか判定
        if (
    """重なっているかを判定したい。"""
        ):
            return True

        return False

    def update(self):
        if self.state == "gameover":
            return

        self.player1.update()
        self.player2.update()

        # 衝突したらゲームオーバー
        if self.collision():
            self.state = "gameover"

    def draw(self):
        pyxel.cls(0)

        if self.state == "playing":
            self.player1.draw()
            self.player2.draw()

        elif self.state == "gameover":
            pyxel.cls(8)
            pyxel.text(55, 55, "GAME OVER", 7)


game = Game()

pyxel.init(160, 120)
pyxel.run(game.update, game.draw)