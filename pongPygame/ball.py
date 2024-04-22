import pygame


class ball(pygame.sprite.Sprite):
    """
    乒乓球类，存放相关参数
    """

    width = -1  # 宽度
    speedx = -1  # 每秒横轴移动的像素点
    speedy = -1  # 每秒纵轴移动的像素点

    def __init__(self, color, size, screensize, speed, img=False):
        pygame.sprite.Sprite.__init__(self)
        if img:  # 有图用图，忽略大小size设置，大小由图片大小确定
            try:
                self.image = pygame.image.load(img)
                self.width = self.image.get_size()[0]  # 大小修正
            except Exception as e:  # 图片文件发生错误用方块替代
                print("温馨提示： ", e, "， 请正确配置图片文件")
                self.image = pygame.Surface((size, size))
                self.width = size
                self.image.fill(color)
        else:  # 没图用方块替代
            self.image = pygame.Surface((size, size))
            self.width = size
            self.image.fill(color)
        self.rect = self.image.get_rect()  # 位置数据
        (self.WIDTH, self.HEIGHT) = screensize
        (self.speedx, self.speedy) = speed

    def reset(self, speed):
        self.rect.x = 490  # 球数据
        self.rect.y = 80
        (self.speedx, self.speedy) = speed

    def update(self):
        # 上边界处理
        if self.rect.y < 0:
            self.speedy = -self.speedy
        # 左右边界处理
        elif (
            (self.rect.x + self.width) > self.WIDTH
        ) or self.rect.x < 0:
            self.speedx = -self.speedx
        self.rect.x = self.rect.x + self.speedx
        self.rect.y = self.rect.y + self.speedy
