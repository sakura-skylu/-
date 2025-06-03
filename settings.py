class Settings(): 
    """存储《外星人入侵》的所有设置的类""" 
 
    def __init__(self): 
        """初始化游戏的设置""" 
        # 屏幕设置 
        self.screen_width = 1200 
        self.screen_height = 800 
        self.bg_color = (230, 230, 230) 
        self.bg_image = 'image/background.png'  # 添加背景图路径
        self.ship_speed_factor = 30
        self.ship_limit=3
        #子弹设置
        self.bullet_speed_factor=100
        self.bullet_width=600  # 改回正常宽度
        self.bullet_height=15
        self.bullet_color=60,60,60
        self.bullets_allowed=5
       #外星人设置
        self.alien_speed_factor= 6
        self.fleet_drop_speed = 1
        # fleet_direction为1表示向右移，为-1表示向左移 
        self.fleet_direction = 1
        # 随机外星人设置
        self.random_alien_chance = 1.00  # 每帧生成随机外星人的概率
        self.max_random_aliens = 10  # 屏幕上最多允许的随机外星人数量
        self.random_alien_speed = 2.0  # 随机外星人的移动速度