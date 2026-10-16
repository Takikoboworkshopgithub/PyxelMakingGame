import pyxel


class App:
    def __init__(self):
        pyxel.init(128, 128, title="Tilemap Movement")
        pyxel.load("my_resource.pyxres")

        # プレイヤーの初期位置（ピクセル単位）
        self.x = 8
        self.y = 8

        # プレイヤーの向き
        self.dir = "UP"

        pyxel.run(self.update, self.draw)

    def update(self):
        # 矢印キーに応じて移動し、向きを変更する
        if pyxel.btnp(pyxel.KEY_LEFT):
            self.x -= 8
            self.dir = "LEFT"

        elif pyxel.btnp(pyxel.KEY_RIGHT):
            self.x += 8
            self.dir = "RIGHT"

        elif pyxel.btnp(pyxel.KEY_UP):
            self.y -= 8
            self.dir = "UP"

        elif pyxel.btnp(pyxel.KEY_DOWN):
            self.y += 8
            self.dir = "DOWN"

    def draw(self):
        pyxel.cls(0)

        # タイルマップを描画
        pyxel.bltm(
            0, 0,     # 描画位置
            0,        # タイルマップ番号
            0, 0,     # マップ上の開始位置
            128, 128  # 描画範囲
        )

        # 向きに応じて画像の取得座標を決める
        if self.dir == "DOWN":
            u, v = 32, 32
        elif self.dir == "UP":
            u, v = 0, 16
        elif self.dir == "LEFT":
            u, v = 0, 48
        elif self.dir == "RIGHT":
            u, v = 32, 48

        # プレイヤーを描画
        pyxel.blt(
            self.x, self.y,  # 描画位置
            0,                # 画像バンク
            u, v,              # 画像の取得開始座標
            16, 16,            # 画像サイズ
            10                 # 透過色
        )


App()