import pyxel


class Game:
    def __init__(self):
        self.count = 0

    def update(self):
        # 上キーで1増やす
        if pyxel.btnp(pyxel.KEY_UP):
            self.count += 1

        # 下キーで1減らす
        if pyxel.btnp(pyxel.KEY_DOWN):
            self.count -= 1

    def draw(self):
        pyxel.cls(0)

        # 数値を画面に表示する
        pyxel.text(70, 55, f"Count: {self.count}", 7)


game = Game()

pyxel.init(160, 120, title="Counter")
pyxel.run(game.update, game.draw)