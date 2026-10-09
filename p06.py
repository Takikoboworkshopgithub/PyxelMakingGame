import pyxel
import random


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2

        self.x = max(0, min(self.x, 150))

    def draw(self):
        pyxel.rect(self.x, self.y, 10, 10, 7)


class Meteor:
    def __init__(self):
        self.x = random.randint(0, 156)
        self.y = random.randint(-120, 0)

    def update(self):
        self.y += 1

        # 画面の下まで落ちたら、上に戻す
        if self.y > 120:
            self.x = random.randint(0, 156)
            self.y = random.randint(-30, 0)

    def draw(self):
        # 小さな隕石を描画
        pyxel.circ(self.x + 2, self.y + 2, 2, 8)


class Game:
    def __init__(self):
        self.player = Player(75, 100)

        # 隕石を複数生成
        self.meteors = []
        for i in range(5):
            self.meteors.append(Meteor())

        self.state = "playing"

    def collision(self, meteor):
        return (
            self.player.x < meteor.x + 4
            and self.player.x + 10 > meteor.x
            and self.player.y < meteor.y + 4
            and self.player.y + 10 > meteor.y
        )

    def update(self):
        if self.state == "gameover":
            return

        self.player.update()

        # すべての隕石を更新し、衝突判定
        for meteor in self.meteors:
            meteor.update()

            if self.collision(meteor):
                self.state = "gameover"

    def draw(self):
        pyxel.cls(0)

        if self.state == "playing":
            self.player.draw()

            # すべての隕石を描画
            for meteor in self.meteors:
                meteor.draw()

            pyxel.text(5, 5, "Avoid the meteors!", 7)

        elif self.state == "gameover":
            """ゲームオーバー画面を表示"""


game = Game()

pyxel.init(160, 120, title="Avoid the Meteors")
pyxel.run(game.update, game.draw)