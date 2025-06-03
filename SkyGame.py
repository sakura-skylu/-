import sys#退出游戏

import pygame #引入这两个库

from ship import Ship
from settings import Settings
import game_functions as gf#指定别名gf
from pygame.sprite import Group
from alien import Alien
from game_stats import GameStats

def run_game():
    #初始化一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_height))
    pygame.display.set_caption("SkyGame")#游戏窗口的标题栏文字
    stats = GameStats(ai_settings)

    #创建一艘飞船
    ship=Ship(ai_settings,screen)
    alien = Alien(ai_settings,screen)
    #创建一个存储子弹的编组
    bullets=Group()
    aliens=Group()
    gf.create_fleet(ai_settings,screen,ship,aliens)
    
    #设置背景色
    bg_color = (230,230,230)

    #开始游戏的主循环
    while True:
        gf.check_events(ai_settings,screen,ship,bullets)
        ship.update()
        gf.update_bullets(ai_settings,screen,ship,aliens,bullets)
        gf.update_aliens(ai_settings,stats,screen,ship,aliens,bullets)
        gf.update_screen(ai_settings,screen,ship,aliens,bullets)
       

run_game()