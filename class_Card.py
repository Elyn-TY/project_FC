import pygame

# レイヤーの分類の詳細はmemo.txtを参照


class Card(pygame.sprite.Sprite):
        
    def __init__(self, x, y, suit, rank, layer=500):
        super().__init__()  # Spriteクラスの初期化
        font = pygame.font.SysFont("meiryo", 25, bold=True)
        suit_symbols = {"H": "♥", "D": "♦", "C": "♣", "S": "♠"}
        self._layer = layer
        self.suit = suit
        self.rank = rank
        self.image = pygame.Surface((70, 100), pygame.SRCALPHA)  # カードのサイズ
        pygame.draw.rect(
            self.image,
            (224, 224, 224),  # 塗りつぶし色
            self.image.get_rect(),
            border_radius=10,  # 丸みの度合い(枠と合わせること！)
        )
        self.text = None
        self.rect = self.image.get_rect(center=(x, y))
        if self.suit == "H" or self.suit == "D":  # ハートとダイヤは赤色で描画
            self.text = font.render(
                suit_symbols[self.suit] + " " + self.rank, True, (255, 0, 0)
            )
        else:
            self.text = font.render(
                suit_symbols[self.suit] + " " + self.rank, True, (0, 0, 0)
            )

        self.text_rect = self.text.get_rect(
            center=self.image.get_rect().center
        )  # カードの中心にテキストを配置
        self.image.blit(self.text, self.text_rect)
        self.dragging = False
        self.drag_offset = (0, 0)
        self.colliding = False
        self.setted = False
        pygame.draw.rect(
            self.image, (0, 0, 0), self.image.get_rect(), width=2, border_radius=10
        )  # カードの枠線
        self.base_image = self.image.copy()  # 元の画像を保存
        self.mask = pygame.mask.from_surface(self.image)  # マスクを作成

    def update(self):
        self.image = self.base_image.copy()  # カードの画像をリセット
        if self.dragging:
            pygame.draw.rect(
                self.image,
                (0, 255, 0),  # 緑色のハイライト
                self.image.get_rect(),
                width=5,
                border_radius=10,
            )

        if self.colliding:
            pygame.draw.rect(
                self.image,
                (255, 255, 0),  # 黄色のハイライト
                self.image.get_rect(),
                width=5,
                border_radius=10,
            )
