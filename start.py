import sys
import pygame as pg

W, H = 1200, 800
WINDOW_TITLE = "Solitaire"
FPS = 30


def draw_background(surface):
    colors = [(80, 100, 220), (80, 120, 250)]
    for x in range(0, W, 10):
        for y in range(0, H, 10):
            pg.draw.rect(surface, colors[(x // 10 + y // 10) % 2], (x, y, 10, 10))


def main():
    pg.init()
    sc = pg.display.set_mode((W, H))
    pg.display.set_caption(WINDOW_TITLE)

    clock = pg.time.Clock()

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

        draw_background(sc)
        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
