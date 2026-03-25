import pygame
import class_Card


pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Card Game Example")

card1 = class_Card.Card(400, 300, 'H', 'A')  # ハートのエースを作成
card2 = class_Card.Card(500, 300, 'S', 'K')  # スペードのキングを作成
card2.pos = (500, 300)  # カード2の位置を設定

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
        elif event.type == pygame.MOUSEBUTTONUP:
            card1.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if card1.dragging:
                card1.target_pos = event.pos
    


    if card1.mask.overlap(card2.mask, offset=(card2.rect.x - card1.rect.x, card2.rect.y - card1.rect.y)):
        card1.colliding = True
        card2.colliding = True
    else:
        card1.colliding = False
        card2.colliding = False

    #カードの更新と描画
    card1.update()
    card2.update()
    screen.blit(card1.image, card1.rect)
    screen.blit(card2.image, card2.rect)

    # マウスの位置を取得
    x, y = pygame.mouse.get_pos()

    # その位置に丸を描く
    pygame.draw.circle(screen, (255, 0, 0), (x, y), 5)
    pygame.draw.circle(screen, (0, 0, 0), (x,y), 5, 2)

    pygame.display.update()
    clock.tick(60)

pygame.quit()