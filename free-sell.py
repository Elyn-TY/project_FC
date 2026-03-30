import pygame
import class_Card


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Card Game Example")

cards = pygame.sprite.LayeredUpdates()
ui = pygame.sprite.LayeredUpdates()
suits = ['H', 'D', 'C', 'S']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

x_t = 0
y_t = 0
for suit in suits:
    for rank in ranks:
        card = class_Card.Card(x_t, y_t, suit, rank, layer=0)
        cards.add(card, layer=card.layer)
        x_t += 80
    y_t += 120



card1 = class_Card.Card(400, 300, 'H', 'A', layer=0)  # ハートのエースを作成
card2 = class_Card.Card(500, 300, 'S', 'K', layer=0)  # スペードのキングを作成
card2.pos = (500, 300)  # カード2の位置を設定

cards.add(card1, layer=card1.layer)
cards.add(card2, layer=card2.layer)

dragging_card = None


clock = pygame.time.Clock()

running = True
while running:
    screen.fill((18, 148, 44))  # 背景を深緑に

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            clicked_cards = []
            for card in cards:
                if card.rect.collidepoint(event.pos):
                    clicked_cards.append(card)
            if clicked_cards:
                top_card = max(clicked_cards, key=lambda c: cards.get_layer_of_sprite(c))  # 最前面のカードを選択
                dragging_card = top_card
                dragging_card.dragging = True
                cards.change_layer(dragging_card, cards.get_top_layer() + 1)
        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging_card:
                dragging_card.dragging = False
                cards.change_layer(dragging_card, dragging_card.layer)  # ドラッグ終了後に元のレイヤーに戻す
                dragging_card = None
        elif event.type == pygame.MOUSEMOTION:
            if dragging_card:
                dragging_card.target_pos = event.pos
                cards.change_layer(dragging_card, cards.get_top_layer() + 1)  # ドラッグ中のカードを常に最前面に移動(uiよりは下)
    
#すべてのカード同士の衝突をチェック
    for card in cards:
        others = [c for c in cards if c != card]
        for other in others:
            if card.dragging:
                if card.mask.overlap(other.mask, offset=(other.rect.x - card.rect.x, other.rect.y - card.rect.y)):
                    card.colliding = True
                    other.colliding = True
                else:
                    card.colliding = False
                    other.colliding = False
            #必要ならここに衝突していないカードの処理を追加

    #カードの更新と描画
    cards.update()
    for c in cards:
        screen.blit(c.image, c.rect)

    # マウスの位置を取得
    mouse_pos = pygame.mouse.get_pos()

    # その位置に丸を描く
    pygame.draw.circle(screen, (255, 0, 0), mouse_pos, 5)
    pygame.draw.circle(screen, (0, 0, 0), mouse_pos, 5, 2)

    pygame.display.update()
    clock.tick(60)

pygame.quit()