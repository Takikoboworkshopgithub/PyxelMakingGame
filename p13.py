import pyxel

# タイル画像の座標
STONE = (0, 0)
GRASS = (0, 1)
SOIL = (1, 0)

TILE_SIZE = 8
MOVE_SPEED = 2
PLAYER_SIZE = 16
SCREEN_SIZE = 128

PLAYER_SCREEN_X = 56
PLAYER_SCREEN_Y = 56

MAP_START_X = 32
MAP_START_Y = 0


class Game:
    def __init__(self):
        pyxel.init(128, 128, title="Break Blocks")
        pyxel.load("my_resource.pyxres")

        # カメラの位置
        self.camera_x = MAP_START_X * TILE_SIZE
        self.camera_y = MAP_START_Y * TILE_SIZE

        # プレイヤーの状態
        self.direction = "DOWN"
        self.time = 0
        self.moving = False

        # 変更したタイルを管理
        # {(タイルX, タイルY): タイル画像の座標}
        self.changed_tiles = {}

        pyxel.run(self.update, self.draw)

    def get_tile(self, tx, ty):
        """(tx, ty)が変更済みのタイルならそれをかえす"""
        # ないなら元のタイルを取得
        return pyxel.tilemaps[0].pget(tx, ty)

    def can_move(self, x, y):
        # プレイヤーが占有するタイル範囲
        left = x // TILE_SIZE
        top = y // TILE_SIZE
        right = (x + PLAYER_SIZE - 1) // TILE_SIZE
        bottom = (y + PLAYER_SIZE - 1) // TILE_SIZE

        # 2×2タイルの当たり判定
        for tx in range(left, right + 1):
            for ty in range(top, bottom + 1):
                if self.get_tile(tx, ty) == STONE:
                    return False

        return True

    def break_blocks(self):
        # プレイヤーのワールド座標
        x = self.camera_x + PLAYER_SCREEN_X
        y = self.camera_y + PLAYER_SCREEN_Y

        # 向いている方向の隣にある2タイル
        if self.direction == "LEFT":
            tx = (x - 1) // TILE_SIZE
            ty = y // TILE_SIZE
            targets = [(tx, ty), (tx, ty + 1)]

        elif self.direction == "RIGHT":
            tx = (x + PLAYER_SIZE) // TILE_SIZE
            ty = y // TILE_SIZE
            targets = [(tx, ty), (tx, ty + 1)]

        elif self.direction == "UP":
            tx = x // TILE_SIZE
            ty = (y - 1) // TILE_SIZE
            targets = [(tx, ty), (tx + 1, ty)]

        else:  # DOWN
            tx = x // TILE_SIZE
            ty = (y + PLAYER_SIZE) // TILE_SIZE
            targets = [(tx, ty), (tx + 1, ty)]

        # 石を草に置き換える
        for tx, ty in targets:
            if self.get_tile(tx, ty) == STONE:
                self.changed_tiles[(tx, ty)] = GRASS

    def update(self):
        self.time = (self.time + 1) % 60
        self.moving = False

        dx = 0
        dy = 0

        # キー入力
        if pyxel.btn(pyxel.KEY_LEFT):
            dx = -MOVE_SPEED
            self.direction = "LEFT"
        elif pyxel.btn(pyxel.KEY_RIGHT):
            dx = MOVE_SPEED
            self.direction = "RIGHT"
        elif pyxel.btn(pyxel.KEY_UP):
            dy = -MOVE_SPEED
            self.direction = "UP"
        elif pyxel.btn(pyxel.KEY_DOWN):
            dy = MOVE_SPEED
            self.direction = "DOWN"

        # スペースキーでブロックを壊す
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.break_blocks()

        # 移動入力がなければ終了
        if dx == 0 and dy == 0:
            return

        # 移動先のワールド座標
        x = self.camera_x + PLAYER_SCREEN_X + dx
        y = self.camera_y + PLAYER_SCREEN_Y + dy

        # 石がなければカメラを移動
        if self.can_move(x, y):
            self.camera_x += dx
            self.camera_y += dy
            self.moving = True

    def draw(self):
        pyxel.cls(0)

        # タイルマップを描画
        pyxel.bltm(
            0, 0, 0,
            self.camera_x, self.camera_y,
            SCREEN_SIZE, SCREEN_SIZE
        )

        # 変更したタイルを描画
        for (tx, ty), tile in self.changed_tiles.items():
            screen_x = tx * TILE_SIZE - self.camera_x
            screen_y = ty * TILE_SIZE - self.camera_y

            pyxel.blt(
                screen_x, screen_y, 0,
                tile[0] * TILE_SIZE,
                tile[1] * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )

        # プレイヤーの画像座標
        if self.direction == "DOWN":
            u, v = 32, 32
        elif self.direction == "UP":
            u, v = 0, 16
        elif self.direction == "LEFT":
            u, v = 0, 48
        else:
            u, v = 32, 48

        # 歩行アニメーション
        frame = 16 if self.moving and self.time < 30 else 0

        # プレイヤーを画面中央に描画
        pyxel.blt(
            PLAYER_SCREEN_X, PLAYER_SCREEN_Y, 0,
            u + frame, v,
            PLAYER_SIZE, PLAYER_SIZE, 10
        )


Game()