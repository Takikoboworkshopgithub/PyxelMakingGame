import pyxel

# タイル画像の座標
STONE = (0, 0)
DIRT = (0, 1)
GRASS = (1, 0)

TILE_SIZE = 8
MOVE_SPEED = 2

SCREEN_SIZE = 128
PLAYER_SIZE = 16

# 地形の開始位置（タイル単位）
MAP_START_X = 32
MAP_START_Y = 0


class App:
    def __init__(self):
        pyxel.init(128, 128, title="Scrolling Tilemap")
        pyxel.load("my_resource.pyxres")

        # カメラの位置（ピクセル単位）
        self.camera_x = MAP_START_X * TILE_SIZE
        self.camera_y = MAP_START_Y * TILE_SIZE

        # プレイヤーの向き
        self.dir = "DOWN"
        self.TIME = 0
        self.moving = False

        pyxel.run(self.update, self.draw)

    def can_move(self, x, y):
        # プレイヤーの左上のピクセル座標から
        # 占有するタイルの範囲を求める
        left = x // TILE_SIZE
        top = y // TILE_SIZE
        right = (x + PLAYER_SIZE - 1) // TILE_SIZE
        bottom = (y + PLAYER_SIZE - 1) // TILE_SIZE

        # プレイヤーが占有するすべてのタイルを確認
        for tx in range(left, right + 1):
            for ty in range(top, bottom + 1):
                tile = pyxel.tilemaps[0].pget(tx, ty)

                # 石があれば移動できない
                if tile == STONE:
                    return False

        return True

    def update(self):
        self.TIME = (self.TIME + 1) % 60
        self.moving = False

        dx = 0
        dy = 0
        ndir = self.dir

        # キー入力を確認
        if pyxel.btn(pyxel.KEY_LEFT):
            dx = -MOVE_SPEED
            ndir = "LEFT"
        elif pyxel.btn(pyxel.KEY_RIGHT):
            dx = MOVE_SPEED
            ndir = "RIGHT"
        elif pyxel.btn(pyxel.KEY_UP):
            dy = -MOVE_SPEED
            ndir = "UP"
        elif pyxel.btn(pyxel.KEY_DOWN):
            dy = MOVE_SPEED
            ndir = "DOWN"

        # 入力がなければ移動しない
        if dx == 0 and dy == 0:
            return

        # プレイヤーの向きを更新
        self.dir = ndir

        # プレイヤーの左上のワールド座標
        world_x = self.camera_x + 56
        world_y = self.camera_y + 56

        # 移動先の左上のワールド座標
        next_x = world_x + dx
        next_y = world_y + dy

        # 移動先の2×2タイル領域に石がないか確認
        # next_x, next_y はピクセル座標のまま渡す
        if self.can_move(next_x, next_y):
            self.camera_x += dx
            self.camera_y += dy
            self.moving = True

    def draw(self):
        pyxel.cls(0)

        # カメラ位置からタイルマップを描画
        pyxel.bltm(
            0, 0,
            0,
            self.camera_x, self.camera_y,
            SCREEN_SIZE, SCREEN_SIZE
        )

        # 向きに応じた画像座標
        if self.dir == "DOWN":
            u, v = 32, 32
        elif self.dir == "UP":
            u, v = 0, 16
        elif self.dir == "LEFT":
            u, v = 0, 48
        else:
            u, v = 32, 48

        # 歩行アニメーション
        frame = 16 if self.moving and self.TIME < 30 else 0

        # プレイヤーを画面中央に固定
        pyxel.blt(
            56, 56,
            0,
            u + frame, v,
            PLAYER_SIZE, PLAYER_SIZE,
            10
        )


App()