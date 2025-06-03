import sys 
import pygame 
import random  # 添加随机数模块
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydowm_events(event,ai_settings,screen,ship,bullets):
  if event.key == pygame.K_RIGHT:
            ship.moving_right=True
  elif event.key == pygame.K_LEFT:
            ship.moving_left=True
  elif event.key == pygame.K_SPACE:
       fire_bullet(ai_settings,screen,ship,bullets)
      
def check_keyup_events(event,ship):
  if event.key == pygame.K_RIGHT:
            ship.moving_right=False
  elif event.key == pygame.K_LEFT:
            ship.moving_left=False
  
def check_events(ai_settings,screen,ship,bullets):
  for event in pygame.event.get(): 
    if event.type == pygame.QUIT: 
      sys.exit() 
    elif event.type == pygame.KEYDOWN:
        check_keydowm_events(event,ai_settings,screen,ship,bullets)
    elif event.type == pygame.KEYUP:
        check_keyup_events(event,ship)

def update_screen(ai_settings,screen,ship,aliens,bullets):
          #每次循环重绘制屏幕
        # 加载并绘制背景图
        bg_image = pygame.image.load(ai_settings.bg_image)
        # 调整背景图大小以匹配屏幕尺寸
        bg_image = pygame.transform.scale(bg_image, (ai_settings.screen_width, ai_settings.screen_height))
        screen.blit(bg_image, (0, 0))
        
        ship.blitme()
        aliens.draw(screen)
        for bullet in bullets.sprites():
              bullet.draw_bullet()
        #让最近绘制的屏幕可见 不断更新屏幕显示元素的新位置
        pygame.display.flip()

def update_bullets(ai_settings,screen,ship,aliens,bullets):
     """更新子弹的位置，并删除已消失的子弹"""
     bullets.update()
     
     # 删除已消失的子弹
     for bullet in bullets.copy():
         if bullet.rect.bottom <= 0:
             bullets.remove(bullet)
     
     # 检查子弹和外星人的碰撞
     check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets)

def fire_bullet(ai_settings,screen,ship,bullets):
      if len(bullets)<ai_settings.bullets_allowed:
        new_bullet=Bullet(ai_settings,screen,ship)
        bullets.add(new_bullet)

def get_number_aliens_x(ai_settings,alien_width):
     available_space_x=ai_settings.screen_width-2*alien_width
     number_aliens_x=int(available_space_x/(2*alien_width))
     return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
     """创建一个外星人并将其放在当前行""" 
     alien = Alien(ai_settings, screen) 
     alien_width = alien.rect.width 
     alien.x = alien_width + 2 * alien_width * alien_number 
     alien.rect.x = alien.x 
     alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
     aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):  
    # 创建一个外星人，并计算每行可容纳多少个外星人 
    alien = Alien(ai_settings, screen) 
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width) 
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    # 创建第一行外星人 
    for row_number in range(number_rows):
      for alien_number in range(number_aliens_x): 
        create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_rows(ai_settings,ship_height,alien_height):
     available_space_y=(ai_settings.screen_height-(3*alien_height)-ship_height)
     number_rows=int(available_space_y/(2*alien_height))
     return number_rows

def create_random_alien(ai_settings, screen, aliens):
    """在屏幕顶部随机位置创建一个外星人"""
    if len(aliens) < ai_settings.max_random_aliens:
        if random.random() < ai_settings.random_alien_chance:
            # 创建随机外星人，设置is_random=True
            alien = Alien(ai_settings, screen, is_random=True)
            aliens.add(alien)

def update_aliens(ai_settings,stats,screen,ship,aliens,bullets):
     check_fleet_edges(ai_settings,aliens)
     aliens.update()
     # 生成随机外星人
     create_random_alien(ai_settings, screen, aliens)
     if pygame.sprite.spritecollideany(ship,aliens):
          ship_hit(ai_settings,stats,screen,ship,aliens,bullets)
     check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)

def check_fleet_edges(ai_settings,aliens):
     for alien in aliens.sprites():
          if alien.check_edges():
             change_fleet_direction(ai_settings, aliens) 
             break  

def change_fleet_direction(ai_settings,aliens):
     for alien in aliens.sprites():
          alien.rect.y+=ai_settings.fleet_drop_speed
     ai_settings.fleet_direction*=-1

def check_bullet_alien_collision(ai_settings,screen,ship,aliens,bullets):
     """检查子弹和外星人的碰撞"""
     # 检查是否有子弹击中了外星人
     collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
     
     # 如果所有外星人都被消灭，创建新的外星人舰队
     if len(aliens) == 0:
         bullets.empty()
         create_fleet(ai_settings, screen, ship, aliens)

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets): 
    """响应被外星人撞到的飞船""" 
    # 将ships_left减1 
    if stats.ships_left>0:
      stats.ships_left -= 1 
     
    # 清空外星人列表和子弹列表
      aliens.empty() 
      bullets.empty() 
     
    # 创建一群新的外星人，并将飞船放到屏幕底端中央
      create_fleet(ai_settings, screen, ship, aliens) 
      ship.center_ship() 
      sleep(0.5)
       
    else:
         stats.game_active=False
         aliens.empty()



def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets): 
    """检查是否有外星人到达了屏幕底端""" 
    screen_rect = screen.get_rect() 
    for alien in aliens.sprites():
       if alien.rect.bottom >= screen_rect.bottom: 
            # 像飞船被撞到一样进行处理 
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets) 
            break