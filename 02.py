import pyxel


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vy = 0
        self.jumping = False

    def update(self):
        # 上キーでジャンプ
        if pyxel.btnp(pyxel.KEY_UP) and not self.jumping:
            self.vy = -5
            self.jumping = True

        # 重力によって落下する
        self.vy += 0.2
        self.y += self.vy

        # 地面との当たり判定
        if self.y >= 100:
            self.y = 100
            self.vy = 0
            self.jumping = False
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2

    def draw(self):
        pyxel.rect(self.x, self.y, 10, 10, 7)


class Game:
    def __init__(self):
        self.player = Player(75, 90)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)

        # 地面の線
        pyxel.line(0, 110, 160, 110, 11)

        self.player.draw()


game = Game()

pyxel.init(160, 120, title="Jump Game")
pyxel.run(game.update, game.draw)