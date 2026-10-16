import pyxel


class Terrain:
    def __init__(self, x, y, w, h, kind):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.kind = kind

    def draw(self):
        if self.kind == "semi":
            # 半当たり地形は薄い線で表示
            pyxel.rect(self.x, self.y, self.w, 2, 11)
        else:
            # ブロックは通常の四角形で表示
            pyxel.rect(self.x, self.y, self.w, self.h, 5)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.w = 8
        self.h = 8

        self.vx = 0
        self.vy = 0
        self.speed = 2
        self.jumping = False

    def update(self, terrains):
        # 横方向の移動量を決める
        self.vx = 0

        if pyxel.btn(pyxel.KEY_LEFT):
            self.vx = -self.speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.vx = self.speed

        # ジャンプ
        if pyxel.btnp(pyxel.KEY_SPACE) and not self.jumping:
            self.vy = -4
            self.jumping = True

        # 横方向の移動前の座標を保存
        old_x = self.x

        # 横方向に移動
        self.x += self.vx

        # 横方向の衝突判定
        for terrain in terrains:
            if terrain.kind == "block":
                self.collision_block_horizontal(terrain, old_x)
            elif terrain.kind == "semi":
                self.collision_semi_horizontal(terrain)

        # 画面外に出ないようにする
        self.x = max(0, min(self.x, 160 - self.w))

        # 重力
        old_y = self.y
        self.vy += 0.2

        # 縦方向に移動
        self.y += self.vy

        # 縦方向の衝突判定
        for terrain in terrains:
            if terrain.kind == "semi":
                self.collision_semi_vertical(terrain, old_y)
            elif terrain.kind == "block":
                self.collision_block_vertical(terrain, old_y)

    # 半当たり地形：縦方向の衝突
    def collision_semi_vertical(self, terrain, old_y):
        # 横方向に重なっていなければ衝突しない
        if self.x + self.w <= terrain.x or self.x >= terrain.x + terrain.w:
            return

        # 上から落下して地形に乗る
        if (
            self.vy >= 0
            and old_y + self.h <= terrain.y
            and self.y + self.h >= terrain.y
        ):
            self.y = terrain.y - self.h
            self.vy = 0
            self.jumping = False

    # 半当たり地形：横方向の衝突
    def collision_semi_horizontal(self, terrain):
        # 横からは通り抜けられる
        pass

    # ブロック：縦方向の衝突
    def collision_block_vertical(self, terrain, old_y):
        # 横方向に重なっていなければ衝突しない
        if self.x + self.w <= terrain.x or self.x >= terrain.x + terrain.w:
            return

        # 上からブロックに当たる
        if (
            self.vy >= 0
            and old_y + self.h <= terrain.y
            and self.y + self.h >= terrain.y
        ):
            self.y = terrain.y - self.h
            self.vy = 0
            self.jumping = False

        # 下からブロックに頭をぶつける
        elif (
            self.vy < 0
            and old_y >= terrain.y + terrain.h
            and self.y <= terrain.y + terrain.h
        ):
            self.y = terrain.y + terrain.h
            self.vy = 0

    # ブロック：横方向の衝突
    def collision_block_horizontal(self, terrain, old_x):
        # 縦方向に重なっていなければ衝突しない
        if self.y + self.h <= terrain.y or self.y >= terrain.y + terrain.h:
            return

        # 右に移動してブロックの左側に当たる
        if (
            self.vx > 0
            and old_x + self.w <= terrain.x
            and self.x + self.w >= terrain.x
        ):
            self.x = terrain.x - self.w

        # 左に移動してブロックの右側に当たる
        elif (
            self.vx < 0
            and old_x >= terrain.x + terrain.w
            and self.x <= terrain.x + terrain.w
        ):
            self.x = terrain.x + terrain.w

    def draw(self):
        pyxel.rect(self.x, self.y, self.w, self.h, 8)


class Game:
    def __init__(self):
        pyxel.init(160, 120, title="Terrain Collision")

        self.player = Player(20, 90)

        self.terrains = [
            # 床
            Terrain(0, 112, 160, 8, "block"),

            # 半当たり地形
            Terrain(10, 85, 55, 2, "semi"),
            Terrain(20, 65, 35, 2, "semi"),

            # ブロック
            Terrain(95, 45, 50, 8, "block"),
            Terrain(120, 45, 8, 35, "block"),
        ]

        pyxel.run(self.update, self.draw)

    def update(self):
        self.player.update(self.terrains)

    def draw(self):
        pyxel.cls(7)

        for terrain in self.terrains:
            terrain.draw()

        self.player.draw()

        pyxel.text(5, 5, "SPACE: Jump", 0)


Game()