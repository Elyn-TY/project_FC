import pygame
import class_Card


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Card Game Example")

cards = pygame.sprite.LayeredUpdates()
ui = pygame.sprite.LayeredUpdates()
suits = ['H', 'D', 'C', 'S']
ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

card1 = class_Card.Card(400, 300, 'H', 'A', layer=0)  # ハートのエースを作成
card2 = class_Card.Card(500, 300, 'S', 'K', layer=0)  # スペードのキングを作成
card2.pos = (500, 300)  # カード2の位置を設定

cards.add(card1, layer=card1.layer)
cards.add(card2, layer=card2.layer)

clock = pygame.time.Clock()

running = True
while running:
    screen.fill((18, 148, 44))  # 背景を深緑に

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if card1.rect.collidepoint(event.pos):
                card1.dragging = True
                cards.change_layer(card1, 999)  # ドラッグ中のカードを最前面に移動(uiよりは下)
        elif event.type == pygame.MOUSEBUTTONUP:
            card1.dragging = False
            cards.change_layer(card1, card1.layer)  # ドラッグ終了後に元のレイヤーに戻す
        elif event.type == pygame.MOUSEMOTION:
            if card1.dragging:
                card1.target_pos = event.pos
                cards.change_layer(card1, cards.get_top_layer() + 1)  # ドラッグ中のカードを常に最前面に移動(uiよりは下)
    


    if card1.mask.overlap(card2.mask, offset=(card2.rect.x - card1.rect.x, card2.rect.y - card1.rect.y)):
        card1.colliding = True
        card2.colliding = True
    else:
        card1.colliding = False
        card2.colliding = False

    #カードの更新と描画
    cards.update()
    for card in cards:
        screen.blit(card.image, card.rect)

    # マウスの位置を取得
    x, y = pygame.mouse.get_pos()

    # その位置に丸を描く
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
    pygame.draw.circle(screen, (0, 0, 0), (x,y), 5, 2)

    pygame.display.update()
    clock.tick(60)

pygame.quit()