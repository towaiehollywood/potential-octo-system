import pygame
import random

# Pygameの初期化
pygame.init()

# 画面設定
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("きゅうりキャッチゲーム")

# 色の定義
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# スプライト（キャラクターとアイテム）の読み込みとリサイズ
try:
    player_original_image = pygame.image.load('man.png')
    cucumber_original_image = pygame.image.load('cucumber.png')
    
    # 画像のリサイズ
    player_image = pygame.transform.scale(player_original_image, (100, 100))
    cucumber_image = pygame.transform.scale(cucumber_original_image, (50, 50))

except pygame.error as e:
    print(f"画像ファイルの読み込みに失敗しました: {e}")
    print("man.png と cucumber.png ファイルが、このスクリプトと同じフォルダにあるか確認してください。")
    pygame.quit()
    exit()

player_rect = player_image.get_rect() 
cucumber_rect = cucumber_image.get_rect()

# ゲーム変数
player_x = SCREEN_WIDTH // 2 - player_rect.width // 2
player_y = SCREEN_HEIGHT - player_rect.height - 20
player_speed_normal = 5
player_speed_boost = 10

# 体力設定
MAX_HEALTH = 100
current_health = MAX_HEALTH
health_drain_rate = 1.0
health_regen_rate = 0.1

cucumbers = []
score = 0
font = pygame.font.Font(None, 36)

# ゲームループ
running = True
while running:
    # イベント処理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # キー入力
    keys = pygame.key.get_pressed()
    current_speed = player_speed_normal

    # スペースキーが押され、かつ体力が0より大きい場合に加速
    if keys[pygame.K_SPACE] and current_health > 0:
        current_speed = player_speed_boost
        current_health -= health_drain_rate
    else:
        current_health += health_regen_rate

    # 体力の上限・下限を制限
    if current_health > MAX_HEALTH:
        current_health = MAX_HEALTH
    if current_health < 0:
        current_health = 0

    if keys[pygame.K_LEFT]:
        player_x -= current_speed
    if keys[pygame.K_RIGHT]:
        player_x += current_speed
    
    # プレイヤーが画面外に出ないように制限
    if player_x < 0:
        player_x = 0
    if player_x > SCREEN_WIDTH - player_rect.width:
        player_x = SCREEN_WIDTH - player_rect.width
    
    player_rect.x = player_x
    player_rect.y = player_y

    # きゅうりの生成
    if random.randint(1, 100) < 2:
        new_cucumber_rect = cucumber_image.get_rect(top=0, left=random.randint(0, SCREEN_WIDTH - cucumber_rect.width))
        cucumbers.append(new_cucumber_rect)

    # きゅうりの移動
    for cucumber in cucumbers[:]:
        cucumber.y += 3
        
        if cucumber.top > SCREEN_HEIGHT:
            cucumbers.remove(cucumber)

    # 衝突判定
    for cucumber in cucumbers[:]:
        if player_rect.colliderect(cucumber):
            cucumbers.remove(cucumber)
            score += 10

    # 画面描画
    screen.fill(WHITE)
    screen.blit(player_image, player_rect)
    for cucumber in cucumbers:
        screen.blit(cucumber_image, cucumber)

    # 体力ゲージの描画
    health_bar_width = 200
    health_bar_height = 20
    health_bar_x = SCREEN_WIDTH - health_bar_width - 10
    health_bar_y = 10
    
    # 背景
    pygame.draw.rect(screen, BLACK, (health_bar_x, health_bar_y, health_bar_width, health_bar_height), 2)
    
    # 体力バー
    health_percentage = current_health / MAX_HEALTH
    health_bar_fill_width = int(health_bar_width * health_percentage)
    pygame.draw.rect(screen, RED, (health_bar_x, health_bar_y, health_bar_fill_width, health_bar_height))

    # スコア表示
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 画面更新
    pygame.display.flip()
    
    # 速度調整
    pygame.time.Clock().tick(60)

# Pygame終了
pygame.quit()