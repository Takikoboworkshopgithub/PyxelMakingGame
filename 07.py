import pyxel


class Player:
    def __init__(self):
        self.x = 5
        self.y = 105
        self.vy = 0
        self.jumping = False

    def update(self, blocks):
        # 左右移動
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x -= 2
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x += 2

        # ジャンプ
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.jumping:
            self.vy = -5
            self.jumping = True

        # 重力
        old_y = self.y
        self.vy += 0.25
        self.y += self.vy

        # ブロックとの衝突判定
        for block in blocks:
            bx, by, bw, bh, color = block

            # 横方向に重なっているか
            if self.x + 6 > bx and self.x < bx + bw:
                # 上から着地したか
                if old_y + 6 <= by and self.y + 6 >= by and self.vy >= 0:
                    self.y = by - 6
                    self.vy = 0
                    self.jumping = False

        # 落下したら最初から
        if self.y > 120:
            self.x = 5
            self.y = 105
            self.vy = 0
            self.jumping = False

    def draw(self):
        pyxel.rect(self.x, self.y, 6, 6, 7)


class Game:
    def __init__(self):
        pyxel.init(160, 120, title="Jump Game")

        self.player = Player()

        # 左から段々高くなる4つのブロック
        self.blocks = [
            (0, 112, 35, 8, 7),
            (35, 92, 35, 8, 7),
            (70, 72, 35, 8, 7),
            (105, 52, 35, 8, 10),
        ]

        self.clear = False

        pyxel.run(self.update, self.draw)

    def update(self):
        if self.clear:
            return

        self.player.update(self.blocks)

        # 最後のブロックに到達したらクリア
        if (
           """到達したかを判定したい。"""
        ):
            self.clear = True

    def draw(self):
        pyxel.cls(0)

        # ブロックを描画
        for i, block in enumerate(self.blocks):
            x, y, w, h, color = block
            pyxel.rect(x, y, w, h, color)

        self.player.draw()

        if self.clear:
            pyxel.text(60, 20, "CLEAR!", 10)


Game()