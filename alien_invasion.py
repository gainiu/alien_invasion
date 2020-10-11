import pygame
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

    # 开始游戏主循环
    while True:

        gf.check_event(ship)
        ship.update()
        gf.upgrade_screen(ai_settings,screen,ship)


run_game()
