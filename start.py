import sys
import random

from settings import pg, W, H, WINDOW_TITLE, FPS
from functions import create_deck, refresh_animations, draw_cards, draw_background
from classes import Animation


def main():
    pg.init()
    sc = pg.display.set_mode((W, H))
    pg.display.set_caption(WINDOW_TITLE)

    clock = pg.time.Clock()

    deck = create_deck()
    cards = [random.choice(deck)]
    animations = []

    while True:
        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

            if animations:
                continue

            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == pg.BUTTON_LEFT:
                    animations.append(Animation(cards[0], *event.pos))
                if event.button == pg.BUTTON_MIDDLE:
                    animations.append(Animation(cards[0], *event.pos, delay=15))
                if event.button == pg.BUTTON_RIGHT:
                    animations.append(Animation(cards[0], *event.pos, turn=True))

        if animations:
            animations = refresh_animations(animations)

        draw_background(sc)
        draw_cards(sc, cards)
        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
