import sys

from settings import pg, W, H, WINDOW_TITLE, FPS
from functions import draw_animations, draw_cards, draw_background
from classes import Deck


def main():
    pg.init()
    sc = pg.display.set_mode((W, H))
    pg.display.set_caption(WINDOW_TITLE)

    clock = pg.time.Clock()

    deck = Deck()
    cards = deck.cards[:]
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
                pass

        draw_background(sc)
        draw_cards(sc, cards)
        draw_animations(animations)

        pg.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
