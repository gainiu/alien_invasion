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

    ship = Ship(screen,ai_settings)
    bullets=Group()

    # 开始游戏主循环
    while True:

        gf.check_event(ship,ai_settings,screen,bullets)
        ship.update()
        gf.update_bullets(bullets)
        gf.upgrade_screen(ai_settings,screen,ship,bullets)

run_game()
