import pyxel


class Game:
    def __init__(self):
        self.count = 0

    def update(self):
        """上キーで1増やす処理と下キーで1減らす処理を追加したい。btnとbtnpの違いを意識して書くと良い。"""

    def draw(self):
        pyxel.cls(0)

        # 数値を画面に表示する
        pyxel.text(70, 55, f"Count: {self.count}", 7)


game = Game()

pyxel.init(160, 120, title="Counter")
pyxel.run(game.update, game.draw)