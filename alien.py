import pygame
from pygame.sprite import Sprite

class Alien(Sprite):

    def __init__(self,ai_settings,screen):
        '''初始化外星人并设置其初始位置'''
        super().__init__()
        self.screen=screen
        self.ai_setting=ai_settings

        #加载外星人图像并获得其外接矩形
        self.image=pygame.image.load('alien_invasion/images/alien.bmp')
        self.rect=self.image.get_rect()

        #每个外星人最初都在屏幕左上角附近
        self.rect.x=self.rect.width
        self.rect.y=self.rect.height

        #存储外星人的准确位置
        self.x=float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image,self.rect)

