import pyxel
import random


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 1
        if pyxel.btn(pyxel.KEY_UP):
            self.y -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y += 1

        # 画面外に出ないようにする
        self.x = max(0, min(self.x, 154))
        self.y = max(0, min(self.y, 114))

    def draw(self):
        pyxel.rect(self.x, self.y, 6, 6, 7)


class Point:
    def __init__(self):
        # 目標ポイントをランダムに決める
        self.x = random.randint(0, 154)
        self.y = random.randint(0, 114)

    def draw(self):
        # 目標ポイントを表示
        pyxel.circ(self.x + 3, self.y + 3, 3, 10)


class Game:
    def __init__(self):
        self.player = Player(75, 55)
        self.point = Point()

        self.distance = self.get_distance()
        self.state = "playing"

    def get_distance(self):
        dx = self.player.x - self.point.x
        dy = self.player.y - self.point.y

        return (dx ** 2 + dy ** 2) ** 0.5

    def update(self):
        if self.state != "playing":
            return

        self.player.update()
        self.distance = self.get_distance()

        # Spaceキーで答え合わせ
        if pyxel.btnp(pyxel.KEY_SPACE):
            if self.distance <= 10:
                self.state = "clear"
            else:
                self.state = "gameover"

    def draw(self):
        pyxel.cls(0)

        if self.state == "playing":
            self.player.draw()

            pyxel.text(5, 5, f"Distance: {self.distance:.1f}", 7)
            pyxel.text(5, 15, "Find the hidden point!", 7)
            pyxel.text(5, 25, "Arrow: Move  SPACE: Check", 7)

        elif self.state == "clear":
            pyxel.cls(3)

            # プレイヤーからポイントまでラインを引く
            pyxel.line(
                self.player.x + 3,
                self.player.y + 3,
                self.point.x + 3,
                self.point.y + 3,
                7
            )

            self.point.draw()
            self.player.draw()

            pyxel.text(65, 10, "CLEAR!", 7)
            pyxel.text(35, 20, "You found the point!", 7)

        elif self.state == "gameover":
            pyxel.cls(8)

            # プレイヤーからポイントまでラインを引く
            pyxel.line(
                self.player.x + 3,
                self.player.y + 3,
                self.point.x + 3,
                self.point.y + 3,
                7
            )

            self.point.draw()
            self.player.draw()

            pyxel.text(55, 10, "GAME OVER", 7)
            pyxel.text(35, 20, "The point is here!", 7)


game = Game()

pyxel.init(160, 120, title="Find the Point")
pyxel.run(game.update, game.draw)