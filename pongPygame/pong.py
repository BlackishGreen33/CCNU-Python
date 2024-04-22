import sys
import pygame
from pygame.locals import K_SPACE, K_a, K_d
from ball import ball
from racket import racket

MHIT = "music/pong.ogg"  # 击球声音文件路径
MBEG = "music/maliaobegin.ogg"  # 开始音频
MFAIL = "music/fail.ogg"  # 游戏失败音频
MBAK = "music/maliaorun.ogg"  # 背景音乐音频

WIDTH = 808
HEIGHT = 640
FPS = 60
CBACK = (153, 255, 0)
CBALL = (245, 245, 220)
CRKT = (200, 0, 0)
CFONT = (0, 0, 0)


def main():
    isload = False  # 音乐是否载入
    isfont = False  # 字体是否存在
    ispause = False  # 是否暂停
    isfail = False
    score = 0  # 分数
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong Pygame program")
    clock = pygame.time.Clock()

    bball = ball(CBALL, 20, (WIDTH, HEIGHT), (280 / FPS, 180 / FPS), "img/ball.png")
    bball.rect.x = 490
    bball.rect.y = 80
    rkt = racket(CRKT, (100, 10), 220 / FPS, "img/pingpongbat.png")
    rkt.rect.x = 0
    rkt.rect.y = HEIGHT - 10

    ball_list = pygame.sprite.Group()  # 存放小球
    all_list = pygame.sprite.Group()  # 存放全部
    ball_list.add(bball)
    all_list.add(bball)
    all_list.add(rkt)

    pygame.mixer.init()  # 初始化音频模块并载入音频文件
    try:
        mhit = pygame.mixer.Sound(MHIT)
        mbegin = pygame.mixer.Sound(MBEG)
        mbegin.set_volume(0.2)
        mfail = pygame.mixer.Sound(MFAIL)
        pygame.mixer.music.load(MBAK)
        pygame.mixer.music.set_volume(0.4)
        isload = True
    except Exception as m:
        print("温馨提示： ", m, "， 请正确配置音频文件")
    if isload:  # 载入失败不会推出，后面不会有音乐罢了
        pygame.mixer.music.play(-1)  # 循环播放
        mbegin.play()

        # 找不到calibri字体就会使用pygame默认字体，都不支持中文
    try:
        ft = pygame.font.SysFont("calibri", 30)
        ftg = pygame.font.SysFont("calibri", 99)
        isfont = True
    except FileNotFoundError as e:
        print("温馨提示： ", e, "， 请在电脑上安装对应的字体")
    while True:
        screen.fill(CBACK)  # 清空画面为背景色

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # 关闭pygame模块
                sys.exit(0)  # 关闭程序
            # 空格键按下响应，长摁无效
            if event.type == pygame.KEYDOWN and pygame.key.get_pressed()[K_SPACE]:
                ispause = not ispause
                if isfail:
                    isfail = False  # 重新开始，重置数据
                    bball.reset((280 / FPS, 180 / FPS))
                    rkt.reset()
                    score = 0
                    if isload:
                        mbegin.play()

        # 未暂停且未结束的情况下才处理移动
        if (not ispause) and (not isfail):
            if (rkt.rect.x - rkt.rkstep >= 0) and pygame.key.get_pressed()[K_a]:
                rkt.rect.x = rkt.rect.x - rkt.rkstep
            if (
                rkt.rect.x + rkt.rktw + rkt.rkstep <= WIDTH
            ) and pygame.key.get_pressed()[K_d]:
                rkt.rect.x = rkt.rect.x + rkt.rkstep

            # 监听鼠标移动事件
            if event.type == pygame.MOUSEMOTION:
                # 根据鼠标的水平位置调整球拍的位置
                rkt.rect.x = event.pos[0] - rkt.rktw // 2

            bball.update()
            if bball.rect.y + bball.rect.height > HEIGHT - rkt.rect.height:  # 下边界
                # 像素遮罩（碰撞）检测
                if pygame.sprite.collide_mask(bball, rkt):
                    score += 1
                    bball.speedy = -bball.speedy
                    # 避免音频未正确加载导致的程序异常结束
                    if isload:
                        mhit.play()
                # 未击中球拍
                else:
                    ispause = True
                    isfail = True
                    if isload:
                        mfail.play()

        if isfail and isfont:
            tover = ftg.render("Game Over", True, CFONT)
            trest = ft.render("Press SPACE to start again", True, CFONT)
            screen.blit(tover, (150, 200))
            screen.blit(trest, (220, 400))
        if ispause and isfont and (not isfail):
            pause = ft.render("Press SPACE to continue", True, CFONT)
            screen.blit(pause, (250, 300))
        if isfont:
            text = ft.render("Score: " + str(score), True, CFONT)
            screen.blit(text, (100, 0))
        all_list.draw(screen)  # 绘制所有的sprite对象
        clock.tick(FPS)  # 以每秒30帧的速率进行绘制
        pygame.display.update()


if __name__ == "__main__":
    main()
