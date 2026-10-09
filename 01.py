import pyxel


class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2

        # 画面外に出ないようにする
        self.x = max(0, min(self.x, 150))

    def draw(self):
        pyxel.rect(self.x, self.y, 10, 10, self.color)


class Game:
    def __init__(self):
        self.player = Player(75, 50, 7)

    def update(self):
        self.player.update()

    def draw(self):
        pyxel.cls(0)
        self.player.draw()


game = Game()

pyxel.init(160, 120, title="Move the Square")
pyxel.run(game.update, game.draw)