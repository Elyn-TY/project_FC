import pygame

# レイヤーの分類の詳細はmemo.txtを参照


class Card(pygame.sprite.Sprite):

    suit_symbols = {"H": "♥", "D": "♦", "C": "♣", "S": "♠"}
    rank_values = {
        "A": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5,
        "6": 6,
        "7": 7,
        "8": 8,
        "9": 9,
        "10": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
    }
        
    def __init__(self, x, y, suit, rank, layer=500):
        super().__init__()  # Spriteクラスの初期化
        font = pygame.font.SysFont("meiryo", 25, bold=True)
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
                Card.suit_symbols[self.suit] + " " + self.rank, True, (255, 0, 0)
            )
            self.text_color = (255, 0, 0)
        else:
            self.text = font.render(
                Card.suit_symbols[self.suit] + " " + self.rank, True, (0, 0, 0)
            )
            self.text_color = (0, 0, 0)

        self.text_rect = self.text.get_rect(
            center=self.image.get_rect().center
        )  # カードの中心にテキストを配置
        self.image.blit(self.text, self.text_rect)
        self.dragging = False
        self.drag_offset = (0, 0)
        self.colliding = False
        self.setted = None
        self.couple = []
        pygame.draw.rect(
            self.image, (0, 0, 0), self.image.get_rect(), width=2, border_radius=10
        )  # カードの枠線
        self.base_image = self.image.copy()  # 元の画像を保存
        self.mask = pygame.mask.from_surface(self.image)  # マスクを作成
        self.motioning = False  # カードが移動中かどうかを追跡するフラグ
        self.cursored = False


    def couple_judge(self, cards):
        collided = pygame.sprite.Group(pygame.sprite.spritecollide(self, cards, dokill=False)).sprites()
        any_self = self
        while True:
            index = collided.index(any_self)
            while index < len(collided) - 1:
                index = collided.index(any_self)
                if any_self.text_color != collided[index + 1].text_color:
                    if Card.rank_values[any_self.rank] == Card.rank_values[collided[index + 1].rank] + 1:
                        any_self.couple += [any_self, collided[index + 1]]
                        any_self = collided[index + 1]
                    else:
                        any_self.couple = []
                        break
                else:
                    any_self.couple = []
                    break
            break

    def is_cursored(self, pos):
        if not self.rect.collidepoint(pos):
            return False

        local_pos = (pos[0] - self.rect.x, pos[1] - self.rect.y)

        return self.mask.get_at(local_pos)


    def update(self):
        self.image = self.base_image.copy()  # カードの画像をリセット
        if self.dragging:
            if self.motioning:
                self.rect.topleft = (
                    pygame.mouse.get_pos()[0] + self.drag_offset[0],
                    pygame.mouse.get_pos()[1] + self.drag_offset[1]
                    )
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
        if self.cursored:
            if self.couple:
                for i in range(len(self.couple)):
                    pygame.draw.rect(
                        self.couple[i].image,
                        (0, 0, 255),  # 青色のハイライト
                        self.couple[i].image.get_rect(),
                        width=5,
                        border_radius=10,
                        )
