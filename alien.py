import pygame 
from pygame.sprite import Sprite
import random

class Alien(Sprite):
    def __init__(self, ai_settings, screen, is_random=False):
        super(Alien,self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings
        self.is_random = is_random  # 标记是否为随机外星人
        self.speed_factor = ai_settings.alien_speed_factor

        # 加载外星人图像，并设置其rect属性 
        self.image = pygame.image.load('image/alien.bmp') 
        self.rect = self.image.get_rect() 
 
        # 根据是否为随机外星人设置初始位置
        if is_random:
            self.rect.x = random.randint(0, ai_settings.screen_width - self.rect.width)
            self.rect.y = -self.rect.height
            self.speed_factor = ai_settings.random_alien_speed
        else:
            self.rect.x = self.rect.width 
            self.rect.y = self.rect.height 
 
        # 存储外星人的准确位置 
        self.x = float(self.rect.x) 
        self.y = float(self.rect.y)

    def blitme(self): 
        """在指定位置绘制外星人""" 
        self.screen.blit(self.image, self.rect)

    def update(self):
        """更新外星人的位置"""
        if self.is_random:
            # 随机外星人只向下移动
            self.y += self.speed_factor
        else:
            # 常规外星人左右移动并向下
            self.x += (self.speed_factor * self.ai_settings.fleet_direction)
            self.y += self.ai_settings.fleet_drop_speed
        
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
    