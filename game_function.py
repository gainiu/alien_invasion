import sys
import pygame
from bullet import Bullet
from alien import Alien


def check_keydown_event(event, ship, ai_settings, screen, bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullet_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_keyup_event(event, ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_event(ship, ai_settings, screen, bullets):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event, ship, ai_settings, screen, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_event(event, ship)


def upgrade_screen(ai_settings, screen, ship, aliens, bullets):
    '''更新屏幕上的图像并切换到新屏幕'''
    # 每次循环时都重绘屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    # 让最近绘制的屏幕可见
    pygame.display.flip()


def update_bullets(bullets):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.top <= 0:
            bullets.remove(bullet)


def create_fleet(ai_settings, screen, aliens):
    '''创建外星人群'''
    # 创建一个外星人，并计算一行可容纳多少个外星人
    # 外星人间距为外星人宽度
    alien=Alien(ai_settings,screen)
    number_alien_x=get_number_aliens_x(ai_settings,screen,alien.rect.width)
    
    #创建第一行外星人
    for alien_number in range(number_alien_x):
        #创建一个外星人并将其加入当前行
        create_alien(ai_settings,screen,alien_number,aliens)
        

def get_number_aliens_x(ai_settings,screen,alien_width):
    '''计算一行可容纳多少个外星人'''
    available_space_x = ai_settings.screen_width - 2*alien_width
    number_alien_x=int(available_space_x/(2*alien_width))
    return number_alien_x

def create_alien(ai_settings,screen,alien_number,aliens):
    '''创建一个外星人并将其放置在当前行'''
    alien=Alien(ai_settings,screen)
    alien_width=alien.rect.width
    alien.x=alien_width+2*alien_width*alien_number
    alien.rect.x=alien.x
    aliens.add(alien)
