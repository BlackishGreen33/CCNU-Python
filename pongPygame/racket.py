import pygame


class racket(pygame.sprite.Sprite):
    """
    球拍类，存放相关参数
    """

    rktw = 100  # 球拍默认宽度
    rkth = 10  # 球拍厚度
    rkstep = 0  # 每秒球拍移动的像素个数

    def __init__(self, color, size, speed, img=False):
        pygame.sprite.Sprite.__init__(self)
        if img:  # 有图用图，忽略大小size设置，大小由图片大小确定
            try:
                self.image = pygame.image.load(img)
                self.rktw = self.image.get_size()[1]  # 大小修正
                self.rkth = self.image.get_size()[0]
            except Exception as e:  # 图片文件发生错误用方块替代
                print("温馨提示： ", e, "， 请正确配置图片文件")
                self.image = pygame.Surface(size)
                self.width = size
                self.image.fill(color)
        else:  # 没图用方块替代
            self.image = pygame.Surface(size)
            (self.rktw, self.rkth) = size
            self.image.fill(color)
        self.rect = self.image.get_rect()  # 位置数据
        self.rkstep = speed

    def reset(self):
        self.rect.y = 630
