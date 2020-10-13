import sys
import pygame
from bullet import Bullet

def check_keydown_event(event,ship,ai_settings,screen,bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right=True
    elif event.key==pygame.K_LEFT:
        ship.moving_left=True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):     
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def check_keyup_event(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right=False
    elif event.key==pygame.K_LEFT:
        ship.moving_left=False

def check_event(ship,ai_settings,screen,bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event,ship,ai_settings,screen,bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event,ship)

def upgrade_screen(ai_settings,screen,ship,bullets):
    '''更新屏幕上的图像并切换到新屏幕'''
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.top <=0:
            bullets.remove(bullet)