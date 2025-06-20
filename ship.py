import pygame

class Ship():

    def __init__(self,ai_settings,screen):
        #初始化飞船及其位置
        self.screen=screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取外接矩形 rect代表一个矩形区域
        self.image=pygame.image.load('image/ship.bmp')
        self.rect=self.image.get_rect()
        self.screen_rect=screen.get_rect()

        #将每艘新飞船放在底部中央
        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        self.center=float(self.rect.centerx)
        #移动标志
        self.moving_right = False
        self.moving_left =False

    def update(self):
        if self.moving_right and self.rect.right<self.screen_rect.right:
             self.center += self.ai_settings.ship_speed_factor 
        if self.moving_left and self.rect.left>0:
             self.center -= self.ai_settings.ship_speed_factor

        self.rect.centerx=self.center

    def blitme(self):
        #把 self.image按照 self.rect 指定的位置，绘制到窗口上。
        self.screen.blit(self.image,self.rect)

    def center_ship(self): 
        """让飞船在屏幕上居中""" 
        self.center=self.screen_rect.centerx