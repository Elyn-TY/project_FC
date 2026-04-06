
import pygame

class Cell(pygame.sprite.Sprite):
    def __init__(self, x, y, layer=0):
        super().__init__()
        self.rect = pygame.Rect(x, y, 70, 100)
        self._layer = layer
        self.image = pygame.Surface((70, 100), pygame.SRCALPHA)

        self.cards = []  # このセルに置かれているカードのリスト
        self.base_image = self.image.copy()  # 元の画像を保存
        self.colliding = False
    
    def update(self):
        self.image = self.base_image.copy()  # セルの画像をリセット
        if self.colliding:
            if not self.cards:
                pygame.draw.rect(
                self.image,
                (255, 255, 0),  # 黄色のハイライト
                self.image.get_rect(),
                width=5,
                border_radius=10,
                )

    def can_add(self, cards):
        #子クラスでオーバーライドして、カードを追加できるかどうかの条件を定義
        return NotImplementedError
    
    def add_card(self, cards):
        self.cards.extend(cards)