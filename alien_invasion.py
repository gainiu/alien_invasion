import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
import game_function as gf


def run_game():
    # 初始化pygame、设置和屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alien Invasion')

    #创建一艘飞船、一个子弹编组和一个外星人编组
    ship = Ship(screen, ai_settings)
    bullets = Group()
    aliens = Group()
    
    #创建外星人群
    gf.create_fleet(ai_settings,screen,aliens,ship)

    # 开始游戏主循环
    while True:

        gf.check_event(ship, ai_settings, screen, bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.update_aliens(ai_settings,aliens)
        gf.upgrade_screen(ai_settings, screen, ship,aliens, bullets)


run_game()
