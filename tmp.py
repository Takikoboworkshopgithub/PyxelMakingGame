
import pyxel

# タイル画像の座標
STONE = (0, 0)  # 石
DIRT = (0, 1)   # 土
GRASS = (1, 0)  # 草

TILE_SIZE = 8
MOVE_SPEED = 2


class App:
    def __init__(self):
        pyxel.init(128, 128, title="Tilemap Movement")
        pyxel.load("my_resource.pyxres")

        # プレイヤーの位置（ピクセル単位）
        self.x = 8
        self.y = 8

        # 移動先の位置
        self.target_x = self.x
        self.target_y = self.y

        self.dir = "UP"
        self.TIME = 0

        pyxel.run(self.update, self.draw)

    def can_move(self, x, y):
        # マップの範囲外なら移動できない
        if not (0 <= x < 16 and 0 <= y < 16):
            return False

        # キャラクターが占める2×2タイルを確認
        for tx in range(x, x + 2):
            for ty in range(y, y + 2):
                # マップの範囲外なら移動できない
                if not (0 <= tx < 16 and 0 <= ty < 16):
                    return False

                tile = pyxel.tilemaps[0].pget(tx, ty)

                # 石なら移動できない
                if tile == STONE:
                    return False

        return True

    def update(self):
        self.TIME = (self.TIME + 1) % 60

        # 移動中なら、移動先へ少しずつ近づける
        if self.x != self.target_x or self.y != self.target_y:
            if self.x < self.target_x:
                self.x = min(self.x + MOVE_SPEED, self.target_x)
            elif self.x > self.target_x:
                self.x = max(self.x - MOVE_SPEED, self.target_x)

            if self.y < self.target_y:
                self.y = min(self.y + MOVE_SPEED, self.target_y)
            elif self.y > self.target_y:
                self.y = max(self.y - MOVE_SPEED, self.target_y)

            return

        # 移動が完了したら、次の入力を確認する
        nx = self.x // TILE_SIZE
        ny = self.y // TILE_SIZE
        ndir = self.dir

        if pyxel.btn(pyxel.KEY_LEFT):
            nx -= 1
            ndir = "LEFT"
        elif pyxel.btn(pyxel.KEY_RIGHT):
            nx += 1
            ndir = "RIGHT"
        elif pyxel.btn(pyxel.KEY_UP):
            ny -= 1
            ndir = "UP"
        elif pyxel.btn(pyxel.KEY_DOWN):
            ny += 1
            ndir = "DOWN"
        else:
            return

        # 向きは壁にぶつかっても更新する
        self.dir = ndir

        # 移動可能なら移動先を設定する
        if self.can_move(nx, ny):
            self.target_x = nx * TILE_SIZE
            self.target_y = ny * TILE_SIZE


    def draw(self):
        pyxel.cls(0)

        # タイルマップを描画
        pyxel.bltm(
            0, 0,
            0,
            0, 0,
            128, 128
        )


        # 向きに応じて画像の取得位置を決める
        if self.dir == "DOWN":
            u, v = 32, 32
        elif self.dir == "UP":
            u, v = 0, 16
        elif self.dir == "LEFT":
            u, v = 0, 48
        elif self.dir == "RIGHT":
            u, v = 32, 48

        # 歩行アニメーションのフレームを選ぶ
        if self.x != self.target_x or self.y != self.target_y:
            frame = 16 if self.TIME < 30 else 0
        else:
            frame  = 0

        # プレイヤーを描画
        pyxel.blt(
            self.x, self.y,
            0,
            u + frame, v,
            16, 16,
            10
        )


App()
