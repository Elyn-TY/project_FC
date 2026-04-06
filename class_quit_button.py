from operator import pos

import pygame

# レイヤーの分類の詳細はmemo.txtを参照


class QuitButton(pygame.sprite.Sprite):
    def __init__(self, x, y, layer=1000):
        super().__init__()
        self._layer = layer
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(x, y))
        pygame.draw.rect(  # ボタンの背景
            self.image,
            (255, 0, 0, 200),  # 塗りつぶし色
            self.image.get_rect(),
            border_radius=10,  # 丸みの度合い(枠と合わせること！)
        )
        pygame.draw.rect(  # 枠線
            self.image, (0, 0, 0, 255), self.image.get_rect(), width=2, border_radius=10
        )
        font = pygame.font.SysFont("meiryo", 15, bold=True)
        text = font.render("Quit", True, (255, 255, 255))  # 白色のテキスト
        text_rect = text.get_rect(center=self.image.get_rect().center)
        self.image.blit(text, text_rect)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)  # マスクを作成
        self.colliding = False
        self.base_image = self.image.copy()  # 元の画像を保存

    def is_clicked(self, pos):
        if not self.rect.collidepoint(pos):
            return False

        local_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)

        return self.mask.get_at(local_pos)

    def update(self):
        self.image = self.base_image.copy()  # ボタンの画像をリセット
        if self.colliding:
            pygame.draw.rect(
                self.image,
                (255, 255, 0, 240),  # 塗りつぶし色
                self.image.get_rect(),
                width=2,
                border_radius=10,  # 丸みの度合い(枠と合わせること！)
            )
