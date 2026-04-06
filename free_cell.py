import pygame
import class_card
import class_quit_button

# レイヤーの分類の詳細はmemo.txtを参照

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Free Cell")

cards = pygame.sprite.LayeredUpdates()
ui = pygame.sprite.LayeredUpdates()
suits = ["H", "D", "C", "S"]
ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

x_t = 0 + 20
y_t = 0 + 50
for suit in suits:  # カードの生成
    for rank in ranks:
        card = class_card.Card(x_t, y_t, suit, rank, layer=500)
        cards.add(card, layer=card.layer)
        x_t += 70
    x_t = 0 + 20
    y_t += 120

quit_button = class_quit_button.QuitButton(1180, 20, layer=1000)  # 終了ボタンの生成
quit_button.add(ui)

dragging_card = None  # ドラッグ中のカードを追跡する変数


clock = pygame.time.Clock()

running = True


while running:  # メインループ開始

    dt = clock.tick(60) / 1000

    screen.fill((18, 148, 44))  # 背景を深緑に

    if quit_button.is_clicked(pygame.mouse.get_pos()):
        quit_button.colliding = True
    else:
        quit_button.colliding = False

    for event in pygame.event.get():  # イベント判定開始
        if event.type == pygame.QUIT:  # ウィンドウの×ボタンが押されたとき
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:  # マウスのボタンが押されたとき
            if quit_button.is_clicked(pygame.mouse.get_pos()):
                running = False

            clicked_cards = []
            for card in cards:
                if card.rect.collidepoint(event.pos):
                    clicked_cards.append(card)
            if clicked_cards:
                top_card = max(
                    clicked_cards, key=lambda c: cards.get_layer_of_sprite(c)
                )  # 最前面のカードを選択
                dragging_card = top_card
                dragging_card.dragging = True
                cards.change_layer(dragging_card, cards.get_top_layer() + 1)

        elif event.type == pygame.MOUSEBUTTONUP:  # マウスのボタンが離されたとき
            if dragging_card:
                dragging_card.dragging = False
                cards.change_layer(
                    dragging_card, dragging_card.layer
                )  # ドラッグ終了後に元のレイヤーに戻す
                dragging_card = None

        elif event.type == pygame.MOUSEMOTION:  # マウスが動いたとき
            if dragging_card:
                dragging_card.target_pos = event.pos
                cards.change_layer(
                    dragging_card, cards.get_top_layer() + 1
                )  # ドラッグ中のカードを常に最前面に移動(uiよりは下)

    for card in cards:  # すべてのカード同士の衝突をチェック
        others = [c for c in cards if c != card]
        for other in others:
            if card.dragging:
                if card.mask.overlap(
                    other.mask,
                    offset=(other.rect.x - card.rect.x, other.rect.y - card.rect.y),
                ):
                    card.colliding = True
                    other.colliding = True
                else:
                    card.colliding = False
                    other.colliding = False
            # 必要ならここに衝突していないカードの処理を追加
    if not dragging_card:
        for card in cards:
            card.colliding = False

    # カードの更新と描画
    cards.update()
    # Uiの更新と描画
    ui.update()
    
    cards.draw(screen)
    ui.draw(screen)

    # マウスの位置を取得
    mouse_pos = pygame.mouse.get_pos()

    # その位置に丸を描く
    pygame.draw.circle(screen, (255, 0, 0), mouse_pos, 5)
    pygame.draw.circle(screen, (0, 0, 0), mouse_pos, 5, 2)

    pygame.display.update()


pygame.quit()
